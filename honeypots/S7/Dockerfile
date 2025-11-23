FROM python:3.10-slim
WORKDIR ${HOME}/app
RUN pip install python-snap7
COPY server.py /
CMD ["python", "/server.py"]