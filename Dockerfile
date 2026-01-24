FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git curl ffmpeg wget bash neofetch software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching pip install)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt

# Set workdir and copy project
WORKDIR /app
COPY . .

# Expose port
EXPOSE 8000

# Use JSON array syntax to avoid CMD warning
CMD ["sh", "-c", "flask run -h 0.0.0.0 -p 8000 & python3 -m kalbhau"]
