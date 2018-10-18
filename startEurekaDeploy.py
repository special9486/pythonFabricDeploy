from fabric.api import local
from fabric.utils import puts

serverList = ['13.209.202.87']
userId = "ec2-user"
keyPath = "/home/ec2-user/aws/ec2-seoul.pem"

def start():
    for server in serverList:
        puts("########################## Deploy Start Server : %s ###############################" % server, None, "\n", True)
        local("fab -H " + server + " -u " + userId + " -i " + keyPath + " -f eurekaDeploy.py deploy")
        puts("////////////////////////// Deploy Finish Server : %s //////////////////////////////" % server, None, "\n", True)

