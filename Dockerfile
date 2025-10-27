# Use Ubuntu as base image
FROM ubuntu:latest

# Set working directory inside the container
WORKDIR /app

# Install all packages in a single layer for better caching
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-pyqt6 \
    ffmpeg \
    libsm6 \
    libxext6 \
    libegl1 \
    libxcb-cursor0 \
    libx11-xcb1 \
    libxcb1 \
    libxcb-keysyms1 \
    libxcb-image0 \
    libxcb-shm0 \
    libxcb-icccm4 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxrender1 \
    libxkbcommon-x11-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy everything into the container
COPY . .

# Install Python dependencies if you have a requirements.txt file
# Uncomment the next line if you have a requirements.txt
# RUN pip3 install -r requirements.txt

# Run your application when the container starts
CMD ["python3", "main.py"]