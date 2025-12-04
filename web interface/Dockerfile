FROM python:3.10-slim
WORKDIR ${HOME}/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "script.py"]
