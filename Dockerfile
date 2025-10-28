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
    libxcb-cursor0 \
    libxcb-xinerama0 \
    libxkbcommon-x11-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy everything into the container
COPY . .

# Run your application when the container starts
CMD ["python3", "main.py"]