import requests
import shutil
with open("./Stock Pictures.csv", "r") as csv:
    for x in csv.readlines():
        x = x.replace("\n", "").split(",")
        res = requests.get(x[2], stream=True)
        if res.status_code == 200:
            with open("{}.jpg".format(x[0]), 'wb') as f:
                shutil.copyfileobj(res.raw, f)
        else:
            print('Image Couldn\'t be retrieved')
