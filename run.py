# (c) 2022 The Regents of the University of Colorado, a body corporate. Created by Stefan Tschimben.
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

import time
import argparse
import random
import sys
from CBSD import CBSD

# This function can be used to create a random serial number
def rand_serial(length):
    serial = ''
    for _ in range(length):
        # Considering only upper and lowercase letters
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        serial += (chr(random_integer))
    
    return serial

def main():
    # This application takes one argument in the form of the number of heartbeats until the emulator should relinquish the frequency and deregister
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required named arguments')
    required.add_argument(dest='heartbeats', metavar='N', type=int, nargs='?', help='Number of Heartbeats to send', default=1)
    args = parser.parse_args()

    # Update these CBSD parameters with your information
    fcc_id = "your_fcc_id"
    user_id = "your_user_id"
    serial = rand_serial(10) # or replace with your actual serial number
    callsign = "YourCallSign"
    category = "A" # your CBSD category
    interface = "E_UTRA" # change to match your interface
    installation = {"latitude": 38.881405, "longitude": -77.108941, "height": 3.0,
    "heightType": "AGL", "indoorDeployment": "True", "eirpCapability": 25,
    "antennaGain": 8 }
    eirp = 10

    new_cbsd = CBSD()

    # Send a registration request
    try:
        print('====================\n***Begin Registration Request***')
        cbsdId, responseCode, responseMessage, responseData = new_cbsd.register(fcc_id, user_id, serial, callsign, category, interface, installation)
        print("***Response from Registration:***")
        print("Serial Number: %s"%(serial))
        print("CBSD ID: %s" %(cbsdId))
        print("Response Code: %s" %(responseCode))
        print("Response Message: %s" %(responseMessage))
        print("Response Data: %s" %(responseData))
        print('***End of Registration Request***')

        if responseCode > 0:
            raise ValueError('Response Code %s. Registration denied with %s'%(responseCode, responseMessage))

    except ValueError as err:
        print(err)
        sys.exit(0)

    # sleep between requests to leave enough time for the repsonse
    time.sleep(2)

    # Send a spectrum inquiry
    try:
        print('====================\n***Begin Spectrum Inquiry***')
        low_freq, high_freq, responseCode, responseMessage, responseData = new_cbsd.inquiry(cbsdId)
        print("***Response from Registration:***")
        print("Selected Low Frequency: %s" %(low_freq))
        print("Selected High Frequency: %s" %(high_freq))
        print("Response Code: %s" %(responseCode))
        print("Response Message: %s" %(responseMessage))
        print("Response Data: %s" %(responseData))
        print('***End of Registration Request***')
        
        if responseCode > 0:
            raise ValueError('Response Code %s. Spectrum Inquiry failed with %s'%(responseCode, responseMessage))

    except ValueError as err:
        print(err)
        sys.exit(0)

    time.sleep(2)

    # Send a grant request
    try:
        print('====================\n***Begin Grant Request***')
        grantId, grantExpireTime, heartbeatInterval, channelType, responseCode, responseMessage, responseData = new_cbsd.grant_request(cbsdId, eirp, low_freq, high_freq)
        print("***Response from Grant:***")
        print("Grant ID: %s" %(grantId))
        print("Grant Expire Time: %s" %(grantExpireTime))
        print("Heartbeat Max Interval: %s" %(heartbeatInterval))
        print("Channel Type: %s" %(channelType))
        print("Response Code: %s" %(responseCode))
        print("Response Message: %s" %(responseMessage))
        print("Response Data: %s" %(responseData))
        print('***End of Grant Request***')

        if responseCode > 0:
            raise ValueError('Response Code %s. Grant Request failed with %s'%(responseCode, responseMessage))

    except ValueError as err:
        print(err)
        sys.exit(0)

    time.sleep(2)

    # Send the first heartbeat request
    try:
        print('====================\n***Begin Heartbeat Request #1')
        responseCode, transmitExpireTime, responseMessage, responseData = new_cbsd.heartbeat(cbsdId, grantId, 'GRANTED')
        print("***Response from Heartbeat:***")
        print("Transmit Expire Time: %s" %(transmitExpireTime))
        print("Response Code: %s" %(responseCode))
        print("Response Message: %s" %(responseMessage))
        print("Response Data: %s" %(responseData))
        print('***End of Heartbeat Request***')

        if responseCode > 0:
            raise ValueError('Response Code %s. Spectrum Inquiry failed with %s'%(responseCode, responseMessage))

    except ValueError as err:
        print(err)
        sys.exit(0)

    # Wait between each heartbeat request until heartbeat interval -1 second before sending the next heartbeat request
    time.sleep(heartbeatInterval-1)
    
    # Send N - 1 heartbeat requests before relinquishing the band
    for beats in range(args.heartbeats-1):
        try:
            print('====================\n***Begin Heartbeat Request #%s***'%(beats+2))
            responseCode, transmitExpireTime, responseMessage, responseData = new_cbsd.heartbeat(cbsdId, grantId, 'AUTHORIZED')
            print("***Response from Heartbeat:***")
            print("Transmit Expire Time: %s" %(transmitExpireTime))
            print("Response Code: %s" %(responseCode))
            print("Response Message: %s" %(responseMessage))
            print("Response Data: %s" %(responseData))
            print('***End of Heartbeat Request***')

            time.sleep(heartbeatInterval-1)

            if responseCode > 0:
                raise ValueError('Response Code %s. Spectrum Inquiry failed with %s'%(responseCode, responseMessage))

        except ValueError as err:
            print(err)
            sys.exit(0)

    # Send a relinquishment request
    try:
        print('====================\n***Begin Relinquishment Request***')
        responseCode, responseMessage, responseData = new_cbsd.relinquish(cbsdId, grantId)
        print("***Response from Relinquishment:***")
        print("Response Code: %s" %(responseCode))
        print("Response Message: %s" %(responseMessage))
        print("Response Data: %s" %(responseData))
        print('***End of Relinquishment Request***')

        if responseCode > 0:
            raise ValueError('Response Code %s. Spectrum Inquiry failed with %s'%(responseCode, responseMessage))

    except ValueError as err:
        print(err)
        sys.exit(0)

    time.sleep(2)

    # Send a deregistration request
    try:
        print('====================\n***Begin Deregistration Request***')
        responseCode, responseMessage, responseData = new_cbsd.deregister(cbsdId)
        print("***Response from Deregistration:***")
        print("Response Code: %s" %(responseCode))
        print("Response Message: %s" %(responseMessage))
        print("Response Data: %s" %(responseData))
        print('***End of Deregistration Request***')
        print("#####==========#####")

        if responseCode > 0:
            raise ValueError('Response Code %s. Spectrum Inquiry failed with %s'%(responseCode, responseMessage))

    except ValueError as err:
        print(err)
        sys.exit(0)

if __name__ == '__main__':
    main()
