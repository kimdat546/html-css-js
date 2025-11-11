# Laptop Theft Monitor - Dockerfile
# Multi-stage build for smaller image size

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Chrome/Chromium dependencies
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    # Install Chromium
    chromium \
    chromium-driver \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome/Chromium environment variables
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for data persistence
RUN mkdir -p /app/browser_profile /app/data

# Set environment variables for headless operation
ENV HEADLESS_BROWSER=true
ENV BROWSER_PROFILE_PATH=/app/browser_profile
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=1h --timeout=30s --start-period=10s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('/app/data') else 1)"

# Run the monitor in continuous mode
CMD ["python", "-u", "monitor.py", "--continuous"]
