FROM python:3.10-slim
WORKDIR ${HOME}/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8001 102
CMD ["python", "./main.py"]