import requests
import csv
import subprocess

# Fonte: Abuse CH
url = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"
response = requests.get(url).text

# Limpar regras de firewall existentes
subprocess.run(["iptables", "-F"])

# Processar os dados do CSV e adicionar regras de firewall
csv_lines = response.splitlines()
csv_reader = csv.reader(filter(lambda x: not x.startswith("#"), csv_lines))
for row in csv_reader:
    # A segunda coluna (índice 1) contém o endereço IP
    ip = row[1]
    
    # Verificar se o IP não é o cabeçalho
    if ip != "dst_ip":
        print("Regra adicionada para bloquear:", ip)

        # Adicionar regra de saída
        add_rule_out = ["iptables", "-A", "OUTPUT", "-d", ip, "-j", "DROP"]
        subprocess.run(add_rule_out)

        # Adicionar regra de entrada
        add_rule_in = ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
        subprocess.run(add_rule_in)
