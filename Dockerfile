FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY scripts ./scripts
RUN pip install --no-cache-dir -e .
ENTRYPOINT ["python", "-m", "mon_ultra_matrix"]
CMD ["stats"]
