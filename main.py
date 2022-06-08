from netconf import NetConf as nf
from netauto import NetAuto as na
from options import Options as opt
from configparser import ConfigParser as conf

if __name__ == "__main__":
    parser = conf()
    parser.read("conf.cfg")
    netconf = nf(
        host=parser.get("NETCONF", "host"), 
        port=parser.getint("NETCONF", "port"), 
        username=parser.get("NETCONF", "username"), 
        password=parser.get("NETCONF", "password"),
        hostkey_verify=parser.getboolean("NETCONF", "hostkey_verify")
    )
    options = opt()
    options += ("banner", "Banner MOTD")
    options += ("hostname", "Hostname")
    options += ("loopback", "Loopback")
    options += ("config", "View Config")
    webex_access_token = parser.get("WEBEX", "access_token")
    webex_room_id = parser.get("WEBEX", "room_id")
    netauto = na(netconf, options, webex_access_token, webex_room_id)
    netauto.init()

    # All the tasks are performed here in the final exam
    try:
        print("Change the hostname of CSR1000v to {}_SkillsExam".format(parser.get("SERVER", "hostname")))
        netauto.set_hostname(parser.get("SERVER", "hostname"))
        print("\n")
    except:
        pass
    try:
        print(" Create a backup of startup and running config")
        netauto.backup_config(startup=True, running=True)
        print("\n")
    except:
        pass
    try:
        print("Add the description")
        netauto.add_description("1", "Interface G1")
        print("\n")
    except:
        pass
    try:
        print("Set the IPv6 address")
        netauto.set_ipv6_address("2607:f0d0:1002:51::4")
        print("\n")
    except:
        pass
    try:
        print("Add new loopback 1")
        netauto.set_loopback(
            parser.get("SERVER","loopback_number"),
            parser.get("SERVER", "loopback_address"),
            parser.get("SERVER", "loopback_mask")
        )
        print("\n")
    except:
        pass
    try:
        print("Configure OSPF")
        netauto.configureOSPF()
        print("\n")
    except:
        pass