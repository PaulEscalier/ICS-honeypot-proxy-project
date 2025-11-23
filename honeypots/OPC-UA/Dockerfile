FROM python:3.10-slim
WORKDIR ${HOME}/app
RUN pip install opcua 
COPY server.py /
CMD ["python", "/server.py"]