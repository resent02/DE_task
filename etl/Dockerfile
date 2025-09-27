FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends cron bash procps && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY cronfile /etc/cron.d/app
RUN chmod 0644 /etc/cron.d/app

RUN touch /var/log/cron.log

CMD ["cron","-f"]
