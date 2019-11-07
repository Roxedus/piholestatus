# piholestatus
A script to display Pi-Hole stats in Grafana via InfluxDB


To install and run the script as a service under SystemD. See: https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux

<details>
    <summary>Native</summary>
    
```bash
git clone https://github.com/Roxedus/piholestatus piholestatus
python -m pip install -r /piholestatus/requirements.txt
cp configuration.example.py configuration.py
```
 
</details>



<details>
  <summary>Docker</summary>
  
Example docker-compose.yml

The listed environment variables is the default

```yml
  piholestats:     
    container_name: piholestats
    image: roxedus/piholestats:latest
    networks:
      - internal
    enviroment:
      - host-name=PiHole
      - pihole_ip=pihole
      - influx_host=influxdb
      - influx_port=8086
      - influx_user=""
      - influx_password=""
      - influx_database=PiHole
      - interval=60
      - do_loop=True
```
  
</details>


Dashboard Example: 
![Grafana Dashboard](http://i.imgur.com/4bitvQt.png)
