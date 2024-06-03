# Code Execution Site

This project consists of a frontend and backend setup to provide a code execution environment for Python code using pandas and scipy libraries.

## Frontend Setup

1. Navigate to the `code_execution_site` directory:
   ```bash
   cd code_execution_site
   ```

2. Install the dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## Additional Information

- Ensure Docker is installed and running on your machine to execute the code within a containerized environment.
- The backend is configured to connect to a PostgreSQL database. Make sure to set up your database connection string in a `.env` file with the key `POSTGRES_URL`.
- Make sure frontend is exposed to the backend api url

With these steps, you'll have both the frontend and backend running locally, ready to execute and test Python code!

---

By Vithun Vigneswaran