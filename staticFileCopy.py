import sys, os
from shutil import copyfile
import tarfile
import zipfile

def extract_file(path, to_directory='.'):
    if path.endswith('.zip'):
        opener, mode = zipfile.ZipFile, 'r'
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        opener, mode = tarfile.open, 'r:gz'
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        opener, mode = tarfile.open, 'r:bz2'
    else:
        raise ValueError, "Could not extract `%s` as no appropriate extractor is found" % path

    cwd = os.getcwd()
    os.chdir(to_directory)

    try:
        file = opener(path, mode)
        try: file.extractall()
        finally: file.close()
    finally:
        os.chdir(cwd)

argumentList = sys.argv
jobName = argumentList[1]
buildNo = argumentList[2]
filePath = argumentList[3]

jobDirPath = "/home/ec2-user/build/" + jobName
targetFilePath = jobDirPath + "/" + buildNo
syncDevPath = jobDirPath + "/syncDev"

print("job dir path => %s" % jobDirPath)

if not os.path.exists(jobDirPath):
    os.makedirs(jobDirPath)

if not os.path.exists(targetFilePath):
    os.makedirs(targetFilePath)

if not os.path.exists(syncDevPath):
    os.makedirs(syncDevPath)

copyfile(filePath, targetFilePath + '/staticResources.tar.gz')
extract_file(filePath, syncDevPath)

