import xml.etree.ElementTree as ET


class Nmapper():
    def __init__(self, source) -> None:
        self.tree = ET.parse(source)
        self.root = self.tree.getroot()

        self.hosts_data = []
        self.response = {}
        self.filter = False
    
    def parser_to_json(self):

        # Get all labels <host>
        for host in self.root.findall("host"):
            address = host.find("address").attrib['addr']
            up_ports = 0
            down_ports = 0
            filtered_ports = 0
            
            host_data = {
                'address':address
            }

            # BLOCK TRY 1 -----------
            try:
                
                self.hostname = host.find("hostnames/hostname").attrib['name']
                host_data['hostname'] = self.hostname
            
            except Exception as ex:
                host_data['hostname'] = None

            # END BLOCK TRY 1

            portsTag = host.find("ports")
            ports_data = [] # data and details of ports

            for port in portsTag.findall("port"):
                state = port.find("state").attrib['state']
                protocol = port.attrib['protocol']
                portId = port.attrib['portid']
                port_data = {
                    'port':portId,
                    'protocol':protocol,
                    'state':state
                }

                if state == 'open':
                    up_ports += 1
                elif state == 'closed':
                    down_ports += 1
                elif state == 'filtered':
                    filtered_ports += 1

                #BLOCK TRY 2
                try:
                    service = port.find("service").attrib
                    name = service['name']
                    product = service.get('product', '')
                    version = service.get('version', '')
                    extrainfo = service.get('extrainfo', '')
                    port_data['service'] = {
                        'name':name,
                        'product':product,
                        'version':version,
                        'extrainfo':extrainfo
                    }
                except Exception as ex:
                    port_data['service'] = None
                #END BLOCK TRY 2

                ports_data.append(port_data)

            host_data['ports'] = ports_data
            host_data['up_ports'] = up_ports
            host_data['down_ports'] = down_ports
            host_data['filtered_ports'] = filtered_ports
            self.hosts_data.append(host_data)
            self.response['scann'] = self.root.attrib['args']
            self.response['hosts'] = self.hosts_data

    """
    A function that return the hosts with open oports
    """
    def get_by_up_ports(self):
        ports = [host for host in self.hosts_data if host['up_ports'] > 0]
        if self.filter != True:
            self.filter = True
            self.response['hosts'] = ports
        else:
            self.response['hosts'] += ports


    """
    A function that return the hosts with domain name
    """
    def get_by_hostname(self):
        ports = [host for host in self.hosts_data if host['hostname']]
        if self.filter != True:
            self.filter = True
            self.response['hosts'] = ports
        else:
            self.response['hosts'] += ports


    def get_data(self):
        self.filter = False
        self.response['hosts'] = sorted(self.response['hosts'], key=lambda x: x['address'])
        self.response['targets'] = [{'host': host['address'], 'hostname':host['hostname']} for host in self.response['hosts']]
        return self.response