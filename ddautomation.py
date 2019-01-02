from asa import Asarest,ObjectDb,Common
from sqlmgr import Sqlmgr
from asa import DeviceConnect
from asa import ParseConfig
import os
from readconfig import ReadConfiguration
from common import Utility

class MyMain:
    def __init__(self, config):
        self.config = config

    def run_command_list_multiple_device(self):
        username,password,secret,device_type = self.config.get_cred
        threads=[]
        for device in self.config.get_device_list:
            thread = DeviceConnect(device, username, password, secret, device_type, self.config)
            threads += [thread]
            thread.start()
        for x in threads:
            x.join()
        Utility.send_email(self.config)

    def run_command_list(self, device, flag):
        username, password, secret, device_type = self.config.get_cred
        cli = DeviceConnect(device, username, password, secret, device_type, self.config)
        cli.run_command()
        Utility.send_email(self.config)

    def asa_config_parser(self):
        user_ip_address = '10.22.14.61'
        asa_list_parse_config = {}
        for asa_config in self.config.get_asa_full_path_list:
            print(asa_config.split('/')[-1])
            asa_list_parse_config['{}'.format(asa_config.split('/')[-1])]=ParseConfig(asa_config, self.config.get_cache_path, self.config)

        for filename,asa_config in asa_list_parse_config.items():
            asa_config.parse_configuration()

        for filename,asa_config in asa_list_parse_config.items():
            print('\n+++++++++++++++')
            print(filename)
            print('+++++++++++++++\n')
            asa_config.get_match_objects(user_ip_address)

    def asa_config_parser1(self):
            user_ip_address = ''
            asa_list_parse_config =[]
            for asa_config in self.config.get_asa_full_path_list:
                asa_list_parse_config.append(ParseConfig(asa_config, self.config.get_cache_path, self.config))
            #asa_list_parse_config[0].parse_configuration()
            asa_list_parse_config[1].parse_configuration()
            #asa_list_parse_config[0].get_match_objects(user_ip_address)
            asa_list_parse_config[1].get_match_objects(user_ip_address)
            #parse_obj.delete_cache()




    def asa_rest_api(self):
        deviceConnect = Asarest(device="", username="admin",
                                password="", verify_cert=False)
        sql = Sqlmgr("object.db")
        hostname = 'custname'
        objectNetwrokDB = ObjectDb(deviceConnect, sql,hostname)
        objectNetwrokDB.create_obj_network_group_db()
        objectNetwrokDB.create_obj_network_group_db()
        objectNetwrokDB.create_obj_network_service_group_db()
        objectNetwrokDB.create_acl_db()
        helper = Common(sql, hostname)
        helper.create_internel_database()
        print(helper.find_port_service_obj('tcp/ssh'))
        helper.find_objid_object_network('')

if __name__ == "__main__":
    '''
    print('\n\n1.Find object groups ')
    print('\n\n2.Automate commands')
    print('\n\n3.exit')
    mynumber = input("Please select any of the above options: ")
    '''
    main_base = os.path.dirname(__file__)
    config = ReadConfiguration(main_base)
    main = MyMain(config)
    main.asa_config_parser()
    #main.run_command_list_multiple_device()
