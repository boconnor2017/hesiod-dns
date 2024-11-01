# Description: Builds Tanium DNS Server using Photon OS
# Author: Brendan O'Connor
# Date: August 2024
# Version: 4.0

# Base imports
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
import os
import stat 
import shutil
import urllib
import requests

'''
This script needs to run on the Photon OS vm that is going to be the dedicated DNS server.
00. Prerequisites: run the quick start https://github.com/boconnor2017/hesiod-vcf5 

Workflow:
01. Configure Tanium Prerequisites  
    02a. Run configure-tanium-ip-tables.sh script
        iptables -A INPUT -i eth0 -p udp --dport 53 -j ACCEPT
        iptables-save >/etc/systemd/scripts/ip4save
        iptables -L
        systemctl disable systemd-resolved.service
        systemctl stop systemd-resolved
    02b. Run run-docker-compose 
        curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        docker-compose --version
        mv /usr/local/e2e-patterns/dns/docker-compose.yml $HOME
        docker-compose up -d
02. Install Tanium
03. Change Default Password
    04a. Get Token using admin/admin 
    04b. Change password 
    04c. Get Token using permanent password 
'''
# General
def append_text_to_file(text, file_name):
    new_file = open(file_name, "a")
    new_file.writelines(text)
    new_file.close()

def get_ip_address(interface):
    # Syntax of interface: eth0
    ip = ni.ifaddresses('eth0')[AF_INET][0]['addr']
    return ip

def run_cmd_on_os(cmd):
    cmd_returned_value = os.system(cmd)
    return cmd_returned_value

# Configure Tanium Prerequisites
def configure_tanium_prerequisites():
    config_tanium_cmds = []
    config_tanium_cmds.append("iptables -A INPUT -i eth0 -p udp --dport 53 -j ACCEPT")
    config_tanium_cmds.append("iptables-save >/etc/systemd/scripts/ip4save")
    config_tanium_cmds.append("iptables -L")
    config_tanium_cmds.append("systemctl disable systemd-resolved.service")
    config_tanium_cmds.append("systemctl stop systemd-resolved")
    for x in config_tanium_cmds:
        cmd_returned_value = run_cmd_on_os(x)
        return cmd_returned_value

def configure_os_name_resolution(ip):
    file_text = "nameserver "+ip
    append_text_to_file(file_text, "resolv.conf")
    run_cmd_on_os("cp resolv.conf /etc/resolv.conf")
    run_cmd_on_os("rm resolv.conf")

def install_tanium():
    download_docker_compose = run_cmd_on_os("curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose")
    os.chmod("/usr/local/bin/docker-compose", stat.S_IEXEC)
    shutil.copy("lib/dns-deploy-docker-config/docker-compose.yaml", os.getcwd())
    run_cmd_on_os("systemctl stop systemd-resolved") #Reserves port 53 for some reason
    config_tanium_cmd = run_cmd_on_os("docker-compose up -d")
    return config_tanium_cmd

# Change Tanium default password
def get_tanium_token(username, password, ip):
    api_url = "http://"+ip+":5380"+"/api/user/login?user="+username+"&pass="+password+"&includeInfo=true"
    api_response = requests.get(api_url)
    tanium_token = (api_response.json()['token'])
    return tanium_token

def change_tanium_password(token, ip, new_password):
    api_url = "http://"+ip+":5380"+"/api/user/changePassword?token="+token+"&pass="+new_password
    api_response = requests.get(api_url)
    return api_response

# Create DNS Zone
def create_dns_zone(tanium_token, dns_ip, zone_name):
    api_url = "http://"+dns_ip+":5380/api/zones/create?token="+tanium_token+"&zone="+zone_name+"&type=Primary"
    api_response = requests.get(api_url)
    return api_response

# Create DNS Record
def createdns_record(tanium_token, dns_ip, dns_record, dns_zone, ip_address, dns_type, dns_ttl, dns_overwrite, dns_ptr, dns_create_ptr_zone):
    api_url = "http://"+dns_ip+":5380/api/zones/records/add?"
    api_url = api_url+"token="+tanium_token
    api_url = api_url+"&domain="+dns_record+"."+dns_zone
    api_url = api_url+"&zone="+dns_zone
    api_url = api_url+"&type="+dns_type
    api_url = api_url+"&ttl="+dns_ttl
    api_url = api_url+"&overwrite="+dns_overwrite
    api_url = api_url+"&ipAddress="+ip_address
    api_url = api_url+"&ptr="+dns_ptr
    api_url = api_url+"&createPtrZone="+dns_create_ptr_zone
    api_response = requests.get(api_url)
    return api_response