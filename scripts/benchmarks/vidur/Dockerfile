FROM python:3.10-slim

WORKDIR /app

# Install git and required system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Clone VIDUR repository
RUN git clone https://github.com/microsoft/vidur.git /app

# Install Python dependencies
RUN pip install --no-cache-dir numpy pandas scikit-learn plotly_express matplotlib seaborn fasteners ddsketch randomname pyyaml wandb

# Disable wandb by default
ENV WANDB_MODE=disabled

# Set entrypoint
ENTRYPOINT ["python", "-m", "vidur.main"]
