from sqlite3 import Error
import configparser
import sqlite3
import os


def config_parser(section, key):
    config = configparser.ConfigParser()
    try:
        config.read(os.path.join(os.path.dirname(__file__)+"/config_files/config.ini"))
        result = config.get(section, key)
        return result
    except config.NoOptionError:
        raise Exception("There was a problem with configuration file. The key does not exist.")
    except config.NoSectionError:
        raise Exception("There was a problem with configuration file. The key does not exist.")


def config_parser_section(section):
    parser = config = configparser.ConfigParser()
    try:
        parser.read(os.path.dirname(__file__)+"/config_files/config.ini")
        result = dict(parser.items(section))
        return result
    except config.NoSectionError:
        raise Exception("There was a problem with configuration file. The key does not exist.")


def load_file(filename):
    path_software_list = os.path.join(os.path.dirname(__file__) + "/config_files/"+filename)
    keyword_list = []
    with open(path_software_list, "r") as ins:
        for line in ins:
            keyword_list.append(line.strip())
        ins.close()
    return keyword_list


def create_connection():
    db_file = os.path.join(os.path.dirname(__file__))+'/sqlite/alerts.db'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def save_alert_db(timestamp, ip, port, country):
    conn = create_connection()
    sql = ''' INSERT OR IGNORE INTO alerts(timestamp,ip,port,country)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (timestamp, ip, port, country))
    conn.commit()
    return cur.lastrowid


def check_saved_threats(ip, port, timestamp):
    exists = False
    sql = '''SELECT * FROM alerts WHERE ip=? AND port=? AND timestamp=?'''
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(sql, (ip, port, timestamp))
    result = cur.fetchone()
    if result:
        exists = True
    return exists
