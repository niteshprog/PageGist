import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"],
)

result = client.feature_extraction(
    "Today is a sunny day and I will get some ice cream.",
    model="Qwen/Qwen3-Embedding-0.6B",
)