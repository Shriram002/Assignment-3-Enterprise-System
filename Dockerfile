# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y build-essential cmake libgtk-3-dev libboost-all-dev && \
    pip install --no-cache-dir -r requirements.txt

# Make port 10000 available to the world outside this container
EXPOSE 10000

# Define environment variable
ENV FLASK_APP=app.py

# Run flask app when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
