import Server
import json
import requests
import base64
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

server_url = "192.168.3.60"
server_user = "super"
server_pwd = "Password"
server_ssl = False

class get_all_fw_policy():

    def __init__(self, url, user, password, sslVerify=False):
        self.root_url = url
        self.user = user
        self.password = password
        self.sslVerify = sslVerify

    def login(self):
       session = requests.session()
       bstr = self.user + ':' + self.password
       #auth = base64.b64encode(bytes(bstr), 'utf-8')
       bstr = bstr.encode('utf-8')
       auth = base64.b64encode(bstr)
       auth = auth.decode('utf-8')
       URL = self.root_url + '/api/space/user-management/login'
       headers = {'Authorization': 'Basic ' + auth}
       response = session.post(url=URL, headers= headers, verify=self.sslVerify)
       if response.status_code == 200:
         self.session = session
         return self
       else:
         raise Exception("Error: code = %d, text = %s" % (response.status_code, response.text))

    def initialize(self):
        #self.session.prepare_request()
        myserver = 'https://' + server_url
        self.server_instance = Server.Server(myserver, server_user, server_pwd, False)
        self.server_instance.login()

    def get_duplicate_addresses(self):
        resp_dup = self.showDuplicates(None)
        return resp_dup.text

     # function to show duplicate
    def showDuplicates(self, uriContext):
        Path = self.root_url + "/api/juniper/sd/address-management/addresses/show-duplicates"
        header = { 'Accept':'application/json' }
        self.server_instance.session.get(Path)
        response = self.server_instance.session.get(url=Path, headers=header, verify=False)
        return response

    def getAddress(self, id):
        Path = self.server_instance.root_url + "/api/juniper/sd/address-management/addresses/%s" % (id)
        header = { 'Accept':'application/vnd.juniper.sd.address-management.address+json;version=1;q=0.01' }
        response = self.server_instance.session.get(url=Path, headers=header, verify=False)
        return response

    def merge_dup_addresses(self, page):
        Path = self.server_instance.root_url + "/api/juniper/sd/address-management/addresses/merge"
        header = {'Content-Type':'application/json', 'Accept':'application/json'}
        input_param = page
        payload = json.dumps(input_param) if input_param is not None else None
        response = self.server_instance.session.post(url=Path, data=payload, headers=header, verify=False)
        return response

    def showDuplicatesServices(self, uriContext):
        Path = self.server_instance.root_url + "/api/juniper/sd/service-management/services/show-duplicates"
        header = {'Accept': 'application/vnd.juniper.sd.show-duplictaes+json;version=1;q=0.01'}
        response = self.server_instance.session.get(url=Path, headers=header, verify=False)
        return response

    def mergeService(self, page):
        Path = self.server_instance.root_url + "/api/juniper/sd/service-management/services/merge"
        header = {'Content-Type': 'application/json',
                  'Accept': 'application/json'}
        input_param = page
        payload = json.dumps(input_param) if input_param is not None else None
        response = self.server_instance.session.post(url=Path, data=payload, headers=header, verify=False)
        return response

if __name__ == "__main__":
    SD_API_Inst = get_all_fw_policy('https://'+server_url, server_user, server_pwd)
    SD_API_Inst.login()
    SD_API_Inst.initialize()

    resp_status_show_dup = SD_API_Inst.get_duplicate_addresses()
    resp_status_show_dup = json.loads(resp_status_show_dup)
    for ids in resp_status_show_dup['duplicate-list']['duplicates']:
            dup_address_id_list = ids['idList']
            first_id = dup_address_id_list[0]
            print(first_id)
            address_get_resp = SD_API_Inst.getAddress(first_id)
            address_detail = json.loads(address_get_resp.text)
            print(address_detail)
            merge_address_name = address_detail['address']['name']
            print(merge_address_name)
            post_body = {
                "merge-request": {
                    "name": merge_address_name,
                    "description": "",
                    "is-group-merge": "false",
                    "ids": dup_address_id_list
                }
            }
            merge_address_resp = SD_API_Inst.merge_dup_addresses(post_body)
            ##Check POST response status message
            print(merge_address_resp)