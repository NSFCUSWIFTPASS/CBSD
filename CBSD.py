# (c) 2022 The Regents of the University of Colorado, a body corporate. Created by Stefan Tschimben.
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

import json
import requests
import os
from datetime import datetime
from Logger import Logger
import argparse

# The CBSD class is used to guide the CBSD emulator
# through the steps necessary to be granted a CBRS
# channel, maintain a presence, and to relinquish it.

class CBSD(object):
    def __init__(self):
        log_time = datetime.now().strftime("%Y-%m-%d")
        log_path = os.environ["HOME"]+"/logs/"
        self.logger = Logger("CBSD", log_path, "cbsd-"+log_time+".log")
        self.sas_url_base = 'https://10.147.20.75:1443/sas-api/' # enter your SAS URL
        #self.sas_url_base = 'https://test.sas.goog/v1.2/' # enter your SAS URL
        self.header = {"content-type" : "application/json",}
        self.cert_file_path = 'Certs/client_10.147.20.114-0.crt' # point to your vendor certificate
        self.key_file_path = 'Certs/client_10.147.20.114-0.key' # point to your vendor certificate
        
        #self.cert_file_path = 'Certs/virginiatech01.cert' # point to your vendor certificate
        #self.key_file_path = 'Certs/virginiatech01.key' # point to your vendor certificate
        
        self.cert = (self.cert_file_path, self.key_file_path)
        self.ca_cert_file_path = 'Certs/ca.crt' # point to your CA certificate
        self.responseMessage = 'Success'
        self.responseData = ''

    # Function to register a CBSD
    def register(self, fcc_id, user_id, serial, callsign, category, interface, installation):
        self.logger.write_log("INFO","Registration request started.")
        sas_url = self.sas_url_base + 'registration'
        data = json.dumps({
                "registrationRequest": [{
                    "fccId": fcc_id, "userId": user_id, "cbsdSerialNumber": serial, 
                    "callSign": callsign, "cbsdCategory" : category, 
                    "airInterface": {
                        "radio_technology": interface
                        },
                    "installationParam": installation
                    }]
                })
        response = requests.post(sas_url, headers=self.header, data=data,
                                cert=self.cert, verify=self.ca_cert_file_path)
        try:
           print("Nothing")
        except Exception as e:
            self.logger.write_log("ERROR", "Request failed with: %s"%(repr(e)))
        responseCode = json.loads(response.text)['registrationResponse'][0]['response']['responseCode']
        if responseCode == 0:
            cbsdId = json.loads(response.text)['registrationResponse'][0]['cbsdId']
            self.logger.write_log("INFO","CBSD registered with SN '%s' and ID '%s'"%(serial, cbsdId))
        else:
            self.responseMessage = json.loads(response.text)['registrationResponse'][0]['response']['responseMessage']
            if json.loads(response.text)['registrationResponse'][0]['response']['responseData']:
                self.responseData = json.loads(response.text)['registrationResponse'][0]['response']['responseData']
            self.logger.write_log("ERROR","CBSD not registered with Response Code %s due to %s"%(responseCode, self.responseMessage))
        self.logger.write_log("INFO","Registration request ended.")
        return cbsdId if 'cbsdId' in locals() else "", responseCode, self.responseMessage, self.responseData

    # Function to start a Spectrum Inquiry
    def inquiry(self, cbsdId):
        self.logger.write_log("INFO","Spectrum Inquiry started.")
        sas_url = self.sas_url_base + 'spectrumInquiry'
        data = json.dumps({ "spectrumInquiryRequest": [{
                            "cbsdId": cbsdId,
                            "inquiredSpectrum": [{ 
                                "lowFrequency": 3550000000, "highFrequency": 3700000000 
                                }],
                            # "measReport": { 
                            #     "rcvdPowerMeasReports": [
                            #         { "measFrequency": 3550000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3560000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3570000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3580000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3590000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3600000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3610000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3620000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3630000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3640000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3650000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3660000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3670000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3680000000, "measBandwidth": 10000000, "measRcvdPower": -100 },
                            #         { "measFrequency": 3690000000, "measBandwidth": 10000000, "measRcvdPower": -100 } 
                            #         ] 
                            #     } 
                            }] 
                        })
        try:
            response = requests.post(sas_url, headers=self.header, data=data,
                                cert=self.cert, verify=self.ca_cert_file_path)
        except Exception as e:
            self.logger.write_log("ERROR", "Request failed with: %s"%(repr(e)))
        responseCode = json.loads(response.text)['spectrumInquiryResponse'][0]['response']['responseCode']
        if responseCode == 0:
            cbsdId = json.loads(response.text)['spectrumInquiryResponse'][0]['cbsdId']
            lowFrequency = json.loads(response.text)['spectrumInquiryResponse'][0]['availableChannel'][0]['frequencyRange']['lowFrequency']
            highFrequency = json.loads(response.text)['spectrumInquiryResponse'][0]['availableChannel'][0]['frequencyRange']['highFrequency']
            self.logger.write_log("INFO","Frequency range %s - %s selected."%(lowFrequency, highFrequency))
        else:
            self.responseMessage = json.loads(response.text)['spectrumInquiryResponse'][0]['response']['responseMessage']
            if json.loads(response.text)['spectrumInquiryResponse'][0]['response']['responseData']:
                self.responseData = json.loads(response.text)['spectrumInquiryResponse'][0]['response']['responseData']
            self.logger.write_log("ERROR","Spectrum Inquiry failed with code %s due to %s"%(responseCode, self.responseMessage))
        self.logger.write_log("INFO","Spectrum Inquiry ended.")
        return lowFrequency if 'lowFrequency' in locals() else "", highFrequency if 'highFrequency' in locals() else "",responseCode, self.responseMessage, self.responseData

    # Function to start a Grant Request
    def grant_request(self, cbsdId, eirp, low_freq, high_freq):
        self.logger.write_log("INFO","Grant request started.")
        sas_url = self.sas_url_base + 'grant'
        data = json.dumps({
                "grantRequest" : [{
                    "cbsdId" : cbsdId,
                    "operationParam" : {
                        "maxEirp" : eirp,
                        "operationFrequencyRange" : {
                            "lowFrequency" : low_freq,
                            "highFrequency" : high_freq
                            }
                        }
                    }]
                })
        try:
            response = requests.post(sas_url, headers=self.header, data=data,
                                cert=self.cert, verify=self.ca_cert_file_path)
        except Exception as e:
            self.logger.write_log("ERROR", "Request failed with: %s"%(repr(e)))
        responseCode = json.loads(response.text)['grantResponse'][0]['response']['responseCode']
        grantId = None
        grantExpireTime = None
        heartbeatInterval = None
        channelType = None
        if responseCode == 0:
            grantId = json.loads(response.text)['grantResponse'][0]['grantId']
            grantExpireTime = json.loads(response.text)['grantResponse'][0]['grantExpireTime']
            heartbeatInterval = json.loads(response.text)['grantResponse'][0]['heartbeatInterval']
            channelType = json.loads(response.text)['grantResponse'][0]['channelType']
            self.responseMessage = json.loads(response.text)['grantResponse'][0]['response']['responseMessage']
            self.logger.write_log("INFO","Grant ID '%s' with Channel Type '%s' and Heartbeat Interval of %s seconds assigned. Expires at '%s' if not renewed."%(grantId,channelType,heartbeatInterval,grantExpireTime))
        else:
            self.responseMessage = json.loads(response.text)['grantResponse'][0]['response']['responseMessage']
            if 'responseData' in json.loads(response.text)['grantResponse'][0]['response']:
                if json.loads(response.text)['grantResponse'][0]['response']['responseData']:
                    self.responseData = json.loads(response.text)['grantResponse'][0]['response']['responseData']
            self.logger.write_log("ERROR","Grant request denied with code %s due to %s"%(responseCode, self.responseMessage))
        self.logger.write_log("INFO","Grant request ended.")
        return grantId, grantExpireTime if 'grantExpireTime' in locals() else "", heartbeatInterval or 0, channelType if 'channelType' in locals() else "", responseCode, self.responseMessage, self.responseData

    # Function to start a Heartbeat Request
    def heartbeat(self, cbsdId, grantId, status):
        self.logger.write_log("INFO","Heartbeat request started.")
        sas_url = self.sas_url_base + 'heartbeat'
        data = json.dumps({
                "heartbeatRequest" :[{
                    "cbsdId": cbsdId,
                    "grantId": grantId,
                    "operationState": status
                    }]
                })
        try:
            response = requests.post(sas_url, headers=self.header, data=data,
                                cert=self.cert, verify=self.ca_cert_file_path)
        except Exception as e:
            self.logger.write_log("ERROR", "Request failed with: %s"%(repr(e)))
        responseCode = json.loads(response.text)['heartbeatResponse'][0]['response']['responseCode']
        transmitExpireTime = json.loads(response.text)['heartbeatResponse'][0]['transmitExpireTime']
        if responseCode == 0:
            #if json.loads(response.text)['heartbeatResponse'][0]['grantExpireTime']:
            #    grantExpireTime = json.loads(response.text)['heartbeatResponse'][0]['grantExpireTime']
            grantId = json.loads(response.text)['heartbeatResponse'][0]['grantId']
            cbsdId = json.loads(response.text)['heartbeatResponse'][0]['cbsdId']
            self.logger.write_log("INFO","Heartbeat request successful, new expiration time at %s."%(transmitExpireTime))
            self.responseMessage = json.loads(response.text)['heartbeatResponse'][0]['response']['responseMessage']
        else:
            self.responseMessage = json.loads(response.text)['heartbeatResponse'][0]['response']['responseMessage']
            if 'responseData' in json.loads(response.text)['heartbeatResponse'][0]['response']:
                if json.loads(response.text)['heartbeatResponse'][0]['response']['responseData']:
                    self.responseData = json.loads(response.text)['heartbeatResponse'][0]['response']['responseData']
            self.logger.write_log("ERROR","Heartbeat request denied with code %s due to %s. Transmit time expires at %s"%(responseCode, self.responseMessage, transmitExpireTime))
        self.logger.write_log("INFO","Heartbeat request ended.")
        return responseCode, transmitExpireTime, self.responseMessage, self.responseData

    # Function to start a Relinquishment Request
    def relinquish(self, cbsdId, grantId):
        self.logger.write_log("INFO","Relinquishment request started.")
        sas_url = self.sas_url_base + 'relinquishment'
        data = json.dumps({
                "relinquishmentRequest" :[{
                    "cbsdId": cbsdId,
                    "grantId": grantId,
                    }]
                })
        try:
            response = requests.post(sas_url, headers=self.header, data=data,
                                cert=self.cert, verify=self.ca_cert_file_path)
        except Exception as e:
            self.logger.write_log("ERROR", "Request failed with: %s"%(repr(e)))
        responseCode = json.loads(response.text)['relinquishmentResponse'][0]['response']['responseCode']
        if responseCode == 0:
            cbsdId = json.loads(response.text)['relinquishmentResponse'][0]['cbsdId']
            grantId = json.loads(response.text)['relinquishmentResponse'][0]['grantId']
            self.logger.write_log("INFO","Grant %s successfully relinquished."%(grantId))
        else:
            self.responseMessage = json.loads(response.text)['relinquishmentResponse'][0]['response']['responseMessage']
            if 'responseData' in json.loads(response.text)['relinquishmentResponse'][0]['response']:
                self.responseData = json.loads(response.text)['relinquishmentResponse'][0]['response']['responseData']
            self.logger.write_log("ERROR","Relinquishment failed with code %s due to %s."%(responseCode, self.responseMessage))
        self.logger.write_log("INFO","Relinquishment request ended.")
        return responseCode, self.responseMessage, self.responseData

    # Function to start a Deregistration Request
    def deregister(self, cbsdId):
        self.logger.write_log("INFO","Deregister request started.")
        sas_url = self.sas_url_base + 'deregistration'
        data = json.dumps({
            'deregistrationRequest': [{
                'cbsdId':cbsdId
                }]
            })
        try:
            response = requests.post(sas_url, headers=self.header, data=data,
                                cert=self.cert, verify=self.ca_cert_file_path)
        except Exception as e:
            self.logger.write_log("ERROR", "Request failed with: %s"%(repr(e)))
        responseCode = json.loads(response.text)['deregistrationResponse'][0]['response']['responseCode']
        if responseCode == 0:
            self.logger.write_log("INFO","User with ID %s successfully unregistered."%(cbsdId))
        else:
            self.responseMessage = json.loads(response.text)['deregistrationResponse'][0]['response']['responseMessage']
            if json.loads(response.text)['deregistrationResponse'][0]['response']['responseData']:
                self.responseData = json.loads(response.text)['deregistrationResponse'][0]['response']['responseData']
            self.logger.write_log("ERROR","Deregistration failed with code %s due to %s."%(responseCode, self.responseMessage))
        self.logger.write_log("INFO","Deregister request ended.")
        return responseCode, self.responseMessage, self.responseData
