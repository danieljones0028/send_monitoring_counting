from subprocess import call as getlog

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

domain = config['DEFAULT']['domain']
zabbixsender = config['DEFAULT']['zabbixsender']
zabbixserver = config['DEFAULT']['zabbixserver']
zabbixclient = config['DEFAULT']['zabbixclient']
account = 'email@domain.com.br'
sender_value = 999

def getlogs(accountlist, logpath):
    try:
        for account in accountlist:
            # Filtro para obter a quantidades de envios de uma conta.
            filterAwK = "{print $12}"
            senders = f'cat {logpath} | grep "from <{account}> " | grep smtp | grep "10025): 250" | grep "> <" | awk "{filterAwK}" | grep -o "," | wc -l'
            ########################################################

            # Transformando a saida do comando em string
            sender_value = getlog([senders], shell=True)
            ########################################################

            # Enviando direto sem gerar arquivo
            account = account.replace(domain, '')
            a = f'{zabbixsender} -z {zabbixserver} -s {zabbixclient} -k msgsender.{account} -o {sender_value}'
            print(a)
            ########################################################

    except Exception as exception_getlogs:
        print(exception_getlogs)


# Definir lista e local
getlogs(lista, local)