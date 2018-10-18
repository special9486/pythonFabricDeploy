from fabric.api import local, put, run, cd, env
from time import sleep
from fabric.utils import puts

filePath = '/home/ec2-user/.jenkins/workspace/userAPI/target/'
fileName = 'user-api-server-1.0-SNAPSHOT.jar'

targetPath = "/home/ec2-user/server"

def deploy():
    with cd(targetPath):
        run("./shutdown.sh")

    for num in range(10):
        puts("Shutdown Waiting : %d" % num, None, "\n", True)
        sleep(1)

    put(filePath + fileName, targetPath)

    with cd(targetPath):
        run("set -m; ./startup.sh")

    for num in range(10):
        puts("Startup Waiting : %d" % num, None, "\n", True)
        sleep(1)

    for server in env.hosts:
        local("curl --retry 100 --retry-delay 5 --retry-connrefused 'http://" + server + ":8080/heartbeat'")

