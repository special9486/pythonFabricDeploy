# pythonFabricDeploy
fabric을 이용한 배포 스크립트 예제

jenkins build script example

mvn clean package
cd ~/script
python buildFileCopy.py userAPI ${BUILD_NUMBER} ~/.jenkins/workspace/${JOB_NAME}/target/user-api-server-1.0-SNAPSHOT.jar
fab -f startUserApiDeploy.py start:elb_use_yn='N',server_ip=$SERVER_IP
