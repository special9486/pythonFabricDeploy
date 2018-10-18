from fabric.api import local
from fabric.utils import puts
import requests, json
from time import sleep

############################################## Configuration ###########################################################
remoteServerUserId = "ec2-user"
keyPath = "/home/ec2-user/aws/ec2-seoul.pem"
startupScriptPath = "/home/ec2-user/server/startup.sh"
shutdownScriptPath = "/home/ec2-user/server/shutdown.sh"

elbTargetGroupArn = "arn:aws:elasticloadbalancing:ap-northeast-2:373660362923:targetgroup/targetGroupUserAPI/ee78bc56adada097"

############################################## //Configuration ###########################################################

cmdTargetHealth = "aws elbv2 describe-target-health --target-group-arn " + elbTargetGroupArn
cmdTargetInfo = "aws ec2 describe-instances --instance-id "
cmdDeregistTarget = "aws elbv2 deregister-targets --target-group-arn " + elbTargetGroupArn + " --targets Id="
cmdRegistTarget = "aws elbv2 register-targets --target-group-arn " + elbTargetGroupArn + " --targets Id="
serverList = []

def setServerListforELB():
    targetHealthResult = local(cmdTargetHealth, capture=True)
    puts(targetHealthResult, None, "\n", True)
    targetHealthJson = json.loads(targetHealthResult)

    for data in targetHealthJson['TargetHealthDescriptions']:
        if data['TargetHealth']['State'] == "healthy":
            targetInfoResult = local(cmdTargetInfo + data['Target']['Id'], capture=True)
            puts(targetInfoResult, None, "\n", True)
            targetInfoJson = json.loads(targetInfoResult)
            instanceInfo = targetInfoJson['Reservations'][0]['Instances'][0]
            serverList.append({"id":data['Target']['Id'], "port":data['Target']['Port'], "ip":instanceInfo['PrivateIpAddress']})

def unbindELB(instance_id):
    local(cmdDeregistTarget + instance_id)

    while True:
        sleep(10)
        targethealthInfo = getTargetHealthInfo(instance_id=instance_id)
        puts(targethealthInfo, None, "\n", True)
        if targethealthInfo['TargetHealth']['State'] == "unused":
            break

def bindELB(instance_id):
    local(cmdRegistTarget + instance_id)

    while True:
        sleep(3)
        targethealthInfo = getTargetHealthInfo(instance_id=instance_id)
        puts(targethealthInfo, None, "\n", True)
        if targethealthInfo['TargetHealth']['State'] == "healthy":
            break

def getTargetHealthInfo(instance_id):
    targetHealthInfoResult = local(cmdTargetHealth + " --targets Id=" + instance_id, capture=True)
    targetHealthInfoJson = json.loads(targetHealthInfoResult)
    return targetHealthInfoJson["TargetHealthDescriptions"][0]


def start(elb_use_yn, server_ip):
    if elb_use_yn == "Y":
        setServerListforELB()
    else:
        serverList.append({'ip':server_ip})

    if len(serverList):
        for server in serverList:
            if elb_use_yn == "Y":
                unbindELB(instance_id=server['id'])

            puts("########################## Deploy Start Server : %s ###############################" % server['ip'], None, "\n", True)
            command = "fab -H " + server['ip'] + " -u " + remoteServerUserId + " -i " + keyPath + " -f serverDeploy.py deploy:startup_script_path='"+startupScriptPath +"',shutdown_script_path='"+ shutdownScriptPath +"'"
            local(command)
            puts("////////////////////////// Deploy Finish Server : %s //////////////////////////////" % server['ip'], None, "\n", True)

            if elb_use_yn == "Y":
                bindELB(instance_id=server['id'])
    else:
        puts("Server List is empty....", None, "\n", True)




