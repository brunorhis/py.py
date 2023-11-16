import requests
import csv
import subprocess

# Fonte: Abuse CH
url = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"
response = requests.get(url).text

# Deleta a regra de firewall existente
delete_rule = "netsh advfirewall firewall delete rule name='BadIP'"
subprocess.run(["Powershell", "-Command", delete_rule])

# Adiciona regras de firewall
csv_lines = response.splitlines()
csv_reader = csv.reader(filter(lambda x: not x.startswith("#"), csv_lines))
for row in csv_reader:
    # A segunda coluna (índice 1) contém o endereço IP
    ip = row[1]

    # Verifica se o IP não é o cabeçalho
    if ip != "dst_ip":
        print("Regra adicionada para bloquear:", ip)

        # Adiciona regra de saída
        add_rule_out = f"netsh advfirewall firewall add rule name='BadIP_Out' dir=out action=block remoteip={ip}"
        subprocess.run(["Powershell", "-Command", add_rule_out])

        # Adiciona regra de entrada
        add_rule_in = f"netsh advfirewall firewall add rule name='BadIP_In' dir=in action=block remoteip={ip}"
        subprocess.run(["Powershell", "-Command", add_rule_in])
