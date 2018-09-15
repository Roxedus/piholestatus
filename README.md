# piholestatus
A script to display Pi-Hole stats in Grafana via InfluxDB


To install and run the script as a service under SystemD. See: https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux

Confuguration is done in `configuration.py`, rename `configuration.example.py` and add your information.

```python
>pip3 install PiHole-api
>pip3 install influxdb
```


Dashboard Example: 
![Grafana Dashboard](http://i.imgur.com/4bitvQt.png)
