# filtering/Dockerfile

FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY filtering/filter.py /app/

RUN pip install --no-cache-dir pymongo

# El comando que genera clean_incidents.csv en /data
CMD ["python", "filter.py"]