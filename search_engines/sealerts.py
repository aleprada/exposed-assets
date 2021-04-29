from config.config import load_file


class SEAlert:
    def __init__(self, search_engine, ip, port, country,banner):
        self.search_engine = search_engine
        self.ip = ip
        self.port = port
        self.country = country
        self.banner = banner
        self.hostname = None
        self.city = None
        self.updated = None
        self.asn = None
        self.vulnerabilities = {}
        self.timestamp = None
        self.os = None

    def add_hostname(self, hostname):
        self.hostname = hostname

    def add_city(self, city):
        self.city = city

    def add_asn(self, asn):
        self.asn = asn

    def add_vulnerability(self, cve, cvss):
        self.vulnerabilities[cve] = cvss

    def add_os(self, os):
        self.os = os

    def add_timestamp(self, timestamp):
        self.timestamp = timestamp

    def show_alert(self):
        print("\t[+] New device found on: "+self.search_engine)
        print('\t\t IP: ' + self.ip + ' port: ' + str(self.port))
        print('\t\t Device: ' + str(self.os))
        print('\t\t City: ' + str(self.city) + ' Country: ' + self.country + ' ASN: ' + str(self.asn))
        if len(self.vulnerabilities) > 0:
            for cve, cvss in self.vulnerabilities.items():
                print('\t\t [!] Vulnerability: ' + cve + ' CVSS: ' + str(cvss))


def filter_alerts_with_keywords(full_alert_list):
    alert_list =[]
    alert_keywords = load_file("alerts_keywords.txt")
    for a in full_alert_list:
        for k in alert_keywords:
            if k in a.banner:
                alert_list.append(a)
    return alert_list



#save a sqlite db with alerts. If there's match query SQLI if the alert was already saved. If not send alert.
def check_stored_alert():
    return 0
