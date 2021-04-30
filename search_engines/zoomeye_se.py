import zoomeye.sdk as zoomeye
from config.config import config_parser
from search_engines.sealerts import SEAlert


def zoomeye_init():
    api_key = config_parser("zoomeye", "api_key")
    zm = zoomeye.ZoomEye(api_key=api_key)
    return zm


def show_zoomeye_response(f):
    print("[+] New device found.")
    print('\t APP/Service: ' + f['portinfo']['service']+ ' IP: ' + f['ip'] + ' port: '+str(f['portinfo']['port']))
    print('\t  Country: '+f['geoinfo']['country']['names']['en'] + ' ASN:'+str(f['geoinfo']['asn']))
    print('\t Banner: '+f['portinfo']['banner'])


def save_alert(f):
    alert = SEAlert("ZoomEye", f['ip'], f['portinfo']['port'], f['geoinfo']['country']['names']['en'], f['portinfo']['banner'])
    if f['geoinfo']['asn'] is not None:
        alert.add_asn(f['geoinfo']['asn'])
    if f['portinfo']['app'] is not None:
        alert.add_app(f['portinfo']['app'])
    if f['timestamp'] is not None:
        alert.add_timestamp(f['timestamp'])
    return alert


#try also multipage search
def zoomeye_search(keyword):
    alerts = []
    zm = zoomeye_init()
    data = zm.dork_search(keyword)
    '''filter = zm.dork_filter("app,ip,port,device,city,country,asn,banner")
    for f in filter:
        alert = save_alert(f)
        alerts.append(alert)'''
    for d in data:
        save_alert(d)
    return alerts




