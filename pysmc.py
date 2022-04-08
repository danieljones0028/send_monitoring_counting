from lib.sendDataToZabbix import SendDataToZabbix

import socket
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

domain = config['DEFAULT']['domain']

zabbixsender = config['DEFAULT']['zabbixsender']
zabbixserver = config['DEFAULT']['zabbixserver']
zabbixclient = config['DEFAULT']['zabbixclient']

zabbix_server_url       =   config['DEFAULT']['zabbix_server_url']
zabbix_user             =   config['DEFAULT']['zabbix_user']
zabbix_user_password    =   config['DEFAULT']['zabbix_user_password']
zabbix_session_verify   =   config['DEFAULT']['zabbix_session_verify']
zabbix_timeout          =   config['DEFAULT']['zabbix_timeout']
zabbix_template_name    =   config['DEFAULT']['zabbix_template_name']
zabbix_application_name =   config['DEFAULT']['zabbix_application_name']



zmprov = config['DEFAULT']['zmprov']

hostname = socket.gethostname()
current_log = '/var/log/zimbra.log'

# Staging
# homelog = '/home/daniel_jones/Documentos/Linux/Zabbix/Zimbra/logs/zimbra.log-20220405'
# pathFileAccounts = '/home/daniel_jones/Documentos/Linux/Zabbix/Zimbra/send_monitoring_counting/temp_test/listaDeContas.txt'
###############################################################################

# TODO incluir log e criacao automatica de item no zabbix

accounts = SendDataToZabbix.getAccounts(zmprov, hostname, domain)
SendDataToZabbix.Testeitem(zabbix_server_url, zabbix_user, zabbix_user_password, zabbix_session_verify, zabbix_timeout, zabbix_template_name, zabbix_application_name, 'Maluco', 'Doido')
SendDataToZabbix.parsingsend(accounts, current_log, domain, zabbixsender, zabbixserver, zabbixclient)