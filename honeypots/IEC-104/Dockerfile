FROM python:3.10-slim
WORKDIR ${HOME}/app
RUN pip install c104
COPY server.py /
CMD ["python", "/server.py"]