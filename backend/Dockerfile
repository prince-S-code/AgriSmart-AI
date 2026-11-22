FROM python:3.12-slim
WORKDIR /app
ARG INSTALL_YOLO=false
RUN if [ "$INSTALL_YOLO" = "true" ]; then \
    apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*; \
    fi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN if [ "$INSTALL_YOLO" = "true" ]; then pip install --no-cache-dir ultralytics==8.3.40; fi
COPY . .
EXPOSE 10000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
