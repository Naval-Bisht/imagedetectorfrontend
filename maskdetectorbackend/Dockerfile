# # Use official Python 3.12.3 slim image as base
# FROM python:3.12.3-slim

# # Set working directory in the container
# WORKDIR /app

# # Install system dependencies for OpenCV and Matplotlib
# RUN apt-get update && apt-get install -y \
#     libgl1 \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# # Upgrade pip
# RUN pip install --upgrade pip

# # Copy and install requirements
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# # Copy the project files
# COPY model.py .
# COPY unet_model.h5 .
# COPY images/ images/

# # Command to run the script interactively
# CMD ["python", "model.py"]



FROM python:3.12.3-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY unet_model.h5 .
COPY images/ images/
EXPOSE 5000
CMD ["python", "app.py"]