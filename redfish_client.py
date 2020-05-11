import requests
import json
import urllib3
import csv

class RestException(Exception):
    def __init__(self, status_code, message):
        super(Exception, RestException).__init__(self, message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return "RestException(status = {}, message = {})".format(self.status_code, self.message)

class RedfishClient:
    def __init__(self, bmc_ip, user, passwd):
        self.bmc_ip = bmc_ip
        self.user = user
        self.passwd = passwd

        self.base_url = 'https://{}/redfish/v1'.format(self.bmc_ip)
        auth = (self.user, self.passwd)

        # Create a persistent session with the follow settings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.session = requests.Session()
        self.session.verify = False # False to not verify the SSL certificate, which is necessary with a self-signed certificate
        self.session.auth = auth    # Configure the session to use HTTP Basic Auth
        self.session.headers.update({'Content-type': 'application/json'}) # Input for PUT/POST is always json
        self.session.headers.update({'Accept': 'application/json'})       # Always expect to receive a json response body

    def __del__(self):
        self.session.close()

    def handleResponse(self, response):
        #
        # HTTP response status codes:
        # Informational responses (100–199)
        # Successful responses (200–299)
        # Redirects (300–399)
        # Client errors (400–499)
        # Server errors (500–599)
        #
        # print(response)
        # print("response.content: {}".format(response.content))
        if(response.status_code >= 300):
            try:
                response_json = response.json()
                raise RestException(response.status_code, response_json)
            except:
                raise RestException(response.status_code, "")

        # Code 204: No Content
        if(response.status_code == 204):
            return {}

        try:
            return response.json()
        except:
            return {}

    def generic_get(self, object_type, query_string=None, **params):
        url = self.base_url + self.resources[object_type].format(**params)
        response = self.session.get(url, params=query_string)
        return self.handleResponse(response)

    def generic_post(self, object_type, data, query_string=None, **params):
        url = self.base_url + self.resources[object_type].format(**params)
        # print(url)
        response = self.session.post(url, data=json.dumps(data), params=query_string)
        return self.handleResponse(response)

    def get_system_info(self):
        response = {}
        try:
            response = self.generic_get('system', id='1')
        except Exception as e:
            print(e)
            return {'System' : []}

        boot = '{}, Target: {}'.format(response['Boot']['BootSourceOverrideEnabled'],
                                       response['Boot']['BootSourceOverrideTarget'])
        if 'BootSourceOverrideMode' in response['Boot']:
            boot += ', Mode: {}'.format(response['Boot']['BootSourceOverrideMode'])
        output = {'BiosVersion' : response['BiosVersion'],
                  'BootSourceOverride' : boot,
                  'Manufacturer' : response['Manufacturer'],
                  'Model' : response['Model'],
                  'Processor' : '{}, {}'.format(response['ProcessorSummary']['Count'], response['ProcessorSummary']['Model']),
                  'Memory' : '{} GiB'.format(response['MemorySummary']['TotalSystemMemoryGiB'])
                 }
        return {'System' : output}

    def get_manager_info(self):
        response = {}
        try:
            response = self.generic_get('manager', id='1')
        except Exception as e:
            print(e)
            return {'Manager' : []}

        output = {'ManagerType' : response['ManagerType'], 'Model' : response['Model'], 'FirmwareVersion' : response['FirmwareVersion']}
        return {'Manager' : output}

    def get_chassis_info(self):
        response = {}
        try:
            response = self.generic_get('chassis', id='1')
        except Exception as e:
            print(e)
            return {'Chassis' : []}
    
        output = {'Manufacturer' : response['Manufacturer'], 'Model' : response['Model'],
                  'Name' : response['Name'], 'PartNumber' : response['PartNumber'], 'ChassisType' : response['ChassisType']}
        return {'Chassis' : output}

    def get_sel(self):
        response = {}
        try:
            response = self.generic_get('sel', id='1')
        except Exception as e:
            print(e)
            return {'SEL' : []}

        output = []
        for sel in response['Members']:
            sel_info = { 'Name' : sel['Name'], 'Created' : sel['Created'], 'Severity' : sel['Severity']}
            if 'Message' in sel:
                sel_info['Message'] = sel['Message']
            output.append(sel_info)

        return {'SEL' : output}

    def clear_sel(self):
        response = {}
        data = {"ClearType" : "ClearAll"}    # Some client needs this
        try:
            response = self.generic_post('clear_sel', data, id='1')
        except Exception as e:
            print(e)
            return { "Clear SEL" : str(e) }

        return response

    def get_power_supply_status(self):
        response = None
        try:
            response = self.generic_get('power_supply_info', id='1')
        except Exception as e:
            print(e)
            return {'Power Supply': []}

        output = []
        for power_supply in response['PowerSupplies']:
            status = power_supply['Status']
            ps_info = {'Name' : power_supply['Name'], 'State' : status['State'], 'Model' : power_supply['Model'], \
                       'FirmwareVersion' : power_supply['FirmwareVersion']
                      }
            if 'Health' in status:
                ps_info['Health'] = status['Health']
            output.append(ps_info)

        return {'Power Supply': output}

    def get_fan_status(self):
        response = {}
        try:
            response = self.generic_get('thermal_info', id='1')
        except Exception as e:
            return {'Fan': []}

        output = []
        for fan in response['Fans']:
            status = fan['Status']

            fan_info = {'State' : status['State'], 'Reading' : '{} {}'.format(fan['Reading'], fan['ReadingUnits']),
                        'ThresholdNonCritical' : '{} to {}'.format(fan['LowerThresholdNonCritical'], fan['UpperThresholdNonCritical']),
                        'ThresholdCritical' : '{} to {}'.format(fan['LowerThresholdCritical'], fan['UpperThresholdCritical']),
                        'ThresholdFatal' : '{} to {}'.format(fan['LowerThresholdFatal'], fan['UpperThresholdFatal'])
                       }
            if 'FanName' in fan:
                fan_info['Name'] = fan['FanName']
            elif 'Name' in fan:
                fan_info['Name'] = fan['Name']
            if 'Health' in status:
                fan_info['Health'] = status['Health']
            output.append(fan_info)

        return {'Fan': output}

    def get_temperature_status(self, table_format = False, temp_file = None):
        response = {}
        try:
            response = self.generic_get('thermal_info', id='1')
        except Exception as e:
            print(e)
            return {'Temperatures': []}

        output = []
        for temp in response['Temperatures']:
            status = temp['Status']
            temp_info = {'Name' : temp['Name'], 'State' : status['State'],
                         'Temperature' : '{} C'.format(temp['ReadingCelsius']),
                         'ThresholdNonCritical' : '{} to {}'.format(temp['LowerThresholdNonCritical'], temp['UpperThresholdNonCritical']), 
                         'ThresholdCritical' : '{} to {}'.format(temp['LowerThresholdCritical'], temp['UpperThresholdCritical']), 
                         'ThresholdFatal' : '{} to {}'.format(temp['LowerThresholdFatal'], temp['UpperThresholdFatal'])
                        }
            if 'Health' in status:
                temp_info['Health'] = status['Health']
            output.append(temp_info)

        if table_format != True:
            return {'Temperatures': output}

        tempHeader = "SensorName             State Reading ThresholdNonCritical    ThresholdCritical       ThresholdFatal"
        tempFormat = "{:20s} {:>5s}{:>8s}{:>21s}{:>21s}{:>21s}"
        csvTempHeader = ",".join(tempHeader.split())

        print(tempHeader)
        csv_file = None
        if temp_file != None:
            temp_file.write(csvTempHeader + "\n")
            csv_file = csv.writer(temp_file)
        for temp in response['Temperatures']:
            status = temp['Status']
            temp_info = [ temp['Name'], status['State'], '{} C'.format(temp['ReadingCelsius']),
                          '{} to {}'.format(temp['LowerThresholdNonCritical'], temp['UpperThresholdNonCritical']),
                          '{} to {}'.format(temp['LowerThresholdCritical'], temp['UpperThresholdCritical']),
                          '{} to {}'.format(temp['LowerThresholdFatal'], temp['UpperThresholdFatal'])
                        ]
            print(tempFormat.format(*temp_info))
            if csv_file != None:
                csv_file.writerow(temp_info)

