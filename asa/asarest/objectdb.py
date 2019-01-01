import json

class ObjectDb:

    def __init__(self, deviceConnect, sql, hostname):
        print("Initializing database .... ")
        self.deviceConnect = deviceConnect
        self.sql = sql
        self.hostname = hostname
    
    def create_obj_network_db(self):
        print("Building object network database .... ")
        self.sql.create('''CREATE TABLE IF NOT EXISTS {0}objectnetwork(
   kind        VARCHAR(17)  
  ,selfLink    VARCHAR(82) 
  ,name        VARCHAR(32) 
  ,hostkind    VARCHAR(11) 
  ,hostvalue   VARCHAR(18) 
  ,objectId    VARCHAR(32) 
  ,description VARCHAR(29)
)'''.format(self.hostname))
        resp = self.deviceConnect.get_networkobjects()
        json_data = json.loads(resp.text)
        dictObjectNetwork = json_data["items"]
        for ObjectNetwork in dictObjectNetwork:
            if('description' in ObjectNetwork):
                self.sql.query('''INSERT INTO {0}objectnetwork(
                    kind,
                    selfLink,
                    name,
                    hostkind,
                    hostvalue,
                    objectId,
                    description) VALUES (?,?,?,?,?,?,?)'''.format(self.hostname), 
                    (ObjectNetwork['kind'], ObjectNetwork['selfLink'], ObjectNetwork['name'], ObjectNetwork['host']['kind'], ObjectNetwork['host']['value'], ObjectNetwork['objectId'], ObjectNetwork['description']))
            else:
                self.sql.query('''INSERT INTO {0}objectnetwork(
                    kind,
                    selfLink,
                    name,
                    hostkind,
                    hostvalue,
                    objectId,
                    description) VALUES (?,?,?,?,?,?,?)'''.format(self.hostname), 
                    (ObjectNetwork['kind'], ObjectNetwork['selfLink'], ObjectNetwork['name'], ObjectNetwork['host']['kind'], ObjectNetwork['host']['value'], ObjectNetwork['objectId'], None,))

    
    def create_obj_network_group_db(self):
        print("Building object network group database .... ")
        self.sql.create('''CREATE TABLE IF NOT EXISTS {0}objectnetworkgroup(
   kind        VARCHAR(17) 
  ,selfLink    VARCHAR(82) 
  ,name        VARCHAR(32) 
  ,memberkind     TEXT
  ,memberObjectId     TEXT
  ,membervalue     TEXT
  ,memberreflink     TEXT
  ,objectId    VARCHAR(32) 
  ,description VARCHAR(29)
)'''.format(self.hostname))
        resp = self.deviceConnect.get_networkobjectgroups()
        json_data = json.loads(resp.text)
        dictObjectNetwork = json_data["items"]
        for ObjectNetwork in dictObjectNetwork:
            for member in ObjectNetwork['members']:
                if('value' in member):
                    self.sql.query('''INSERT INTO {0}objectnetworkgroup(
                        kind,
                        selfLink,
                        name,
                        memberkind,
                        memberObjectId,
                        membervalue,
                        memberreflink,
                        objectId,
                        description) VALUES (?,?,?,?,?,?,?,?,?)'''.format(self.hostname), 
                        (ObjectNetwork['kind'], ObjectNetwork['selfLink'], ObjectNetwork['name'], member['kind'], None,
                        member['value'] , 
                        None , 
                        ObjectNetwork['objectId'],
                        ObjectNetwork['description']))

                else:
                    self.sql.query('''INSERT INTO {0}objectnetworkgroup(
                        kind,
                        selfLink,
                        name,
                        memberkind,
                        memberObjectId,
                        membervalue,
                        memberreflink,
                        objectId,
                        description) VALUES (?,?,?,?,?,?,?,?,?)'''.format(self.hostname), 
                        (ObjectNetwork['kind'], ObjectNetwork['selfLink'], ObjectNetwork['name'], member['kind'], member['objectId'],
                        None , 
                        member['refLink'] , 
                        ObjectNetwork['objectId'],
                        ObjectNetwork['description']))

    def create_obj_network_service_group_db(self):
        print("Building object network service group database .... ")
        self.sql.create('''CREATE TABLE IF NOT EXISTS {0}objectnetworkservicegroup(
   kind        VARCHAR(17) 
  ,selfLink    VARCHAR(82) 
  ,name        VARCHAR(32) 
  ,memberkind     TEXT
  ,membervalue    TEXT
  ,objectId    VARCHAR(32) 
  ,description VARCHAR(29)
)'''.format(self.hostname))
        resp = self.deviceConnect.get_networkservicegroups()
        json_data = json.loads(resp.text)
        dictObjectNetwork = json_data["items"]
        for ObjectNetwork in dictObjectNetwork:
            for member in ObjectNetwork['members']:
                self.sql.query('''INSERT INTO {0}objectnetworkservicegroup(
                    kind,
                    selfLink,
                    name,
                    memberkind,
                    membervalue,
                    objectId,
                    description) VALUES (?,?,?,?,?,?,?)'''.format(self.hostname), 
                    (ObjectNetwork['kind'], ObjectNetwork['selfLink'], ObjectNetwork['name'], member['kind'],member['value'], ObjectNetwork['objectId'], ObjectNetwork['description']))

    def create_acl_db(self):
        #resp = self.deviceConnect.get_acls()
        resp = self.deviceConnect.get_acl('outside.810_access_in')
        print(resp.text)




