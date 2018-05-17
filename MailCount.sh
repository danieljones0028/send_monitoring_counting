#!/bin/bash
#ZCS 8.6
zmp="/opt/zimbra/bin/zmprov"
srv="ip_zabbix_proxy_ou_server"
hostname=`hostname` # Deve ser igual ao system.hostname no zabbix-agent

if [ -e /tmp/contas.txt ]; then
	rm /tmp/contas.txt
	rm /tmp/conta.txt
	rm /opt/zabbix/Senders/acc
	rm /opt/zabbix/Senders/env
	rm /opt/zabbix/Senders/acc-pronta
	rm /opt/zabbix/Senders/coleta_enviados
	$zmp -l gaa >> /tmp/contas.txt
	sort /tmp/contas.txt >> /tmp/conta.txt
else
	$zmp -l gaa >> /tmp/contas.txt
	rm /opt/zabbix/Senders/acc
    rm /opt/zabbix/Senders/env
	rm /opt/zabbix/Senders/acc-pronta
	rm /opt/zabbix/Senders/coleta_enviados
	sort /tmp/contas.txt >> /tmp/conta.txt
fi

for account in `cat /tmp/conta.txt`; do

	enviados=$(cat /var/log/zimbra.log | grep "from <$account> " | grep smtp | grep "10025): 250" | grep "> <" | awk '{print $12}' | grep -o "," | wc -l)

	echo $enviados >> /opt/zabbix/Senders/env
	echo $account >> /opt/zabbix/Senders/acc
done

# Resolve problema de varias contas de admin@domain
sed 's/admin@zimbra/admin2@zimbra/' -i /opt/zabbix/Senders/acc

awk -F"@" '{print $1}' /opt/zabbix/Senders/acc > /opt/zabbix/Senders/acc-pronta
sed 's/^/mail./' -i /opt/zabbix/Senders/acc-pronta

cd /opt/zabbix/Senders

paste -d " " acc-pronta env >> /opt/zabbix/Senders/coleta_enviados
sed "s/^/$hostname /g" -i /opt/zabbix/Senders/coleta_enviados

chown -R zabbix. /opt/zabbix/Senders

cd /opt/zabbix/Senders/

zabbix_sender -z $srv -i coleta_enviados

exit
