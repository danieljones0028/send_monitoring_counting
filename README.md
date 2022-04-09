# Enviando Contagem de Monitoramento

#### Obtenha o número de envios de contas por domínio (interno) do Zimbra.

Os testes foram feitos em cima do Zimbra 8.8.15 mas acredito que deve funcionar a partir do 8.7 e posteriores

##### Operação
* Obtém a lista de contas de um domínio, e desta lista é feita uma verificação no arquivo /var/log/zimbra.log onde é obtido o número de envios por conta.
* Quando esses dados são obtidos, eles são enviados para o servidor Zabbix server ou proxy que monitora o host Zimbra.

#### Problemas
1. Digite ARGV para chamar @domínio. O arquivo de configuração está sendo lido para isso no momento.
2. Digite o ARGV para chamar versões do Zimbra. O arquivo de configuração está sendo lido para isso no momento.
3. Inserir logs.