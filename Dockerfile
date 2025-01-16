# Use a specific Python version for predictability
FROM python:3.10-slim

# Upgrade pip
RUN pip install --upgrade pip

# Set up working directory
WORKDIR /technews

# Copy only requirements first (cache-friendly)
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY ./src ./src

# Command to run your application
CMD ["python3", "./src/main.py"]
