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

# Local functions
def deploy_dns():
    print("Deploying Tanium DNS Server.")
    err = "    configure_tanium_prerequisites(): "
    liblog.write_to_logs(err, logfile_name)
    cmd_returned_value = dnslib.configure_tanium_prerequisites()
    err = "    cmd_returned_value: "+str(cmd_returned_value)
    liblog.write_to_logs(err, logfile_name)
    libgen.pause_python_for_duration(5)
    err = "    configure_os_name_resolution(ip): "
    liblog.write_to_logs(err, logfile_name)
    dnslib.configure_os_name_resolution("8.8.8.8")
    libgen.pause_python_for_duration(5)
    err = "    install_tanium(): "
    liblog.write_to_logs(err, logfile_name)
    cmd_returned_value = dnslib.install_tanium()
    err = "    cmd_returned_value: "+str(cmd_returned_value)
    liblog.write_to_logs(err, logfile_name)
    libgen.pause_python_for_duration(60)
    err = "    get_ip_address(): "
    liblog.write_to_logs(err, logfile_name)
    ip = dnslib.get_ip_address("eth0")
    err = "    ip address of DNS Server: "+ip
    liblog.write_to_logs(err, logfile_name)
    err = "    get_tanium_token(): "
    liblog.write_to_logs(err, logfile_name)
    token = dnslib.get_tanium_token("admin", "admin", ip)
    err = "    token: "+token
    liblog.write_to_logs(err, logfile_name)
    err = "    change_tanium_password(): "
    liblog.write_to_logs(err, logfile_name)
    dnslib.change_tanium_password(token, ip, env_json_py["universal_authentication"]["universal_password"])
    sys.exit()

deploy_dns()