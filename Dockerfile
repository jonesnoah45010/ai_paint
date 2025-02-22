
FROM python:3.9

# Set the working directory
WORKDIR /app


# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

ENV PORT=8080

# Set the command to run the Flask app
CMD ["python", "main.py"]


