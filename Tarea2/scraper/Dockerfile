

FROM python:3.8-slim


ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY scraper/scraper.py /app/

COPY cache/ /app/cache/
COPY metrics/ /app/metrics/

RUN pip install --no-cache-dir requests pymongo elasticsearch==8.6.2 numpy

CMD ["python", "scraper.py"]
