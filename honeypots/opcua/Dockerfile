FROM python:3.10-slim
WORKDIR ${HOME}/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8003 4840
CMD ["python", "./main.py"]