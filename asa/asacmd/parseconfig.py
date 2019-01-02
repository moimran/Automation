from ciscoconfparse import CiscoConfParse
import sys,os
import datetime
import re
import ipaddress
import json


class ParseConfig:
    def __init__(self, asa_full_path, cache_path, config):
        self.path = asa_full_path
        self.config = config
        self.cache_path = cache_path
        full_file_name = self.path.split('/')[-1]
        if('.' in full_file_name):
            self.filename = full_file_name.strip().split('.')[0]
        else:
            self.filename = full_file_name
        self.input_raw = None
        self.read_file()
        self.names_f = '{0}/{1}_names.json'.format(self.cache_path,self.filename)
        self.objects_f = '{0}/{1}_objects.json'.format(self.cache_path,self.filename)
        self.object_groups_f = '{0}/{1}_object_groups.json'.format(self.cache_path,self.filename)
        self.access_lists_f = '{0}/{1}_access_lists.json'.format(self.cache_path,self.filename)
        print("Started parsing cisco configuration {0}".format(self.cache_path,self.filename))
        self.input_parse = CiscoConfParse(self.input_raw, 'asa')
        self.names = []
        self.objects = {}
        self.object_groups = {}
        self.access_lists = []

    # Function to parse the full configuration into dictionaries/lists that we will later use for analysis. Returns a bunch of lists and dictionaries.
    def parse_asa_configuration(self):
        # Read each line of the config, looking for configuration components that we care about
        for line in self.input_raw:
            # Identify all statically configured name/IPAddress translations
            if re.match(
                    "^name (([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).*",
                    line):
                self.names.append(line)

            # Identify and collect configurations for all configured objects
            if 'object network' in line:
                obj = self.input_parse.find_children_w_parents(line, '^(?! nat ?.*)')
                obj_name = (line.split()).pop(2)
                if not obj_name in self.objects and obj:
                    self.objects[obj_name] = (obj)

            # Identify and collect configurations for all configured object groups
            if 'object-group network' in line:
                obj_group = self.input_parse.find_children_w_parents(line, '.*')
                obj_group_name = (line.split()).pop(2)
                if not obj_group_name in self.object_groups and obj_group:
                    self.object_groups[obj_group_name] = (obj_group)

            # Identify and collect configurations for all configured access lists
            if re.match("^access-list .*", line):
                self.access_lists.append(line)

        # Return all these things. At this point we aren't being discriminate. These are a raw collections of all items.
        self.create_cache()
        return (self.names, self.objects, self.object_groups, self.access_lists)

    def read_file(self):
        print("Read the file")
        with open(self.path) as file:
            self.input_raw = file.readlines()

    def create_cache(self):
        print('Creating cache ....')
        with open(self.names_f, 'w') as f:
            json.dump(self.names, f)
        with open(self.objects_f, 'w') as f:
            json.dump(self.objects, f)
        with open(self.object_groups_f, 'w') as f:
            json.dump(self.object_groups, f)
        with open(self.access_lists_f, 'w') as f:
            json.dump(self.access_lists, f)

    def check_cache(self):
        cur_dir = os.getcwd()
        file_list = os.listdir(self.cache_path)
        flag = True
        for x in [self.names_f.split('/')[-1], self.objects_f.split('/')[-1], self.object_groups_f.split('/')[-1], self.access_lists_f.split('/')[-1]]:
            if x not in file_list:
                flag = False
        if(flag):
            print('cache available ....')
            return True
        else:
            print('cache not available ....')
            return False

    def read_cache(self):
        with open(self.names_f) as f:
            self.names = json.load(f)
        with open(self.objects_f) as f:
            self.objects = json.load(f)
        with open(self.object_groups_f) as f:
            self.object_groups = json.load(f)
        with open(self.access_lists_f) as f:
            self.access_lists = json.load(f)

    def delete_cache(self):
        os.remove(self.names_f)
        os.remove(self.objects_f)
        os.remove(self.object_groups_f)
        os.remove(self.access_lists_f)

    # Function to check names for references to the provided IP address. Returns a list.
    def check_names(self, input_names, ip_address):
        valid_names = []
        for item in input_names:
            if item.split()[1] == ip_address:
                valid_names.append(item.split()[2])
        return (valid_names)

    # Function to check objects for references to the provided IP address or matches for any matched name. Returns a list.
    def check_objects(self, input_objects, input_names, ip_address):
        valid_objects = []
        for k, v in input_objects.items():
            for item in v:
                # There are multiple possible configurations. Host, subnet and range. We need to validate if our IP Address is in any of them.
                if 'host' in item:
                    # This one is simple.  Check to see if a host IP matches directly or if it matches a matched name.
                    if item.split()[1] == ip_address:
                        valid_objects.append(k)
                    for name in input_names:
                        if item.split()[1] == name:
                            valid_objects.append(k)
                if 'subnet' in item:
                    # Here it requires a bit more work. We use the ipaddress library to validate if the IP resides within the network statement.
                    network = '{0}/{1}'.format(item.split()[1],item.split()[2])
                    try:
                        ipaddress.ip_network(network)
                    except ValueError:
                        continue
                    ipa = str(ip_address)
                    if ipaddress.ip_address(ipa) in ipaddress.ip_network(network):
                        valid_objects.append(k)
                if 'range' in item:
                    # This one was tricky. Since a range doesn't necessarily line up 1-for-1 with subnets, I used a summarization function in the ipaddress
                    # library to generate a list of summaries required to cover the range of addresses provided in the object.  I then check our
                    # IP address against that list (ike the block above) to see if it resides in any of the summaries.
                    ipa = str(ip_address)
                    first = str(item.split()[1])
                    last = str(item.split()[2])
                    try:
                        subnets = []
                        for ipaddr in ipaddress.summarize_address_range(ipaddress.IPv4Address(first),
                                                                        ipaddress.IPv4Address(last)):
                            if ipaddress.ip_address(ipa) in ipaddr:
                                valid_objects.append(k)
                    except Exception as e:
                        print('{}  {}  {}'.format(ipa,first,last))


        return (valid_objects)

    # Function to check object-groups for references to the provided IP address
    def check_object_groups(self, input_object_groups, input_names, input_objects, ip_address):
        # Now we're cooking with fire. Again we have multiple possible config statements under the object-group config and we need
        # to match against all of them. We are working our way down the heirarchy from more specific to less spacific, so we can use
        # previous matches to determine if an object, name, or host configuration is relevant to our IP address.
        valid_object_groups = []
        recursive_groups = {}
        for k, v in input_object_groups.items():
            for item in v:
                # Right off the bat we have to start dealing with a mess. Object-groups can be nested. Those nested groups are relevant
                # to our IP address so we need to pull configs referencing them as well.
                if 'group-object' in item:
                    if k in recursive_groups.keys():
                        recursive_groups[k].append(item.split()[1])
                    if not k in recursive_groups.keys():
                        recursive_groups[k] = []
                        recursive_groups[k].append(item.split()[1])
                # Check a host/name reference against already matched lists
                if 'network-object host' in item:
                    if item.split()[2] in input_names:
                        if k not in valid_object_groups:
                            valid_object_groups.append(k)
                    if item.split()[2] == ip_address:
                        if k not in valid_object_groups:
                            valid_object_groups.append(k)
                # Check object references against already matched objects
                if 'network-object object' in item:
                    if item.split()[2] in input_objects:
                        if k not in valid_object_groups:
                            valid_object_groups.append(k)
                # Identify network statements that are independent of objects and see if our IP address lies within their range.
                if re.match(
                        "^ network-object (([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).*",
                        item):
                    network = '{0}/{1}'.format(item.split()[1],item.split()[2])
                    try:
                        ipaddress.ip_network(network)
                    except ValueError:
                        print('address/netmask is invalid: %s' % network)
                        continue
                    ipa = str(ip_address)
                    if ipaddress.ip_address(ipa) in ipaddress.ip_network(network):
                        if k not in valid_object_groups:
                            valid_object_groups.append(k)
            '''
            # If any of our relevant object-groups had a nested-group, add it to the list of relevant object-groups.
            if k in valid_object_groups and k in recursive_groups.keys():
                for addons in recursive_groups[k]:
                    if addons not in valid_object_groups:
                        valid_object_groups.append(addons)
            '''
        return (valid_object_groups)

    # Function to check for recursive object-group references to those object-groups that matched the supplied IP Address
    def check_recursive_object_groups(self,input_object_groups, matched_object_groups):
        recursive_reference = []
        for k, v in input_object_groups.items():
            for item in v:
                for matched_item in matched_object_groups:
                    if 'group-object' in item and item.split()[1] == matched_item and k not in recursive_reference:
                        recursive_reference.append(k)
        return (recursive_reference)

    def deep_recursive_object_groups(self, input_object_groups, matched_object_groups):
        t=[]
        while(True):
            p = self.check_recursive_object_groups(input_object_groups, matched_object_groups)
            t.append(p)
            if(len(p) == 0):
                return [inner for outer in t for inner in outer]
            else:
                matched_object_groups = p

    # Function to check access-lists against previously discovered names, objects, object-groups and the provided IP address
    def check_access_lists(self, input_access_lists, input_names, input_objects, input_object_groups, ip_address):
        valid_access_lists = {}
        for acl in input_access_lists:
            # We have to use enumerate here because I need to be able to reference the next word in the sentence so I need an accurate index.
            for i, v in enumerate(acl.split()):
                # Looking for specific key words in the ACL
                # Host is always followed by a single IP address so check to see if the next work matches the supplied IP Address or a matched name.
                if v == 'host':
                    for names in input_names:
                        # Have to check for the existence of a next word.  Sometimes, including the test file I was working with, host is the last word
                        # in an ACL remark, which makes this script puke all over itself.  Better safe than sorry.
                        if (i + 1) < len(acl.split()):
                            if acl.split()[i + 1] == names:
                                if acl.split()[1] in valid_access_lists.keys():
                                    valid_access_lists[acl.split()[1]].append(acl)
                                if not acl.split()[1] in valid_access_lists.keys():
                                    valid_access_lists[acl.split()[1]] = []
                                    valid_access_lists[acl.split()[1]].append(acl)
                    if (i + 1) < len(acl.split()):
                        if acl.split()[i + 1] == ip_address:
                            if acl.split()[1] in valid_access_lists.keys():
                                valid_access_lists[acl.split()[1]].append(acl)
                            if not acl.split()[1] in valid_access_lists.keys():
                                valid_access_lists[acl.split()[1]] = []
                                valid_access_lists[acl.split()[1]].append(acl)
                # Here we're looking for the object key word and the following word will be an object.  We then check that againast our matched objects.
                if v == 'object':
                    for objects in input_objects:
                        if (i + 1) < len(acl.split()):
                            if acl.split()[i + 1] == objects:
                                if acl.split()[1] in valid_access_lists.keys():
                                    valid_access_lists[acl.split()[1]].append(acl)
                                if not acl.split()[1] in valid_access_lists.keys():
                                    valid_access_lists[acl.split()[1]] = []
                                    valid_access_lists[acl.split()[1]].append(acl)
                # Same as the object routine above.
                if v == 'object-group':
                    for object_groups in input_object_groups:
                        if (i + 1) < len(acl.split()):
                            if acl.split()[i + 1] == object_groups:
                                if acl.split()[1] in valid_access_lists.keys():
                                    valid_access_lists[acl.split()[1]].append(acl)
                                if not acl.split()[1] in valid_access_lists.keys():
                                    valid_access_lists[acl.split()[1]] = []
                                    valid_access_lists[acl.split()[1]].append(acl)
                # Here we're looking for IP ranges directly configured in the ACL.  Use regex to match an IP address or subnet mask.
                if re.match(
                        "(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])",
                        v):
                    if (i + 1) < len(acl.split()):
                        if re.match(
                                "(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])",
                                acl.split()[i + 1]):
                            network = str(v + "/" + acl.split()[i + 1])
                            ipa = str(ip_address)
                            # The problem here is that we can match on a mask and then an IP so we don't know if we have a valid IP/Mask combo.
                            # In order to not have the script fall apart when this happens, I'm just catching the exception and moving on.  The IPAddress
                            # library returns a ValueError if the network is represnted in a Mask/IPAddress format.  We just ignore these instances.
                            # Probably not the cleanest option but it works for now.
                            try:
                                if ipaddress.ip_address(ipa) in ipaddress.ip_network(network):
                                    if acl.split()[1] in valid_access_lists.keys():
                                        valid_access_lists[acl.split()[1]].append(acl)
                                    if not acl.split()[1] in valid_access_lists.keys():
                                        valid_access_lists[acl.split()[1]] = []
                                        valid_access_lists[acl.split()[1]].append(acl)
                            except ValueError:
                                continue
                # We have to include any/any ACLs as well since they technicaly match all addresses.
                if v == 'any':
                    if (i + 1) < len(acl.split()):
                        if acl.split()[i + 1] == 'any':
                            if acl.split()[1] in valid_access_lists.keys():
                                valid_access_lists[acl.split()[1]].append(acl)
                            if not acl.split()[1] in valid_access_lists.keys():
                                valid_access_lists[acl.split()[1]] = []
                                valid_access_lists[acl.split()[1]].append(acl)
        return (valid_access_lists)

    def get_match_objects(self, user_ip_address):
        exclude_list = self.config.get_exclude_list
        print("Checking names ....")
        conf_names = self.check_names(self.names, user_ip_address)
        print("Checking objects...")
        conf_objects = self.check_objects(self.objects, self.names, user_ip_address)
        print("Checking object groups...")
        conf_object_groups = self.check_object_groups(self.object_groups, conf_names, conf_objects, user_ip_address)
        #print(conf_names)
        print(conf_objects)
        print(conf_object_groups)
        deep_group = self.deep_recursive_object_groups(self.object_groups, conf_object_groups)
        merged_object_groups = conf_object_groups + deep_group
        print(merged_object_groups)
        print("excluding access list for object groups {}".format(exclude_list))
        for exclude_object in exclude_list:
            if(exclude_object in conf_objects):
                conf_objects.remove(exclude_object)
            if(exclude_object in conf_object_groups):
                conf_object_groups.remove(exclude_object)
            if(exclude_object in merged_object_groups):
                merged_object_groups.remove(exclude_object)

        print("Checking access-lists...")
        conf_access_lists = self.check_access_lists(self.access_lists, conf_names, conf_objects, merged_object_groups, user_ip_address)
        print(conf_access_lists)


    def parse_configuration(self):
        print("Started parsing asa configuration")
        if(self.check_cache()):
            self.read_cache()
        else:
            self.parse_asa_configuration()
            print("end parsing configuration")