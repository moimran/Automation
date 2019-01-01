import os,json

class ReadConfiguration:
    def __init__(self, main_directory):
        self.main_directory = main_directory

    @property
    def get_asa_full_path_list(self):
        full_path = []
        asa_config_path = '{0}/configfiles/asaconfigs'.format(self.main_directory)
        asa_file_list = os.listdir(asa_config_path)
        for asa_config in asa_file_list:
            full_path.append('{0}/{1}'.format(asa_config_path,asa_config))
        return full_path

    @property
    def get_cache_path(self):
        return '{0}/configfiles/cache'.format(self.main_directory)

    @property
    def get_show_output_path(self):
        return '{0}/configfiles/showoutput'.format(self.main_directory)

    @property
    def get_cred(self):
        cred_path = '{0}/configfiles/creds'.format(self.main_directory)
        with open(cred_path) as f:
            data = json.load(f)
        return (data['tacacsusername'], data['tacacspassword'], data['tacacssecret'], data['devicetype'])

    @property
    def get_device_list(self):
        device_list_path = '{0}/configfiles/devicelist.csv'.format(self.main_directory)
        device_list = []
        with open(device_list_path, 'r') as file_handle:
            file_content = file_handle.readlines()
            for line in file_content:
                device_list.append(line.strip())

        return device_list

    @property
    def get_command_list(self):
        command_list_path = '{0}/configfiles/commandlist'.format(self.main_directory)
        command_list = []
        with open(command_list_path, 'r') as file_handle:
            file_content = file_handle.readlines()
            for line in file_content:
                command_list.append(line.strip())

        return command_list

    @property
    def email_data(self):
        cred_path = '{0}/configfiles/creds'.format(self.main_directory)
        with open(cred_path) as f:
            data = json.load(f)
        return (data['sendaddress'], data['commonbody'], data['subject'])
