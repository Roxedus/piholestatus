FROM python:3.7-alpine3.10

LABEL maintainer="Roxedus"

ENV host-name=PiHole \
    pihole_ip=pihole \
    influx_host=influxdb \
    influx_port=8086 \
    influx_user="" \
    influx_password="" \
    influx_database=PiHole \
    interval=60 \
    do_loop=True

COPY / /app

RUN python3 -m pip install -r /app/requirements.txt

WORKDIR /app

CMD python3 /app/Collector.py