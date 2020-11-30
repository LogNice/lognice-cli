FROM python:3.8.6-slim
WORKDIR /usr/src/app
COPY src/requirements.txt /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt
COPY src/* /usr/src/app
ENTRYPOINT ["python", "/usr/src/app/app.py"]
