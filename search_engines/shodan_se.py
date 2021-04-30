import shodan
from config.config import config_parser
from search_engines.sealerts import SEAlert


def shodan_init():
    shodan_api_key = config_parser("shodan", "api_key")
    api = shodan.Shodan(shodan_api_key)
    return api


def show_shodan_response(f):
    print("[+] New device found.")
    print('\t IP: ' + f['ip_str'] + ' port: ' + str(f['port']))
    print('\t Device: ' + str(f['os']))
    print('\t City: ' + f['location']['city'] + ' Country: ' + f['location']['country_name'] + ' ASN:' + f['asn'])
    if 'vulns' in f:
        for v in f['vulns']:
            print('\t [!] Vulnerability: ' + v + " CVSS:"+str(f['vulns'][v]['cvss']))
    print('\t Banner: ' + f['data'])


def save_alert(f):
    alert = SEAlert("Shodan",f['ip_str'],f['port'],f['location']['country_name'], f['data'])
    alert.add_asn(f['asn'])
    if f['location']['city'] is not None:
        alert.add_city(f['location']['city'])
    if'vulns' in f:
        for v in f['vulns']:
            alert.add_vulnerability(v, f['vulns'][v]['cvss'])
    if 'os' in f:
        alert.add_app(f['os'])
    if 'hostnames' in f:
        alert.add_hostname(f['hostnames'])
    if 'timestamp' in f:
        alert.add_timestamp(f['timestamp'])

    return alert


def shodan_search(keyword):
    alerts = []
    api = shodan_init()
    shodan_api_key = config_parser("shodan","api_key")
    api = shodan.Shodan(shodan_api_key)
    try:
        results = api.search(keyword)
        for result in results['matches']:
            alert = save_alert(result)
            alerts.append(alert)
    except shodan.APIError as e:
        print('Error: {}'.format(e))

    return alerts



