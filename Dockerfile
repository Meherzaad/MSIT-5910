FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY config ./config
RUN python src/generate_data.py && python src/evaluate.py \
    && useradd --create-home --uid 10001 appuser \
    && mkdir -p /app/state && chown -R appuser:appuser /app
ENV DATABASE_PATH=/app/state/monitor.db
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=3)"
CMD ["python", "-m", "gunicorn", "--chdir", "src", "--bind", "0.0.0.0:8000", "--workers", "1", "app:create_app()"]
