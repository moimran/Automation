# Copyright 2015 Patrick Ogenstad <patrick@ogenstad.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ip_protocol_name = {
    '0': 'ip',
    '1': 'icmp',
    '2': 'igmp',
    '3': '3',
    '4': 'ipinip',
    '5': '5',
    '6': 'tcp',
    '7': '7',
    '8': '8',
    '9': 'igrp',
    '10': '10',
    '11': '11',
    '12': '12',
    '13': '13',
    '14': '14',
    '15': '15',
    '16': '16',
    '17': 'udp',
    '18': '18',
    '19': '19',
    '20': '20',
    '21': '21',
    '22': '22',
    '23': '23',
    '24': '24',
    '25': '25',
    '26': '26',
    '27': '27',
    '28': '28',
    '29': '29',
    '30': '30',
    '31': '31',
    '32': '32',
    '33': '33',
    '34': '34',
    '35': '35',
    '36': '36',
    '37': '37',
    '38': '38',
    '39': '39',
    '40': '40',
    '41': '41',
    '42': '42',
    '43': '43',
    '44': '44',
    '45': '45',
    '46': '46',
    '47': '47',
    '48': '48',
    '49': '49',
    '50': 'esp',
    '51': 'ah',
    '52': '52',
    '53': '53',
    '54': '54',
    '55': '55',
    '56': '56',
    '57': '57',
    '58': 'icmp6',
    '59': '59',
    '60': '60',
    '61': '61',
    '62': '62',
    '63': '63',
    '64': '64',
    '65': '65',
    '66': '66',
    '67': '67',
    '68': '68',
    '69': '69',
    '70': '70',
    '71': '71',
    '72': '72',
    '73': '73',
    '74': '74',
    '75': '75',
    '76': '76',
    '77': '77',
    '78': '78',
    '79': '79',
    '80': '80',
    '81': '81',
    '82': '82',
    '83': '83',
    '84': '84',
    '85': '85',
    '86': '86',
    '87': '87',
    '88': 'eigrp',
    '89': 'ospf',
    '90': '90',
    '91': '91',
    '92': '92',
    '93': '93',
    '94': 'nos',
    '95': '95',
    '96': '96',
    '97': '97',
    '98': '98',
    '99': '99',
    '100': '100',
    '101': '101',
    '102': '102',
    '103': 'pim',
    '104': '104',
    '105': '105',
    '106': '106',
    '107': '107',
    '108': 'pcp',
    '109': 'snp',
    '110': '110',
    '111': '111',
    '112': '112',
    '113': '113',
    '114': '114',
    '115': '115',
    '116': '116',
    '117': '117',
    '118': '118',
    '119': '119',
    '120': '120',
    '121': '121',
    '122': '122',
    '123': '123',
    '124': '124',
    '125': '125',
    '126': '126',
    '127': '127',
    '128': '128',
    '129': '129',
    '130': '130',
    '131': '131',
    '132': '132',
    '133': '133',
    '134': '134',
    '135': '135',
    '136': '136',
    '137': '137',
    '138': '138',
    '139': '139',
    '140': '140',
    '141': '141',
    '142': '142',
    '143': '143',
    '144': '144',
    '145': '145',
    '146': '146',
    '147': '147',
    '148': '148',
    '149': '149',
    '150': '150',
    '151': '151',
    '152': '152',
    '153': '153',
    '154': '154',
    '155': '155',
    '156': '156',
    '157': '157',
    '158': '158',
    '159': '159',
    '160': '160',
    '161': '161',
    '162': '162',
    '163': '163',
    '164': '164',
    '165': '165',
    '166': '166',
    '167': '167',
    '168': '168',
    '169': '169',
    '170': '170',
    '171': '171',
    '172': '172',
    '173': '173',
    '174': '174',
    '175': '175',
    '176': '176',
    '177': '177',
    '178': '178',
    '179': '179',
    '180': '180',
    '181': '181',
    '182': '182',
    '183': '183',
    '184': '184',
    '185': '185',
    '186': '186',
    '187': '187',
    '188': '188',
    '189': '189',
    '190': '190',
    '191': '191',
    '192': '192',
    '193': '193',
    '194': '194',
    '195': '195',
    '196': '196',
    '197': '197',
    '198': '198',
    '199': '199',
    '200': '200',
    '201': '201',
    '202': '202',
    '203': '203',
    '204': '204',
    '205': '205',
    '206': '206',
    '207': '207',
    '208': '208',
    '209': '209',
    '210': '210',
    '211': '211',
    '212': '212',
    '213': '213',
    '214': '214',
    '215': '215',
    '216': '216',
    '217': '217',
    '218': '218',
    '219': '219',
    '220': '220',
    '221': '221',
    '222': '222',
    '223': '223',
    '224': '224',
    '225': '225',
    '226': '226',
    '227': '227',
    '228': '228',
    '229': '229',
    '230': '230',
    '231': '231',
    '232': '232',
    '233': '233',
    '234': '234',
    '235': '235',
    '236': '236',
    '237': '237',
    '238': '238',
    '239': '239',
    '240': '240',
    '241': '241',
    '242': '242',
    '243': '243',
    '244': '244',
    '245': '245',
    '246': '246',
    '247': '247',
    '248': '248',
    '249': '249',
    '250': '250',
    '251': '251',
    '252': '252',
    '253': '253',
    '254': 'tcp-udp',
    '255': '255'
}

