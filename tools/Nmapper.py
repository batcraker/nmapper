import xml.etree.ElementTree as ET


class Nmapper():
    def __init__(self, source) -> None:
        self.tree = ET.parse(source)
        self.root = self.tree.getroot()

        self.hosts_data = []
    
    def parser_to_json(self):

        # Get all labels <host>
        for host in self.root.findall("host"):
            address = host.find("address").attrib['addr']
            
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
            self.hosts_data.append(host_data)

        return {
            'scann':self.root.attrib['args'],
            'hosts':self.hosts_data
        }
            