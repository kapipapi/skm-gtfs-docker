# Use the official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Update the package list and install the GDAL dependencies
RUN apt-get update
RUN apt-get install -y gdal-bin libgdal-dev g++

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY ./src .

# Expose the port on which the Flask server will run
EXPOSE 8800

# Set the entrypoint command to start the Flask server
CMD ["flask", "run", "--port=8800", "--host=0.0.0.0"]
