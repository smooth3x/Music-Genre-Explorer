# Backend Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY . .

RUN pytest -v test.py

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & pytest -v test.py"]
