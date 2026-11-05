# =============================================================================
# AI Production Agent - Dockerfile
# Multi-stage build for production
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Base Image with CUDA
# -----------------------------------------------------------------------------
FROM nvidia/cuda:12.1.1-base-ubuntu22.04 as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    wget \
    ca-certificates \
    libssl-dev \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Stage 2: Install Python Dependencies
# -----------------------------------------------------------------------------
FROM base as dependencies

# Set Python as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 3: Final Image
# -----------------------------------------------------------------------------
FROM base as final

# Copy virtual environment
COPY --from=dependencies /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create app directory
WORKDIR /app

# Copy application code
COPY . .

# Create directories
RUN mkdir -p /app/models /app/storage/uploads /app/storage/outputs /app/storage/cache

# Set permissions
RUN chmod -R 755 /app/storage

# Expose ports
EXPOSE 8000 5555

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()" || exit 1

# Command to run
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
