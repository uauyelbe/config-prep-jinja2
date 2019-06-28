from jinja2 import Environment, FileSystemLoader
import pandas
import yaml
from pprint import pprint
import ipaddress

file = FileSystemLoader(".")
env = Environment(loader=file)
template = env.get_template("template.j2")
crypto = env.get_template("crypto_template.j2")

row = 1

def read_atm_hostname(filename):
    df_hostname = pandas.read_excel(filename, usecols="B", skiprows=row, sheet_name="ATMs", header=None)
    return df_hostname

def read_kcell(filename):
    df_kcell = pandas.read_excel(filename, usecols="C", skiprows=row, sheet_name="ATMs", header=None)
    return df_kcell

def read_tele2(filename):
    df_tele2 = pandas.read_excel(filename, usecols="G", skiprows=row, sheet_name="ATMs", header=None)
    return df_tele2

def read_kcell_ip(filename):
    df_kcell_ip = pandas.read_excel(filename, usecols="D", skiprows=row, sheet_name="ATMs", header=None)
    return df_kcell_ip

def read_tele2_ip(filename):
    df_tele2_ip = pandas.read_excel(filename, usecols="H", skiprows=row, sheet_name="ATMs", header=None)
    return df_tele2_ip

def read_int_ip(filename):
    df_int_ip = pandas.read_excel(filename, usecols="J", skiprows=row, sheet_name="ATMs", header=None)
    return df_int_ip

def read_tunn_ip(filename):
    df_tunn_ip = pandas.read_excel(filename, usecols="I", skiprows=row, sheet_name="ATMs", header=None)
    return df_tunn_ip

def main():
    filename = "ATM-3G.xlsx"
    hostname = read_atm_hostname(filename).values.tolist()
    kcell = read_kcell(filename).values.tolist()
    tele2 = read_tele2(filename).values.tolist()
    kcell_ip = read_kcell_ip(filename).values.tolist()
    tele2_ip = read_tele2_ip(filename).values.tolist()
    int_ip = read_int_ip(filename).values.tolist()
    tunn_ip = read_tunn_ip(filename).values.tolist()

    df_username = pandas.read_excel("PPP-User.xlsx", usecols="B", skiprows=1, sheet_name="Лист1",
                                    header=None).values.tolist()
    df_values = pandas.read_excel("PPP-User.xlsx", usecols="E", skiprows=1, sheet_name="Лист1",
                                  header=None).values.tolist()

    for j in range(len(hostname)):
        with open("config/" + str(hostname[j]).strip("['']") + ".txt", "a") as f,\
                open("config/" + str(hostname[j]).strip("['']") + "_crypto.txt", "a") as cryp:

            #ip address for ospf network
            ip_net = ipaddress.ip_address(str(int_ip[j]).strip("['']")) - 1

            #finding kcell username and password
            for i in range(len(df_username)):
                if df_username[i] == kcell[j]:
                    tmp_kcell = df_username[i]
                    tmp_kcell_pass = df_values[i]
                else:
                    continue

            #finding tele2 username and password
            for i in range(len(df_username)):
                if df_username[i] == tele2[j]:
                    tmp_tele2 = df_username[i]
                    tmp_tele2_pass = df_values[i]
                else:
                    continue

            #render to jinja2 template
            rnd_tmp = template.render(kcell_name=str(tmp_kcell).strip("['']"),
                                      tele2_name=str(tmp_tele2).strip("['']"),
                                      hostname=str(hostname[j]).strip("['']"),
                                      tunn_ip=str(tunn_ip[j]).strip("['']"),
                                      int_ip=str(int_ip[j]).strip("['']"),
                                      router_id=str(tunn_ip[j]).strip("['']"),
                                      p2p_net=ip_net,
                                      kcell_pass=str(tmp_kcell_pass).strip("['']"),
                                      tele2_pass=str(tmp_tele2_pass).strip("['']"))

            rnd_tmp_crypto = crypto.render(kcell_name=str(tmp_kcell).strip("['']")[:-3],
                                           tele2_name=str(tmp_tele2).strip("['']")[:-3],
                                           kcell_ip=str(kcell_ip[j]).strip("['']"),
                                           tele2_ip=str(tele2_ip[j]).strip("['']"))

            f.write(rnd_tmp)
            cryp.write(rnd_tmp_crypto)

if __name__ == "__main__":
    main()