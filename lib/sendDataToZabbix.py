from os import popen as pp
from os import path
from subprocess import check_call

class SendDataToZabbix:

    def parsingsend(accountlist, logpath, domain, zabbixsender, zabbixserver, zabbixclient):
        try:
            for account in accountlist:
                # Filtro para obter a quantidades de envios de uma conta.
                filterAwK = "{print $12}"
                senders = f'cat {logpath} | grep "from <{account}> " | grep smtp | grep "10025): 250" | grep "> <" | awk "{filterAwK}" | grep -o "," | wc -l'
                ########################################################

                # Transformando a saida do comando em string
                sender_value = check_call([senders], shell=True,)
                # sender_value = pp(senders).read()
                ########################################################

                # Enviando direto sem gerar arquivo
                account = account.replace(domain, '')
                a = f'{zabbixsender} -z {zabbixserver} -s {zabbixclient} -k msgsender.{account} -o {sender_value}'
                print(a)
                ########################################################

        except Exception as exception_getlogs:
            print(exception_getlogs)


    def getAccounts(command, hostname, domain):
        try:
            if path.exists(command):
                # getAllAccounts(gaa) [-v] [-e] [-s server] [{domain}]
                # -- NOTE: getAllAccounts can only be used with "zmprov -l/--ldap"
                accounts = pp(f'{command} -l gaa -s {hostname} {domain}').read().splitlines()

                return accounts

        except Exception as accounts_error:
            print(accounts_error)
