# .devcontainer/Dockerfile
# Use the official image as a parent image
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir streamlit_lottie

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit when the container launches
CMD ["streamlit", "run", "overview.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
