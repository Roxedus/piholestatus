import sys
import os
from collections import namedtuple
import configuration
import pihole as ph
import time
from influxdb import InfluxDBClient


def get_settings():
    pi = namedtuple('settings',
                    'hostname pihole_ip influx_host influx_port influx_user '
                    'influx_passsword influx_database interval do_loop')
    hostname = os.getenv('host-name', configuration.hostname)
    pihole_ip = os.getenv('pihole_ip', configuration.pihole_ip)
    influx_host = os.getenv('influx_host', configuration.influx_host)
    influx_port = os.getenv('influx_port', configuration.influx_port)
    influx_user = os.getenv('influx_user', configuration.influx_user)
    influx_passsword = os.getenv('influx_passsword', configuration.influx_passsword)
    influx_database = os.getenv('influx_database', configuration.influx_database)
    interval = os.getenv('interval', configuration.interval)
    do_loop = os.getenv('do_loop', configuration.do_loop)
    if "-manual" in sys.argv:
        do_loop = False
    conf = pi(hostname, pihole_ip, influx_host, influx_port, influx_user, influx_passsword, influx_database,
              interval, do_loop)
    return conf


def send_msg(settings, client, ads_percentage_today, ads_blocked_today, dns_queries_today, domains_being_blocked, unique_domains,
             queries_forwarded, queries_cached, clients_ever_seen, unique_clients, status):
    if domains_being_blocked == "N/A":
        domains_being_blocked = 0
    else:
        pass

    json_body_querries = [
        {
            "measurement": "pihole.querries",
            "tags": {
                "host": settings.hostname
            },
            "fields": {
                "dns_queries_today": int(dns_queries_today),
                "unique_domains": int(unique_domains),
                "queries_forwarded": int(queries_forwarded),
                "queries_cached": int(queries_cached)
            }
        }
    ]

    json_body_state = [
        {
            "measurement": "pihole.state",
            "tags": {
                "host": settings.hostname
            },
            "fields": {
                "domains_being_blocked": int(domains_being_blocked),
                "clients_ever_seen": int(clients_ever_seen),
                "unique_clients": int(unique_clients),
                "status": str(status)
            }
        }
    ]

    json_body_stats = [
        {
            "measurement": "pihole.stats",
            "tags": {
                "host": settings.hostname
            },
            "fields": {
                "ads_percentage_today": float(ads_percentage_today),
                "ads_blocked_today": int(ads_blocked_today)
            }
        }
    ]


    #client.create_database(configuration.influx_database)
    client.write_points(json_body_querries)
    client.write_points(json_body_state)
    client.write_points(json_body_stats)


def run_script(settings, client):
    api = ph.PiHole(settings.pihole_ip)
    api.refresh()
    domains_being_blocked = api.domain_count.replace(",", "")
    dns_queries_today = api.queries.replace(",", "")
    ads_percentage_today = api.ads_percentage
    ads_blocked_today = api.blocked.replace(",", "")
    unique_domains = api.unique_domains.replace(",", "")
    queries_forwarded = api.forwarded.replace(",", "")
    queries_cached = api.cached.replace(",", "")
    clients_ever_seen = api.total_clients.replace(",", "")
    unique_clients = api.unique_clients.replace(",", "")
    status = api.status.capitalize()

    send_msg(settings, client, ads_percentage_today, ads_blocked_today, dns_queries_today, domains_being_blocked,
             unique_domains, queries_forwarded, queries_cached, clients_ever_seen, unique_clients, status)


if __name__ == '__main__':
    settings = get_settings()
    client = InfluxDBClient(settings.influx_host, settings.influx_port, settings.influx_user,
                            settings.influx_passsword, settings.influx_database)
    if settings.do_loop is True:
        print("Loop On")
        while settings.do_loop is True:
            run_script(settings, client)
            time.sleep(settings.interval)
    if settings.do_loop is not True:
        print("Loop Off")
        run_script(settings, client)
