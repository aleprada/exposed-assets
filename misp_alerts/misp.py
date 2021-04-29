from pymisp import PyMISP,MISPEvent, PyMISPError, MISPObject
from config.config import config_parser
from search_engines.sealerts import SEAlert


def misp_connection(url, misp_key, proxy_usage):
    try:
        if proxy_usage:
            proxies = {}
            proxies ["http"] = config_parser("misp","http")
            proxies ["https"] = config_parser("misp","https")
            misp = PyMISP(url, misp_key, False, 'json', proxies=proxies)
        else:
            misp = PyMISP(url, misp_key, False, 'json',None)
    except PyMISPError:
        print("\t [!] Error connecting to MISP instance. Check if your MISP instance it's up!")
        return None

    return misp


def create_event(misp):
    event = MISPEvent()
    event.distribution = 0
    event.threat_level_id = 1
    event.analysis = 0
    return event


def create_vulnerabilities_objs(vuln_list):
    vuln_obj_list = []
    for vuln, cvss in vuln_list.items():
        vulnerability_object = MISPObject('vulnerability')
        vulnerability_object.add_attribute("cvss-score", cvss)
        vulnerability_object.add_attribute("id", vuln)
        vuln_obj_list.append(vulnerability_object)
    return vuln_obj_list


def save_exposed_assets(sealerts, proxy_usage):
    misp = misp_connection(config_parser("misp","url"),config_parser("misp", "api_key"), proxy_usage)
    for asset in sealerts:
        event = create_event(misp)
        event.add_tag("circl:incident-classification=\"vulnerability\"")
        event.info = "[Exposed Asset] New potential rail asset exposed"
        event.add_attribute('ip-dst', asset.ip)
        event.add_attribute('port', asset.port)
        event.add_attribute('other', asset.country)
        event.add_attribute('other', asset.banner)
        if asset.asn is not None:
            event.add_attribute('other', asset.asn)
        if len(asset.vulnerabilities)>0:
            vulns_objs_list = create_vulnerabilities_objs(asset.vulnerabilities)
            for v in vulns_objs_list:
                event.add_object(v)
        event = misp.add_event(event, pythonify=True)
        print("\t [*] Event with ID "+str(event.id) + " has been successfully stored.")
