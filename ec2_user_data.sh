#!/bin/bash
# Paste this into "User data" when you launch the EC2 instance.
# It installs MLflow and runs it on port 5000 as a service, so it also starts again after a reboot.
if [ ! -f /swapfile ]; then
  fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile
  echo '/swapfile swap swap defaults 0 0' >> /etc/fstab
fi
swapon /swapfile 2>/dev/null
python3 -m venv /opt/mlenv
/opt/mlenv/bin/pip install mlflow==2.19.0 sqlalchemy==2.0.36 boto3
TOKEN=$(curl -s -X PUT http://169.254.169.254/latest/api/token -H "X-aws-ec2-metadata-token-ttl-seconds: 300")
ACCOUNT=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/dynamic/instance-identity/document | python3 -c "import sys, json; print(json.load(sys.stdin)['accountId'])")
cat > /etc/systemd/system/mlflow.service <<UNIT
[Unit]
Description=MLflow tracking server
After=network-online.target

[Service]
Environment=AWS_DEFAULT_REGION=us-east-1
ExecStart=/opt/mlenv/bin/mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:////opt/mlflow.db --serve-artifacts --artifacts-destination s3://mlops-demo-$ACCOUNT/mlflow-artifacts
Restart=always

[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now mlflow
