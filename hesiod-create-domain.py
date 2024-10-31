# Import Hesiod libraries
from hesiod import lib_general as libgen
from hesiod import lib_json as libjson
from hesiod import lib_logs_and_headers as liblog 
from hesiod import lib_paramiko as libpko 

# Import DNS libraries
from lib import deploy_dns as dnslib

# Import Standard Python libraries
import os
import sys

# Import json configuration parameters
env_json_str = libjson.populate_var_from_json_file("json", "lab_environment.json")
env_json_py = libjson.load_json_variable(env_json_str)
this_script_name = os.path.basename(__file__)
logfile_name = env_json_py["logs"][this_script_name]

# Hesiod Header and Log init
liblog.hesiod_print_header()
liblog.hesiod_log_header(logfile_name)
err = "Successfully imported Hesiod python libraries."
liblog.write_to_logs(err, logfile_name)
err = "Succesfully initialized logs to "+logfile_name
liblog.write_to_logs(err, logfile_name)
err = ""
liblog.write_to_logs(err, logfile_name)

# Create DNS Zone
tanium_token = dnslib.get_tanium_token("admin", env_json_py["universal_authentication"]["universal_password"], env_json_py["dns_ip_address"])
dns_zone = dnslib.create_dns_zone(tanium_token,  env_json_py["dns_ip_address"], env_json_py["dns_zone"])

# Create DNS Records
i=0
while i < len(env_json_py["dns_entries"]):
    dns_record = dnslib.createdns_record(tanium_token,  env_json_py["dns_ip_address"], env_json_py["dns_entries"][i]["domain_name"], env_json_py["dns_zone"], env_json_py["dns_entries"][i]["ip_address"], env_json_py["dns_entries"][i]["type"], env_json_py["dns_entries"][i]["ttl"], env_json_py["dns_entries"][i]["overwrite"], env_json_py["dns_entries"][i]["ptr"], env_json_py["dns_entries"][i]["create_pointer_zone"])
    i=i+1