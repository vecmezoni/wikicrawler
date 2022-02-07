FROM python:3.10-alpine
RUN apk add gcc openssl-dev libffi-dev musl-dev libxml2-dev libxslt-dev postgresql-dev python3-dev
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY main.py ./main.py
ENTRYPOINT ["python", "main.py"]
