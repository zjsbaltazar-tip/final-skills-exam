from netconf import NetConf as nf
from options import Options as opt
import xml.dom.minidom
import requests

class NetAuto(object):

    def __init__(self, netconf: nf, options: opt, webex_access_token: str, webex_room_id: str):
        self.netconf = netconf
        self.options = options
        self.webex_access_token = webex_access_token
        self.webex_room_id = webex_room_id
        self.msg = ""
    
    def init(self):
        self.options.connect("banner", self.set_banner_motd)
        self.options.connect("hostname", self.set_hostname)
        self.options.connect("loopback", self.set_loopback)
        self.options.connect("config", self.display_config)

    def set_banner_motd(self, bmotd):
        netconf_bmotd_start = """
        <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <banner>
        <motd>
        <banner>"""
        netconf_bmotd_end = """</banner>
        </motd>
        </banner>
        </native>
        </config>
        """
        netconf_bmotd = netconf_bmotd_start + bmotd + netconf_bmotd_end
        netconf_reply = self.netconf.manager.edit_config(target="running", config=netconf_bmotd)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
        self.msg = """
        CONFIGURATION NOTIFICATION:
        Target device: {}
        Changes: Banner motd
        Description: {}
        Note: This is an automated message.
        """.format(self.netconf.host, bmotd)

    def backup_config(self, startup=False, running=True):
        config = {"startup": None, "running": None}
        netconf_reply = self.netconf.manager.get_config(source="running")
        if startup: 
            config["startup"] = xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()
            with open("startup_backup.txt", "w+") as file:
                file.write(config["startup"])
        if running: 
            config["running"] = xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()
            with open("run_backup.txt", "w+") as file:
                file.write(config["running"])
            
    def set_hostname(self, hn):
        netconf_hn_start = """
        <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>"""
        netconf_hn_end = """</hostname>
        </native>
        </config>
        """
        netconf_hn = netconf_hn_start + hn + netconf_hn_end
        netconf_reply = self.netconf.manager.edit_config(target="running", config=netconf_hn)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
        self.msg = """
        CONFIGURATION NOTIFICATION:
        Target device: {}
        Changes: Hostname
        Description: {}
        Note: This is an automated message.
        """.format(self.netconf.host, hn)

    def add_description(self, interface_number, description):
        netconf_add_desc = f"""
        <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <interface>
                    <GigabitEthernet>
                        <name>{interface_number}</name>
                        <description>{description}</description>
                    </GigabitEthernet>
                </interface>
            </native>
        </config>
        """
        netconf_reply = self.netconf.manager.edit_config(target="running", config=netconf_add_desc)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    def set_ipv6_address(self, ipv6_addr):
        netconf_set_ipv6 = f"""
        <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <interface>
                        <GigabitEthernet>
                                <name>1</name>
                                <ipv6>
                                        <address>
                                                <prefix-list>
                                                        <prefix>{ipv6_addr}</prefix>
                                                </prefix-list>
                                        </address>
                                </ipv6>
                        </GigabitEthernet>
                </interface>
            </native>
        </config>
        """
        netconf_reply = self.netconf.manager.edit_config(target="running", config=netconf_set_ipv6)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    def configureOSPF(self):
        netconf_ospf = """
        <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <router>
                            <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                                    <id>1</id>
                                    <router-id>1.1.1.1</router-id>
                                    <network>
                                            <ip>10.1.1.5</ip>
                                            <mask>0.0.0.255</mask>
                                            <area>0</area>
                                    </network>
                                    <network>
                                            <ip>192.168.56.0</ip>
                                            <mask>0.0.0.255</mask>
                                            <area>0</area>
                                    </network>
                            </ospf>
                    </router>
            </native>
        </config>
        """
        netconf_reply = self.netconf.manager.edit_config(target="running", config=netconf_ospf)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    def set_loopback(self, 
            loopback_number,
            loopback_address, 
            loopback_mask
        ):
        netconf_loopback_number_start = """
        <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
        <Loopback>
            <name>"""
        netconf_loopback_number_end = """</name>
        """
        netconf_loopback_address_start = """<ip>
        <address>
        <primary>
        <address>"""
        netconf_loopback_address_end = """</address>
        """
        netconf_loopback_mask_start = """<mask>"""
        netconf_loopback_mask_end = """</mask>
        </primary>
        </address>
        </ip>
        </Loopback>
        </interface>
        </native>
        </config>
        """
        netconf_loopback = netconf_loopback_number_start + loopback_number + netconf_loopback_number_end + netconf_loopback_address_start + loopback_address + netconf_loopback_address_end + netconf_loopback_mask_start + loopback_mask + netconf_loopback_mask_end
        netconf_reply = self.netconf.manager.edit_config(target="running", config=netconf_loopback)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
        self.msg = """
        CONFIGURATION NOTIFICATION:
        Target device: {}
        Changes: Loopback interface
        Description: Loopback{}, IP:{}, mask:{}
        Note: This is an automated message.
        """.format(self.netconf.host, loopback_number, loopback_address, loopback_mask)

    def display_config(self):
        netconf_reply = self.netconf.manager.get_config(source="running")
        netconf_filter = """
        <filter>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
        </filter>
        """
        netconf_reply = self.netconf.manager.get_config(source="running", filter=netconf_filter)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    def webex_notif(self):
        #WEBEX message
        access_token = self.webex_access_token
        room_id = self.webex_room_id
        url = 'https://webexapis.com/v1/messages'

        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'
        }
        params = {'roomId': room_id, 'markdown': self.msg}
        res = requests.post(url, headers=headers, json=params)
        print(res.json())
        self.msg = ""