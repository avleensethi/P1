import os
import openai
import uvicorn
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API Key
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
if not AIPROXY_TOKEN:
    raise ValueError("AIPROXY_TOKEN is not set in the environment variables.")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=AIPROXY_TOKEN)

# Initialize FastAPI app
app = FastAPI()

# Endpoint: Read file contents
@app.get("/read")
def read_file(path: str):
    try:
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(path, "r") as file:
            content = file.read().strip()
        
        if not content:
            raise HTTPException(status_code=400, detail="File is empty")

        return {"content": content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Execute a task using OpenAI API
@app.post("/run")
def run_task(task: str):
    try:
        response = client.completions.create(
            model="gpt-4",
            prompt=f"Execute: {task}",
            max_tokens=100
        )
        return {"result": response.choices[0].text.strip()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
