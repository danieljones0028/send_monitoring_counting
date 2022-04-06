from lib.sendDataToZabbix import SendDataToZabbix

import socket
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

domain = config['DEFAULT']['domain']

zabbixsender = config['DEFAULT']['zabbixsender']
zabbixserver = config['DEFAULT']['zabbixserver']
zabbixclient = config['DEFAULT']['zabbixclient']

zmprov = config['DEFAULT']['zmprov']

hostname = socket.gethostname()
current_log = '/var/log/zimbra.log'

# Staging
# homelog = '/home/daniel_jones/Documentos/Linux/Zabbix/Zimbra/logs/zimbra.log-20220405'
# pathFileAccounts = '/home/daniel_jones/Documentos/Linux/Zabbix/Zimbra/send_monitoring_counting/temp_test/listaDeContas.txt'
###############################################################################

accounts = SendDataToZabbix.getAccounts(zmprov, hostname, domain)

SendDataToZabbix.parsingsend(accounts, current_log, domain, zabbixsender, zabbixserver, zabbixclient)