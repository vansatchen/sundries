#!/usr/bin/python

import requests

getToken = requests.post('http://api.ufanet.platform24.tv/v2/auth/device', json={"device_id": "3da6bc30-f85f-402a-b004-7e9a8a0022c7"})

#print("Status code: ", response.status_code)
# Get token
accessToken = getToken.json().get('access_token')

# Get channels
paramsChan = {"includes": "images.whiteback", "access_token": accessToken}
getChannels = requests.get('http://api.ufanet.platform24.tv/v2/channels', params=paramsChan)
#print(getChannels.json())
with open("channels.txt", "w") as file:
    for el in getChannels.json():
        for key in el:
            file.write(key + " - " + str(el[key]) + '\n')
            if key == 'is_purchased':
                file.write(" " + '\n')
