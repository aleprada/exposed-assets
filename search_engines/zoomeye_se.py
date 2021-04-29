import zoomeye.sdk as zoomeye
from config.config import config_parser
from search_engines.sealerts import SEAlert


def zoomeye_init():
    api_key = config_parser("zoomeye", "api_key")
    zm = zoomeye.ZoomEye(api_key=api_key)
    return zm


def show_zoomeye_response(f):
    print("[+] New device found.")
    print('\t APP/Service: ' + f[0] + ' IP: ' + f[1] + ' port: '+str(f[2]))
    print('\t Device: ' + f[3])
    print('\t City: ' + f[4] + ' Country: '+f[5] + ' ASN:'+str(f[6]))
    print('\t Banner: '+f[7])


def save_alert(f):
    alert = SEAlert("ZoomEye", f[1], f[2], f[5], f[7])
    if f[4] is not None:
        alert.add_city(f[4])
    if f[6] is not None:
        alert.add_asn(f[6])
    if f[3] is not None:
        alert.add_os(f[3])
    return alert


#try also multipage search
def zoomeye_search(keyword):
    alerts = []
    zm = zoomeye_init()
    zm.dork_search(keyword)
    filter = zm.dork_filter("app,ip,port,device,city,country,asn,banner")
    for f in filter:
        alert = save_alert(f)
        alerts.append(alert)
    return alerts




