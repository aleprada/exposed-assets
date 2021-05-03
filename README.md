**Exposed assets**  
![Build Status](https://travis-ci.com/aleprada/exposed-assets.svg?branch=main)

This tool allows you to gather IT/OT exposed assets for Threat Intelligence analysis. The tool
uses the official Python [Shodan](https://github.com/achillean/shodan-python) and [ZoomEye](https://github.com/knownsec/ZoomEye-python) libraries.

The usage of the tool is very simple. The tool needs a list of dorks (located at config
->config_files->dorks.txt) that will use for searching in both search engines. In this case,
the dorks provided are focused on ICS/SCADA and CCTV/IP-Cameras as well as other IT devices that might be used by
adversaries at early stages of the [kill-chain](https://en.wikipedia.org/wiki/Kill_chain), such as RDPs or VNCs.

After gathering the results from the different search engines, the tool has the functionality
of correlating(-a) the banner of each host with a list of keywords (config->config_files->alerts_keywords). In case of 
a match, the alerts can be **shown on the screen (-v)** and/or **sent to a MISP instance(-m)**.

**Usage**

Looking for IT/OT exposed assets.
```bash 
python main.py -v
```
Output
``` bash
[*] Gathering IT/OT exposed assets
	[*] Searching: hostname:rail
	[+] New device found.
		 IP: 158.XXX.XXX.XX port: 443
		 Device: None
		 City: Cambridge Country: United States ASN: AS46XXX
	[+] New device found.
		 IP: 157.XXX.XXX.XX port: 80
		 Device: None
		 City: London Country: United Kingdom ASN: AS21XXX
[*] Number of IT/OT exposed assets discovered: 2

```

Looking for **relevant IT/OT exposed assets**. This option **correlates results with a keyword list**.
```bash 
python main.py -a 
```

Output
``` bash
[*] Gathering IT/OT exposed assets
	[*] Searching: hostname:rail
[*] Checking if IT/OT assets gathered contain any keyword of your list.
[*] Number of IT/OT exposed assets discovered: 5
```

Looking for **relevant IT/OT exposed assets and showing the output**. This option **correlates results with a keyword 
list**.
```bash 
python main.py -a -v
```

Output
``` bash
[*] Gathering IT/OT exposed assets
	[*] Searching: hostname:rail
[*] Checking if IT/OT assets gathered contain any keyword of your list.
	[+] New device found.
		 IP: 158.XXX.XXX.XX port: 443
		 Device: None
		 City: Cambridge Country: United States ASN: AS46XXX
[*] Number of IT/OT exposed assets discovered: 1
```

Looking for **relevant IT/OT exposed assets and sending them to MISP**. This option **correlates results with a 
keyword list**. Type also **--proxy(-p)** for using a proxy to send the alerts to MISP.
```bash 
python main.py -a -m -v
```
Output
```bash
[*] Gathering IT/OT exposed assets
	[*] Searching: hostname:rail
[*] Checking if IT/OT assets gathered contain any keyword of your list.
	[+] New device found.
		 IP: 158.XXX.XXX.XX port: 443
		 Device: None
		 City: Cambridge Country: United States ASN: AS46XXX
[*] Sending alerts to MISP
	 [*] Event with ID 1654 has been successfully stored.
[*] Number of IT/OT exposed assets discovered: 1
```

**ToDo List**
* Publish a list of Dorks related to ICS/SCADA Cameras.
* Detect vulnerabilities (CVE) in ZoomEye.
* Add other search engines (e.g. Censys)