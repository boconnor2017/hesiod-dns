# Hesiod DNS
Uses [Project Hesiod](https://github.com/boconnor2017/hesiod), a Photon based approach to initiate, launch, and manage an immutable DNS Server. 

## Prerequisites
Edit the `lab_environment.json` file with appropriate credential information for your DNS server.

# Quick Start
Deploy Photon OS OVA to the physical server. Follow the steps in the [Hesiod Photon OS Quick Start](https://github.com/boconnor2017/hesiod/blob/main/photon/readme.md) readme file to prep the Photon server for VCF. 

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