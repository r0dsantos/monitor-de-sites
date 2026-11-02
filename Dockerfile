FROM python:3.12-slim
WORKDIR /app
COPY monitor.py sites.txt ./
CMD ["python", "monitor.py"]
