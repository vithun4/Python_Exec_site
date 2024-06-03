from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
import uuid
import json

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
        raise HTTPException(status_code=500, detail="Error executing code")

@app.post("/test-code")
async def test_code(payload: CodePayload):
    code_id = str(uuid.uuid4())
    code_file = f"/tmp/{code_id}.py"
    result_file = f"/tmp/{code_id}_result.json"
    user_id = os.getuid()

    with open(code_file, "w") as f:
        print(f"payload: {payload}")
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
        raise HTTPException(status_code=500, detail="Error executing code")
    except PermissionError as e:
        raise HTTPException(status_code=500, detail=f"Permission error: {str(e)}")

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

        # Persist code and result to database (assuming a SQLAlchemy setup)
        # from sqlalchemy import create_engine, MetaData, Table, Column, String
        # engine = create_engine("your_database_url")
        # metadata = MetaData()
        # codes_table = Table(
        #     "codes", metadata,
        #     Column("id", String, primary_key=True),
        #     Column("code", String),
        #     Column("result", String),
        #     Column("stdout", String),
        #     Column("stderr", String)
        # )
        # conn = engine.connect()
        # conn.execute(codes_table.insert().values(
        #     id=code_id, code=payload.code, 
        #     result=json.dumps(result['result']), 
        #     stdout=result['stdout'], 
        #     stderr=result['stderr']
        # ))
        # conn.close()

        os.remove(result_file)
        os.remove(code_file)

        return {"message": "Code submitted successfully", "output": result['result']}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Error executing code")
    except PermissionError as e:
        raise HTTPException(status_code=500, detail=f"Permission error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
