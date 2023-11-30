# Use the official Python base image
FROM python:3.9-slim

RUN apt-get update && apt-get install git libgl1-mesa-glx ffmpeg libsm6 libxext6  -y

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

RUN pip install git+https://github.com/Kohulan/DECIMER-Image_Transformer.git
RUN pip install decimer_segmentation --no-deps
RUN pip install numpy==1.23.5

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8080

ENV PYSTOW_HOME="modal"

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]