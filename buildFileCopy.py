import sys, os
from shutil import copyfile

argumentList = sys.argv
jobName = argumentList[1]
buildNo = argumentList[2]
filePath = argumentList[3]

jobDirPath = "/home/ec2-user/build/" + jobName
targetFilePath = jobDirPath + "/" + buildNo
currentFilePath = jobDirPath + "/current"

print("job dir path => %s" % jobDirPath)

if not os.path.exists(jobDirPath):
    os.makedirs(jobDirPath)

if not os.path.exists(targetFilePath):
    os.makedirs(targetFilePath)

if not os.path.exists(currentFilePath):
    os.makedirs(currentFilePath)

copyfile(filePath, targetFilePath + "/" + jobName + ".jar")
copyfile(filePath, currentFilePath + "/" + jobName + ".jar")