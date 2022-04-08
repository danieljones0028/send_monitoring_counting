import sys

# https://github.com/lukecyca/pyzabbix
from pyzabbix import ZabbixAPI, ZabbixAPIException

#stream = logging.StreamHandler(sys.stdout)
#stream.setLevel(logging.DEBUG)
#log = logging.getLogger('pyzabbix')
#log.addHandler(stream)
#log.setLevel(logging.DEBUG)

ZABBIX_SERVER = 
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login()

zapi.session.auth = ()
zapi.session.verify = False

zapi.timeout = 5.1
###############################################################################
template_name = 'zimbra'
application_name = 'Sender'

template = zapi.template.get(filter={"host": template_name})
template_apps = zapi.application.get(filter={"name": application_name})

if template and template_apps:
    templateid = template[0]["templateid"]
    applicationid = template_apps[0]["applicationid"]

    print(f"Found template id {templateid} and application {applicationid}")

    try:
        item = zapi.item.create(
            hostid=templateid,
            name='Teste 007',
            key_='msgsender.teste007',
            type=2, #Trapper
            value_type=3,
            applications=[applicationid]
        )
    except ZabbixAPIException as e:
        print(e)
        sys.exit()

    print(f'Added item with itemid {item["itemids"][0]} to template: {template_name} id:{templateid} in application: {application_name} id:{applicationid}')

else:
    print("template not found")
