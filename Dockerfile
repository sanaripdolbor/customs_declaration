# Use a base image that supports your Flask application (e.g., Python 3.9)
FROM python:3.10.6

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Install Gunicorn
RUN pip install gunicorn

# Expose the port on which your application will run (e.g., 8000)
EXPOSE 5000

# Set the entrypoint command to start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]