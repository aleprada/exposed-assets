from config.config import load_file, save_alert_db, check_saved_threats


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
        self.app = None

    def add_hostname(self, hostname):
        self.hostname = hostname

    def add_city(self, city):
        self.city = city

    def add_asn(self, asn):
        self.asn = asn

    def add_vulnerability(self, cve, cvss):
        self.vulnerabilities[cve] = cvss

    def add_app(self, app):
        self.app = app

    def add_timestamp(self, timestamp):
        self.timestamp = timestamp

    def show_alert(self):
        print("\t[+] New device found on: "+self.search_engine)
        print('\t\t IP: ' + self.ip + ' port: ' + str(self.port))
        print('\t\t Device: ' + str(self.app))
        print('\t\t City: ' + str(self.city) + ' Country: ' + self.country + ' ASN: ' + str(self.asn))
        if len(self.vulnerabilities) > 0:
            for cve, cvss in self.vulnerabilities.items():
                print('\t\t [!] Vulnerability: ' + cve + ' CVSS: ' + str(cvss))


def filter_alerts_with_keywords(full_alert_list):
    alert_list = []
    alert_keywords = load_file("alerts_keywords_prod.txt")
    for a in full_alert_list:
        already_stored = check_saved_threats(a.ip, a.port, a.timestamp)
        if already_stored is True:
            continue
        else:
            for k in alert_keywords:
                if k in a.banner:
                    alert_list.append(a)
                    save_alert_db(a.timestamp, a.ip, a.port, a.country)
    return alert_list

