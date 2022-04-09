import sys
from os import path
from os import popen as pp
from subprocess import Popen
# https://github.com/lukecyca/pyzabbix
from pyzabbix import ZabbixAPI, ZabbixAPIException

class SendDataToZabbix:

    def parsingsend(accountlist, logpath, domain, zabbixsender, zabbixserver, zabbixclient):
        try:
            for account in accountlist:
                # Filtro para obter a quantidades de envios de uma conta.
                filterAwK = "'{print $12}'"
                senders = f'cat {logpath} | grep "from <{account}> " | grep smtp | grep "10025): 250" | grep "> <" | awk {filterAwK} | grep -o "," | wc -l'
                ########################################################

                # Transformando a saida do comando em string
                sender_value = pp(senders).read()
                ########################################################

                # Enviando direto sem gerar arquivo
                account = account.replace(domain, '')
                send = f'{zabbixsender} -z {zabbixserver} -s "{zabbixclient}" -k msgsender.{account} -o {int(sender_value)}'
                Popen([send], shell=True)
                ########################################################

        except Exception as exception_getlogs:
            print(exception_getlogs)


    def getAccounts(command, hostname, domain):
        try:
            if path.exists(command):
                # getAllAccounts(gaa) [-v] [-e] [-s server] [{domain}]
                # -- NOTE: getAllAccounts can only be used with "zmprov -l/--ldap"
                accounts = pp(f'{command} -l gaa -s {hostname} {domain.replace("@", "")}').read().splitlines()

                return accounts

        except Exception as accounts_error:
            print(accounts_error)

    def createItem(zabbix_server_url, zabbix_user, zabbix_user_password, zabbix_session_verify, zabbix_timeout, zabbix_template, zabbix_application, zabbix_item_name, zabbix_key_name):

        zapi = ZabbixAPI(zabbix_server_url)
        zapi.login(zabbix_user, zabbix_user_password)
        zapi.session.auth = (zabbix_user, zabbix_user_password)
        zapi.session.verify = zabbix_session_verify
        zapi.timeout = zabbix_timeout
        template_name = zabbix_template
        application_name = zabbix_application

        template = zapi.template.get(filter={"host": template_name})
        template_apps = zapi.application.get(filter={"name": application_name})

        if template and template_apps:
            templateid = template[0]["templateid"]
            applicationid = template_apps[0]["applicationid"]

            print(f"Found template id {templateid} and application {applicationid}")

            try:
                item = zapi.item.create(
                    hostid=templateid,
                    name=zabbix_item_name,
                    key_=zabbix_key_name,
                    type=2,
                    value_type=3,
                    applications=[applicationid]
                )
            except ZabbixAPIException as e:
                print(e)
                sys.exit()

            print(f'Added item with itemid {item["itemids"][0]} to template: {template_name} id:{templateid} in application: {application_name} id:{applicationid}')

        else:
            print("template not found")
