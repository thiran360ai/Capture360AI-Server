import os

def get_imei():
    try:
        imei = os.popen("adb shell service call iphonesubinfo 1 | grep -o '[0-9]*' | awk 'NR==2{print}'").read().strip()
        return imei if imei else "Could not retrieve IMEI"
    except Exception as e:
        return str(e)

print(get_imei())
