# Dockerfile
FROM python:3.11-slim

RUN pip install pandas scipy

COPY executor.py /executor.py

ENTRYPOINT ["python", "/executor.py"]
