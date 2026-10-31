# MLOps Pipelines on AWS - demo repo

A small end-to-end ML pipeline on AWS, built using only the browser.
The model is a logistic regression on 5 features of the breast cancer dataset.
Follow the step-by-step student guide (PDF) to run it.

| What | File | Where it runs |
|---|---|---|
| Data prep, plus a "next week" file with drift | src/prepare_data.py | GitHub Actions |
| Training, MLflow logging, quality gate (f1 >= 0.85) | src/train.py | GitHub Actions and the Docker build |
| Unit tests for the API | tests/test_api.py | GitHub Actions |
| Batch scoring | src/batch_predict.py | GitHub Actions |
| Drift check (KS test) | src/drift.py | GitHub Actions |
| Build image, push to ECR, deploy to ECS | .github/workflows/deploy.yml | GitHub Actions |
| Real-time API | src/app.py + Dockerfile | ECS Express Mode |
| MLflow server | ec2_user_data.sh | EC2 t2.micro |
| Sample data | data/*.csv | upload to your S3 bucket |

## Settings you must add in your fork

Open Settings, then Secrets and variables, then Actions.

- Secret MLFLOW_TRACKING_URI = http://YOUR_EC2_PUBLIC_IP:5000
- Variable AWS_ROLE_ARN = the ARN of the github-actions-deploy role
- Variable ECS_SERVICE = the name of your ECS Express Mode service (add after you create it)

## Run on your own computer (optional)

    pip install -r requirements-dev.txt
    python -m src.prepare_data
    python -m src.train
    pytest -q
    python -m src.batch_predict
    python -m src.drift
