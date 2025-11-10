import logging, os, asyncio, re
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

#model 
app = FastAPI()
class RequestData(BaseModel):
    content: str

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    # task="conversational",
    max_new_tokens=500,
    do_sample=False,
    temperature=0.1, 
    huggingfacehub_api_token= os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    streaming=True
)

# Wrap it in ChatHuggingFace for conversational task
chat_model = ChatHuggingFace(llm=llm)

# Create a chat prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a summarization assistant. Directly output the cleaned summary of the given text without any reasoning, self-talk, thoughts, or internal planning steps."),
    ("human", "{content}")
])

# Create the chain
bot = prompt | chat_model

#endpoint
@app.post("/summarize_stream_status")
async def summarize_stream_status(data: RequestData):
    user_input = data.content
    
    # Use async generator instead of regular generator
    async def stream():
        try:
            yield "🔍 Reading content on website...\n"
            await asyncio.sleep(0.1)  # Small delay to ensure streaming
            
            print("Received text:", user_input[:200])
            
            messages = [
                {"role": "system", "content": "You are a summarization assistant. Directly output the cleaned summary of the given text without any reasoning, self-talk, thoughts, or internal planning steps. Do not include phrases like 'I think', 'maybe', 'let's', 'the user wants', or anything not part of the final summary. Your output must look like it was written by an editor, not a model."},
                {"role": "user", "content": "<nothink>\nSummarize the following text clearly and concisely. Do not include any internal thoughts, planning, or reasoning. Just return the final summary:\n\n" + user_input + "\n</nothink>"}
            ]
            
            yield "🧠 Generating summary...\n"
            await asyncio.sleep(0.1)
            
            # Run blocking bot.invoke in thread pool to avoid blocking
            result = await asyncio.to_thread(bot.invoke, messages)
            
            print("Raw result:", result)
            
            # Extract the content from the result
            if hasattr(result, 'content'):
                last_content = result.content
            elif isinstance(result, dict) and 'content' in result:
                last_content = result['content']
            elif isinstance(result, str):
                last_content = result
            else:
                last_content = str(result)
            
            if not last_content:
                yield "❌ No valid summary found.\n"
                return
            
            # Clean up the summary
            summary = re.sub(r"</?think>", "", last_content)
            summary = re.sub(
                r"(?s)^.*?(Summary:|Here's a summary|The key points are|Your tutorial|This tutorial|To summarize|Final summary:)", 
                "", 
                summary, 
                flags=re.IGNORECASE
            )
            summary = re.sub(r"\n{3,}", "\n\n", summary)
            summary = summary.strip()
            
            yield "\n📄 Summary:\n"
            await asyncio.sleep(0.05)
            
            # Stream the summary character by character for better UX
            for char in summary:
                yield char
                await asyncio.sleep(0.01)  # Adjust speed as needed
            
            yield "\n"
            
        except Exception as e:
            print("Error:", e)
            yield f"\n❌ Error: {str(e)}\n"
    
    # Important: Set headers to prevent buffering
    return StreamingResponse(
        stream(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )