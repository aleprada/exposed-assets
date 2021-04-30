from search_engines.zoomeye_se import zoomeye_search
from search_engines.shodan_se import shodan_search
from search_engines.sealerts import SEAlert, filter_alerts_with_keywords
from config.config import load_file
from misp_alerts.misp import save_exposed_assets
import argparse


def search():
    dorks = load_file("dorks.txt")
    alerts = []
    for d in dorks:
        print("\t[*] Searching: "+d)
        alerts_shodan=shodan_search(d)
        alerts_zoomeye=zoomeye_search(d)
        alerts = alerts_shodan + alerts_zoomeye
    return alerts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--alerts", help=" Check if the banner of the exposed assets gathered contains any of"
                                               " your keyword list. See folder config->config_files ", action="store_true")
    parser.add_argument("-m", "--misp", help="Send alerts of exposed assets to MISP", action="store_true")
    parser.add_argument("-p", "--proxy", help="Set a proxy for sending the alert to your MISP instance..", action="store_true")
    parser.add_argument("-v", "--verbose", help="Show details of the IT/OT gathered. ", action="store_true")

    args = parser.parse_args()
    proxy_usage = False
    print("[*] Gathering IT/OT exposed assets")
    alerts = search()

    if args.alerts:
        print("[*] Checking if IT/OT assets gathered contain any keyword of your list.")
        filtered_alerts = filter_alerts_with_keywords(alerts)
        if args.verbose:
            for a in filtered_alerts:
                a.show_alert()
            print("[*] Number of IT/OT exposed assets with alert: " + str(len(filtered_alerts)))
        if args.misp:
            if args.proxy:
                proxy_usage = True
            print("[*] Sending alerts to MISP")
            save_exposed_assets(filtered_alerts, proxy_usage)

    elif args.verbose:
        for a in alerts:
            a.show_alert()
        print("[*] Number of IT/OT exposed assets discovered: "+str(len(alerts)))


if __name__ == '__main__':
    main()