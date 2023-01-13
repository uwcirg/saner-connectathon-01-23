# pyarrow doesn't support python 3.11 yet
# https://github.com/apache/arrow/pull/14499
FROM python:3.10

WORKDIR /opt/app

COPY . .
RUN pip install --requirement requirements.txt

ENTRYPOINT ["python3"]