tcp_services = {
    '7': 'echo',
    '9': 'discard',
    '13': 'daytime',
    '19': 'chargen',
    '20': 'ftp-data',
    '21': 'ftp',
    '22': 'ssh',
    '23': 'telnet',
    '25': 'smtp',
    '43': 'whois',
    '49': 'tacacs',
    '53': 'domain',
    '70': 'gopher',
    '79': 'finger',
    '80': 'http',
    '101': 'hostname',
    '109': 'pop2',
    '110': 'pop3',
    '111': 'sunrpc',
    '113': 'ident',
    '119': 'nntp',
    '139': 'netbios-ssn',
    '143': 'imap4',
    '179': 'bgp',
    '194': 'irc',
    '389': 'ldap',
    '443': 'https',
    '496': 'pim-auto-rp',
    '512': 'exec',
    '513': 'login',
    '514': 'rsh',
    '515': 'lpd',
    '517': 'talk',
    '540': 'uucp',
    '543': 'klogin',
    '544': 'kshell',
    '554': 'rtsp',
    '636': 'ldaps',
    '750': 'kerberos',
    '1352': 'lotusnotes',
    '1494': 'citrix-ica',
    '1521': 'sqlnet',
    '1720': 'h323',
    '1723': 'pptp',
    '2049': 'nfs',
    '2748': 'ctiqbe',
    '3020': 'cifs',
    '5060': 'sip',
    '5190': 'aol',
    '5631': 'pcanywhere-data'    
}

udp_services = {
    '7': 'echo',
    '9': 'discard',
    '37': 'time',
    '42': 'nameserver',
    '49': 'tacacs',
    '53': 'domain',
    '67': 'bootps',
    '68': 'bootpc',
    '69': 'tftp',
    '80': 'www',
    '111': 'sunrpc',
    '123': 'ntp',
    '137': 'netbios-ns',
    '138': 'netbios-dgm',
    '161': 'snmp',
    '162': 'snmptrap',
    '177': 'xdmcp',
    '195': 'dnsix',
    '434': 'mobile-ip',
    '496': 'pim-auto-rp',
    '500': 'isakmp',
    '512': 'biff',
    '513': 'who',
    '514': 'syslog',
    '517': 'talk',
    '520': 'rip',
    '750': 'kerberos',
    '1645': 'radius',
    '1646': 'radius-acct',
    '2049': 'nfs',
    '3020': 'cifs',
    '4789': 'vxlan',
    '5060': 'sip',
    '5510': 'secureid-udp',
    '5632': 'pcanywhere-status'    
}