# Use Python 3.9 base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to cache dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 (Render uses $PORT env var, but we bind to it in CMD)
EXPOSE 5000

# Start the app using Gunicorn from the backend folder
# Note: We use 'sh -c' to change directory before starting
CMD ["sh", "-c", "cd backend && gunicorn app:app --bind 0.0.0.0:$PORT"]
