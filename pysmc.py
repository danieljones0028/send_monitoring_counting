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

# TODO incluir log e criacao automatica de item no zabbix

try:
    accounts = SendDataToZabbix.getAccounts(zmprov, hostname, domain)
except Exception as e:
    print(e)

try:
    for account in accounts:
        account = account.replace(domain, '')
        SendDataToZabbix.createItem(zabbix_server_url, zabbix_user, zabbix_user_password, zabbix_session_verify, zabbix_timeout, zabbix_template_name, zabbix_application_name, f'{account}{domain}', f'msgsender.{account}')
except Exception as e:
    print(e)

try:
    SendDataToZabbix.parsingsend(accounts, current_log, domain, zabbixsender, zabbixserver, zabbixclient)
except Exception as e:
    print(e)
