from netmiko import Netmiko
import threading
from asa.asacmd.showcmd import ShowCmd
from common import OutlookClient

class DeviceConnect(threading.Thread):
    def __init__(self, ip_address, user, password, secret, device_type, config):
        super().__init__()
        self.ip_address = ip_address
        self.user = user
        self.password = password
        self.secret = secret
        self.device_type = device_type
        self.config = config

    def run(self):
        connect = Netmiko(host=self.ip_address, username=self.user, password=self.password,
                              secret=self.secret, device_type=self.device_type)
        asa_commands = ShowCmd(connect, self.config, self.ip_address)
        asa_commands.run_command_list()
        connect.disconnect()

    def run_command(self):
        connect = Netmiko(host=self.ip_address, username=self.user, password=self.password,
                              secret=self.secret, device_type=self.device_type)
        asa_commands = ShowCmd(connect, self.config, self.ip_address)
        asa_commands.run_command_list()
        connect.disconnect()
