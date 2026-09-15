FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 TORCH_HOME=/opt/models TORCH_NUM_THREADS=1
WORKDIR /app
COPY apps/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt Pillow==11.3.0 \
    && pip install --no-cache-dir torch==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cpu
COPY apps/classifier/download_model.py /app/download_model.py
RUN python download_model.py && chmod -R a+rX /opt/models
COPY apps/common /app/common
COPY apps/classifier /app
COPY apps/shared /app/static
USER 10001:10001
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "2", "--timeout", "90", "--worker-tmp-dir", "/tmp", "app:app"]
