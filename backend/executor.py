import sys
import json
import traceback
import io

def execute_user_code(code):
    try:
        # Redirect stdout and stderr
        stdout = io.StringIO()
        stderr = io.StringIO()
        sys.stdout = stdout
        sys.stderr = stderr

        exec_globals = {}
        exec_locals = {}
        exec(code, exec_globals, exec_locals)

        # Check for 'result' variable first
        if 'result' in exec_locals:
            result = exec_locals['result']
        else:
            # Get the last expression value if no 'result' variable
            result = list(exec_locals.values())[-1] if exec_locals else None
        
        output = stdout.getvalue()
        error_output = stderr.getvalue()

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        return {
            "status": "success",
            "result": result,
            "stdout": output,
            "stderr": error_output
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "stdout": stdout.getvalue(),
            "stderr": stderr.getvalue()
        }

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        user_code = f.read()
    
    result = execute_user_code(user_code)
    
    with open(sys.argv[2], 'w') as f:
        json.dump(result, f)
