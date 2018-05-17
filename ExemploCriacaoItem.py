# Fonte
# https://github.com/lukecyca/pyzabbix
from pyzabbix import ZabbixAPI, ZabbixAPIException
import sys
import logging

#stream = logging.StreamHandler(sys.stdout)
#stream.setLevel(logging.DEBUG)
#log = logging.getLogger('pyzabbix')
#log.addHandler(stream)
#log.setLevel(logging.DEBUG)

# Login (in case of HTTP Auth, only the username is needed, the password, if passed, will be ignored)
# The hostname at which the Zabbix web interface is available
ZABBIX_SERVER = "http://172.16.241.101/zabbix"
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login("Admin", "zabbix")

# Enable HTTP auth
zapi.session.auth = ("Admin", "zabbix")

# Disable SSL certificate verification
zapi.session.verify = False

# Specify a timeout (in seconds)
zapi.timeout = 5.1

# Use zbx-api_getHostid.py para obter o hostid
host_name = 'zimbra'

hosts = zapi.host.get(filter={"host": host_name}, selectInterfaces=["interfaceid"])

if hosts:
    host_id = hosts[0]["hostid"]
    print("Found host id {0}".format(host_id))

    try:
        item = zapi.item.create(
            hostid=host_id,
            name='danieljones',
            key_='mail.danieljones',
            type=2, #Trapper
            value_type=3,
            interfaceid=hosts[0]["interfaces"][0]["interfaceid"],
            delay=30
        )
    except ZabbixAPIException as e:
        print(e)
        sys.exit()
    print("Added item with itemid {0} to host: {1}".format(item["itemids"][0], host_name))
else:
    print("No hosts found")
