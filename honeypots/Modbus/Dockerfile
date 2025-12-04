FROM python:3.10-slim
WORKDIR ${HOME}/app
RUN pip install pymodbus asyncio typing
COPY server.py /
COPY helper.py /
CMD ["python", "/server.py"]