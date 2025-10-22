# Hesiod DNS
Uses [Project Hesiod](https://github.com/boconnor2017/hesiod), a Photon based approach to initiate, launch, and manage an immutable DNS Server. 

## Prerequisites
1. Deploy a [Hesiod Node](https://github.com/boconnor2017/hesiod?tab=readme-ov-file#deploy-hesiod-nodes). Run all remaining steps on this node.
2. Edit the `lab_environment.json` file with appropriate credential information for your DNS server. *Optional but recommended: save the configuration to `/usr/local/drop/ and copy when needed.*

# Quick Start
*Recommended: run these scripts as root.*
```
cd /usr/local/
```
```
git clone https://github.com/boconnor2017/hesiod-dns
```
```
cp -r hesiod/python/ hesiod-dns/hesiod
```
```
cd hesiod-dns/
```

Edit the variables in `/usr/local/hesiod-dns/json/lab_environment.json` and run:
```
python3 hesiod-dns.py
```

Login to your DNS server using a browser. Enter `http://` the IP address of the Photon machine and `:5380`. Default username is `admin`. Password is whatever you set in your json file. 

## Creating the DNS Entries
The `lab_environment.json` file contains all of the necessary information to build a DNS zone and DNS entries for your lab environment. When the json file is populated with appropriate DNS information, run the following:
```
python3 hesiod-create-domain.py
```

### Bug Fix
Run the following steps manually after the first time creating your DNS:
1. Login to Tanium at http://<tanium_ip_address>:5380 using admin and password from `lab_environment.json`
2. Click the `Zones` tab and click the zone from `lab_environment.json`
3. Click `Add Record`
    * Name: `@` (default)
    * Type: `A` (default)
    * TTL : `3600` (default)
    * IPv4 Address: `<enter the tanium ip address>`
    * Add Reverse (PTR) record: `yes`
    * Create reverse zone for PTR record: `yes`
    * Overwrite existing records: `yes` (optional but recommended)
    * Comments: `bug fix`
4. Click `Save`
