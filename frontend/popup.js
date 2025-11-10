document.addEventListener('DOMContentLoaded', function () {
    let serverAddress = '127.0.0.1'; 
    
    document.getElementById('summarizeBtn').addEventListener('click', async () => {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      chrome.scripting.executeScript(
        {
          target: { tabId: tab.id },
          func: () => {
            try {
              return document.body?.innerText || 'EMPTY';
            } catch (e) {
              return 'SCRIPT_ERROR';
            }
          }
        },
        async (results) => {
          const pageText = results?.[0]?.result || '';
          console.log('Extracted text:', pageText.slice(0, 500));
          
          if (pageText === 'SCRIPT_ERROR') {
            document.getElementById('output').innerText = 'Could not access page content (script error).';
            return;
          }
          
          if (!pageText || pageText.trim() === 'EMPTY') {
            document.getElementById('output').innerText = 'No page text found.';
            return;
          }
          
          try {
            console.log(`Sending streaming POST to http://${serverAddress}:7864/summarize_stream_status`);
            
            const res = await fetch(`http://${serverAddress}:7864/summarize_stream_status`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ content: pageText }),
            });
            
            const reader = res.body.getReader();
            const decoder = new TextDecoder();
            let resultText = '';
            
            while (true) {
              const { done, value } = await reader.read();
              if (done) break;
              
              const chunk = decoder.decode(value, { stream: true });
              resultText += chunk;
              document.getElementById('output').innerText = resultText;
            }
          } catch (err) {
            console.error('Fetch error:', err);
            document.getElementById('output').innerText = 'Failed to get summary.\n' + err.message;
          }
        }
      );
    });
});
