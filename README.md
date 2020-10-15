# MerakiMVImageRecognitionandCiscoVision
Automatic process to detect age and sex for people on Meraki MV camera by using AWS Image Recognition. Then automatic trigger to Cisco Vision according to the person.






| :exclamation:  External repository notice   |
|:---------------------------|
| This repository is now mirrored at "PLEASE UPDATE HERE - add External repo URL after code review is completed"  Please inform a https://github.com/gve-sw/ organization admin of any changes to mirror them to the external repo |
## Contacts
* Eda Akturk (eakturk@cisco.com)

## Solution Components
*  Python 3.8
*  Meraki MV Camera
*  Cisco Vision
*  AWS Image Recognition
*  MongoDB


## Installation/Configuration

#### Clone the repo :
```$ git clone (link)```

#### *(Optional) Create Virtual Environment :*
Initialize a virtual environment 

```virtualenv venv```

Activate the virtual env

*Windows*   ``` venv\Scripts\activate```

*Linux* ``` source venv/bin/activate```

Now you have your virtual environment setup and ready

#### Install the libraries :

```$ pip install -r requirements.txt```


## Setup: 

*Meraki MV Camera Connection*
1. Obtain the Meraki API key and add it to env_var.py file.
```
MERAKI_API_KEY= " "
```
2. Add your Network ID and Camera Serial to the mv_mqtt.py file. 
```
NETWORK_ID = "NETWORK ID"
CAMERA_SERIAL = "CAMERA SERIAL"
```

*Cisco Vision Connection*

3. Add the URL to Cisco vision to the env_var.py file. 
```
base_url= " "
```

*Database Connection*

4. Download and Install MongoDB. 

5. Create a collection and add the Database, Cluster and Collection credentials to env_var.py.  
```
Database = " "
Cluster = " "
Collection = " "
```
*AWS Connection*

6. Create an account in AWS Console to use the Image Rekognition API. 

7. Add your access key, secret_access and region to the env_var.py file. 
```
access_key = " "
secret_access= " "
region = " "
```
*MQTT Setup*

8. In the Meraki dashboard, go to Cameras > [Camera Name] > Settings > Sense page.

9. Click to Add or edit MQTT Brokers > New MQTT Broker and add you broker information. For testing/trial you can find public broker at [here](https://github.com/mqtt/mqtt.github.io/wiki/public_brokers).

10. Add the MQTT Server settings to the mv_mqtt.py file.
```
MQTT_SERVER = " "
MQTT_PORT = " "
```
Now you have completed the setup and are ready to run the script. 

## Usage: 
Run the python script
```
    $ python mv_mqtt.py
```
When a person is detected the a snapshot will be taken by the Meraki MV snapshot API. The snapshot will be sent to the AWS API to detect the age and the sex of the person. Depending on the sex and the age different content will be sent to Cisco Vision. 
The age, sex and the time of update will be saved into the database. 



# Screenshots

![/IMAGES/CapturePOV.PNG](/IMAGES/CapturePOV.PNG)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
