from fabric.api import local, put, run, cd, env
from time import sleep
from fabric.utils import puts

def deploy(startup_script_path, shutdown_script_path):

    run(shutdown_script_path)

    for num in range(10):
        puts("Shutdown Waiting : %d" % num, None, "\n", True)
        sleep(1)


    run("set -m;" + startup_script_path)

    for num in range(10):
        puts("Startup Waiting : %d" % num, None, "\n", True)
        sleep(1)

    for server in env.hosts:
        local("curl --retry 100 --retry-delay 5 --retry-connrefused 'http://" + server + ":8080/heartbeat'")

