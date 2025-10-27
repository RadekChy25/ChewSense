# Use lowercase image name
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
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

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your application (don’t run during build!)
CMD ["python", "main.py"]
