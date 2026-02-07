# nn-Meter evaluation environment
FROM python:3.10-slim

WORKDIR /app

# Install nn-meter with pinned sklearn and numpy versions for compatibility
RUN pip install --no-cache-dir numpy==1.26.4 scikit-learn==1.0.2 nn-meter==2.0 onnx==1.14.0

# Install PyTorch CPU from pytorch index (1.13.1 is the oldest available for aarch64)
RUN pip install --no-cache-dir \
    torch==1.13.1 torchvision==0.14.1 --index-url https://download.pytorch.org/whl/cpu

# Copy evaluation script
COPY run_all.py .

# Create output directory
RUN mkdir -p /output

CMD ["python", "run_all.py"]
