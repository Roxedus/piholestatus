import configuration
import pihole as ph
import time
from influxdb import InfluxDBClient

def send_msg(ads_percentage_today, ads_blocked_today, dns_queries_today, domains_being_blocked, unique_domains,
             queries_forwarded, queries_cached, clients_ever_seen, unique_clients, status):
    if domains_being_blocked == "N/A":
        domains_being_blocked = 0
    else:
        pass

    json_body_querries = [
        {
            "measurement": "pihole.querries",
            "tags": {
                "host": configuration.hostname
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
                "host": configuration.hostname
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
                "host": configuration.hostname
            },
            "fields": {
                "ads_percentage_today": float(ads_percentage_today),
                "ads_blocked_today": int(ads_blocked_today)
            }
        }
    ]


    client = InfluxDBClient(configuration.influx_host, configuration.influx_port, configuration.influx_user,
                            configuration.influx_passsword, configuration.influx_database)  # InfluxDB host, InfluxDB port, Username, Password, database
    # client.create_database(influx_database) # Uncomment to create the database (expected to exist prior to feeding it data)
    client.write_points(json_body_querries)
    client.write_points(json_body_state)
    client.write_points(json_body_stats)


if __name__ == '__main__':
    while True:
        api = ph.PiHole(configuration.pihole_ip)
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

        send_msg(ads_percentage_today, ads_blocked_today, dns_queries_today, domains_being_blocked, unique_domains,
                 queries_forwarded, queries_cached, clients_ever_seen, unique_clients, status)
        time.sleep(configuration.interval)
