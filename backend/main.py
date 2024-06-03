from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
import uuid
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",  # Your React app URL
    "http://127.0.0.1:3000",  # Another way to access your React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodePayload(BaseModel):
    code: str

def run_docker_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing docker command: {e}")
        raise HTTPException(status_code=500, detail="Error executing code")

# Database setup
DATABASE_URL = os.getenv("POSTGRES_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.post("/test-code")
async def test_code(payload: CodePayload):
    code_id = str(uuid.uuid4())
    code_file = f"/tmp/{code_id}.py"
    result_file = f"/tmp/{code_id}_result.json"
    user_id = os.getuid()

    with open(code_file, "w") as f:
        f.write(payload.code)
    
    try:
        run_docker_command(["docker", "buildx", "build", "--load", "-t", code_id, "."])
        run_docker_command([
            "docker", "run", "--rm", 
            "-v", f"{os.path.dirname(code_file)}:/tmp", 
            "-u", f"{user_id}:{user_id}",  # Run Docker with the same user ID
            code_id, code_file, result_file
        ])
        
        with open(result_file, "r") as f:
            result = json.load(f)
        
        os.remove(result_file)
        os.remove(code_file)

        if result['status'] == 'error':
            raise HTTPException(status_code=400, detail={
                "error": result['error'],
                "traceback": result['traceback'],
                "stdout": result['stdout'],
                "stderr": result['stderr']
            })
        
        return {
            "status": "success",
            "result": result['result'],
            "stdout": result['stdout'],
            "stderr": result['stderr']
        }
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        raise HTTPException(status_code=500, detail="Error executing code")
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        raise HTTPException(status_code=500, detail=f"Permission error: {str(e)}")
    finally:
        if os.path.exists(result_file):
            os.remove(result_file)
        if os.path.exists(code_file):
            os.remove(code_file)

@app.post("/submit-code")
async def submit_code(payload: CodePayload):
    code_id = str(uuid.uuid4())
    code_file = f"/tmp/{code_id}.py"
    result_file = f"/tmp/{code_id}_result.json"
    user_id = os.getuid()

    with open(code_file, "w") as f:
        f.write(payload.code)
    
    try:
        run_docker_command(["docker", "buildx", "build", "--load", "-t", code_id, "."])
        run_docker_command([
            "docker", "run", "--rm", 
            "-v", f"{os.path.dirname(code_file)}:/tmp", 
            "-u", f"{user_id}:{user_id}",  # Run Docker with the same user ID
            code_id, code_file, result_file
        ])
        
        with open(result_file, "r") as f:
            result = json.load(f)

        if result['status'] != 'success':
            raise HTTPException(status_code=400, detail={
                "error": result['error'],
                "traceback": result['traceback'],
                "stdout": result['stdout'],
                "stderr": result['stderr']
            })

        # Persist code and result to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO code_submissions (created_at, user_code, execution_output)
            VALUES ( %s, %s, %s)
            """,
            (datetime.utcnow(), payload.code, json.dumps(result))
        )
        conn.commit()
        cursor.close()
        conn.close()

        os.remove(result_file)
        os.remove(code_file)

        return {
            "message": "Code submitted successfully", 
            "result": result['result'],
            "stdout": result['stdout'],
            "stderr": result['stderr']}
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        raise HTTPException(status_code=500, detail="Error executing code")
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        raise HTTPException(status_code=500, detail=f"Permission error: {str(e)}")
    finally:
        if os.path.exists(result_file):
            os.remove(result_file)
        if os.path.exists(code_file):
            os.remove(code_file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
