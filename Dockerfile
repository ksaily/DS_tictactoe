# Use the official Python image as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

RUN rm -rf /app
# Copy the server and client files into the container
COPY server.py /app/server.py
COPY client.py /app/client.py

# Expose the port the server will listen on
EXPOSE 5555

CMD ["python", "server.py"]
