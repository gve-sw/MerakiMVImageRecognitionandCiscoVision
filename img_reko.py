import csv
import boto3
from env_var import access_key, secret_access, region
from cisco_vision import child, male, female, default

from update_db import database_update

# Client is needed to make the AWS connection
client = boto3.client('rekognition',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_access,
                      region_name=region)

def aws_img_recognition (photo):
    with open(photo, 'rb') as source_image:
        # convert the image to bytes to bass to img recognition api
        source_bytes = source_image.read()
        response = client.detect_faces(
            Image={
                'Bytes': source_bytes,
            },
            Attributes=["ALL", "DEFAULT"]
        )
        try:
            # Gets the age and the gender of all the faces from the Amazon API response
            for person in response['FaceDetails']:
                #print(person)
                try:
                    age = person['AgeRange']
                except:
                    age = "na"

                try:
                    sex = person['Gender']
                except:
                    sex = "na"

                # average age is calculated
                average_age = int((age['Low'] + age['High']) / 2)
                # sex is taken from the api response
                sex = (sex['Value'])

                #tag value is needed for the Cisco Vision Api Calls
                if average_age < 18:
                    tag = 'Children'
                    child()
                elif average_age < 38:
                    if gender == 'Male':
                        tag = 'VYPE'
                        male()
                    else:
                        tag = 'LYFT'
                        female()
                else:
                    tag = 'Default'
                    defalut()

                database_update(age, sex, tag)
                print(f"Age: {average_age}, Sex: {sex}")
                

        except:
            print('There is no response from Amazon Image Recognition')


