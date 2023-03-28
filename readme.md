
# CBSD Emulator

This code emulates the communication occurring between a Spectrum Access System (SAS) and a Citizens Broadband Radio Service Device (CBSD).

## Documentation

Communication between a SAS and a CBSD consists of the following 6 components. Note that each request needs to include the required certificates, which are not included in this repository. Each response to a request either contains a response code 0 if the request was a success or a different response code with a message describing why the request failed.

### Registration

Registering a CBSD requires:
* FCC ID
* User ID
* CBSD Serial Number
* Call Sign
* CBSD Category
* Air Interface Radio Technology
* Installation Parameters

A registration requests returns:
* A response code
* A CBSD ID

### Spectrum Inquiry

A spectrum inquiry request consists of:
* The previously received CBSD ID
* The low to high frequency range of the spectrum of interest
* The received power measurement report

The spectrum inquiry response consists of:
* A response code
* A frequency range of available channels

### Grant Request

A grant request consists of:
* CBSD ID
* Operational parameters, such as:
    * EIRP
    * Frequency range (low and high)

A grant request responds with:
* A response code
* Grant ID
* Grant Expiration Time
* Heart Beat Interval
* Channel Type

### Heartbeat Request

Depending on the Grant Expiration and Heart Beat Interval provided by the response to the grant request, a Heartbeat Request needs to be sent within certain intervals.

A Heartbeat Request consists of:
* CBSD ID
* Grant ID
* Operational Status

The first response to a grant request response is a heartbeat request with the status 'GRANTED'. After this first heartbeat, the CBSD can begin transmitting. All subsequent heartbeat requests need the status 'AUTHORIZED' for a successful response.

The response to a successful Heartbeat Request contains:
* A reponse code
* Transmit Expiration Time
* Grant ID
* CBSD ID

If the heartbeat request is unsuccessful it can be due to an incumbent moving into the channel, resulting in a status such as 'TERMINATED GRANT', requiring the CBSD to terminate operation associated with this Grant within 60 seconds after the value of the transmitExpireTime parameter expires.

### Relinquishment Request

A Relinquishment Request needs to be sent after the CBSD stops transmitting. The request only contains the CBSD ID and the Grant ID and responds either with a response code 0 plus CBSD ID and Grant ID or an error with message.

### Deregistration Request

Finally, deregister the CBSD by sending it CBSD ID to the deregistration url. Expect a response code 0 for success.

## Usage

Note that this repository does not contain the certificates necessary to connect to a SAS. In CBSD.py change:
* line 12 to point at your SAS URL,
* line 14 for your vendor .cert,
* line 15 for your vendor .key,
* and line 17 for your ca.cert file.
If you would like to change the location where log files are written to, change lines 10 and 11 as well.

In run.py edit lines 25 to 34 with your specific deployment parameters.

The emulator can be run with `python3 run.py N` where N represents the number of heartbeats you want to send out with your emulator before relinquishing the grant and deregistering.

## Raspberry Pi LEDs

When the code is executed on a Raspberry Pi, it will attempt to control one LED on GPIO 18 and one LED connected to GPIO 16, which is typically used for SD Card access. Use a 330 ohm resistor for each light. Depending on the function being executed, the LED will flash on 4 different states:
00 Once the Raspberry Pi is registered as a CBSD, both LEDs will change to a solid light and flash on heartbeats
01 When transmitting at a lower power, the GPIO 18 light will be on and the GPIO 16 light will be off
02 When moving to a different channel, the GPIO 16 light will be on and the GPIO 18 light will be off
03 When the CBSD is not transmitting both lights will be off
