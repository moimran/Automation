import ipaddress

class Common:

    def __init__(self, sql, hostname):
        self.sql = sql
        self.hostname = hostname
        self.networkservicegrouplist = []
        self.networkobjectnetworklist = []
        self.networkobjectlist = []
        self.networkobjectrangelist = []
        self.objectnetworkgrouplist = []
        self.networkgroupmemberObjectIdlist = 0
        self.networkgroupObjectIdlist = 0
    
    def find_port_service_obj(self, port):
        portIdlist=[item for item in self.networkservicegrouplist if item[0] == port]
        return portIdlist
    
    def convert_ipv4(self,ip):
        return tuple(int(n) for n in ip.split('.'))
    
    def check_in_range(self,startip,endip,checkip):
        start = self.convert_ipv4(startip)
        end = self.convert_ipv4(endip)
        ip = self.convert_ipv4(checkip)
        ip_range = [(start), (end)]
        if(ip >= ip_range[0] and ip <= ip_range[1]):
            return True
        else:
            return False


    def find_objid_object_network(self, ip):
        t=[]
        l=''
        z=[]
        # check IP for ip in in network object host
        objIdlist=[item for item in self.networkobjectlist if item[0] == ip]
        # check for ip in a subnet in network object 
        for item in self.networkobjectnetworklist: 
            if ipaddress.ip_address(str(ip)) in ipaddress.ip_network(str(item[0])):
                objIdlist.append(item)

        # check for ip in a range in network object     
        for item in self.networkobjectrangelist:
            (start,end)=item[0].split('-')
            if(self.check_in_range(start,end,ip)):
                 objIdlist.append(item)
        
        print(objIdlist)
        if(len(objIdlist) != 0):
            flag=True
            f= True
            while(flag):
                for objIdtuple in objIdlist:
                    print('Evaluating object ID {0} ....'.format(objIdtuple[1]) )
                    if(objIdtuple[1] in self.networkgroupmemberObjectIdlist):
                        f=[item for item in self.objectnetworkgrouplist  if item[1] == objIdtuple[1]]
                        print(f)
                        l=[]
                        for objGroupeTuple in f:
                            if(objGroupeTuple[3] in self.networkgroupmemberObjectIdlist):
                                l=[item for item in self.objectnetworkgrouplist  if item[1] == objGroupeTuple[3]]
                                print(l)
                            else:
                                ff=1
                                while(len(l) != 0):
                                    for ll in l:
                                        if(ll[3] in self.networkgroupmemberObjectIdlist):
                                            z= [item for item in self.objectnetworkgrouplist  if item[1] == ll[3]]
                                            print(z)
                                            l=z
                                        else:
                                            ff=0
                                            break
                                    if(ff == 0):
                                        break
                                flag = False                  
                    else:
                        print('ppppppppppppp')
                        flag=False
        else:
            objIdgrouplist = [item for item in self.objectnetworkgrouplist if item[2] == ip]
            print(objIdgrouplist)
            l=objIdgrouplist
            ff=1
            while(len(l) != 0):
                for ll in l:
                    if(ll[3] in self.networkgroupmemberObjectIdlist):
                        z= [item for item in self.objectnetworkgrouplist  if item[1] == ll[3]]
                        print(z)
                        l=z
                    else:
                        ff=0
                        break
                if(ff == 0):
                    break

        return t  

    def create_internel_database(self):
        ipquery = '''SELECT membervalue,objectId FROM  {0}objectnetworkservicegroup'''.format(self.hostname)    
        self.sql.simplequery(ipquery)
        self.networkservicegrouplist = self.sql.fetchall()
        ipquery = '''SELECT hostvalue,objectId,hostkind FROM  {0}objectnetwork WHERE hostkind = 'IPv4Network' '''.format(self.hostname)    
        self.sql.simplequery(ipquery)
        self.networkobjectnetworklist = self.sql.fetchall()
        ipquery = '''SELECT hostvalue,objectId,hostkind FROM  {0}objectnetwork WHERE hostkind = 'IPv4Address' '''.format(self.hostname)    
        self.sql.simplequery(ipquery)
        self.networkobjectlist = self.sql.fetchall()
        ipquery = '''SELECT hostvalue,objectId,hostkind FROM  {0}objectnetwork WHERE hostkind = 'IPv4Range' '''.format(self.hostname)    
        self.sql.simplequery(ipquery)
        self.networkobjectrangelist = self.sql.fetchall()
        ipquery = '''SELECT memberkind,memberObjectId,membervalue,objectId,kind FROM  {0}objectnetworkgroup '''.format(self.hostname)    
        self.sql.simplequery(ipquery)
        self.objectnetworkgrouplist = self.sql.fetchall()
        ipquery = '''SELECT memberObjectId FROM  {0}objectnetworkgroup '''.format(self.hostname)    
        self.sql.simplequery(ipquery)
        networkgroupmemberObjectIdtuple = self.sql.fetchall()
        self.networkgroupmemberObjectIdlist = set([i[0] for i in networkgroupmemberObjectIdtuple])
        #print(self.networkgroupmemberObjectIdlist)
        ipquery = '''SELECT objectId FROM  {0}objectnetworkgroup '''.format(self.hostname)    
        self.sql.simplequery(ipquery)
        networkgroupObjectIdtuple = self.sql.fetchall()
        self.networkgroupObjectIdlist = set([i[0] for i in networkgroupObjectIdtuple])
        #print(self.networkgroupObjectIdlist)
        


        