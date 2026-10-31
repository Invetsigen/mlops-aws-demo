# Stage 1: prepare data and train the model during the build.
# If the quality gate in train.py fails, the build fails and nothing is deployed.
FROM python:3.11-slim AS trainer
WORKDIR /app
COPY requirements-dev.txt requirements.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY src/ src/
RUN python -m src.prepare_data && python -m src.train

# Stage 2: small image that only serves the trained model.
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY --from=trainer /app/model/ model/
# The container listens on port 8080 (ECS Express Mode sends traffic there)
CMD exec uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8080}
