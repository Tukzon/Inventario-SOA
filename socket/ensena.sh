#!/bin/bash
echo "Starting ssh tunnel to bus"
echo "=========================="
sshpass -p ${BUSPASS} ssh -p ${BUSPORT} -tt -L *:${LOCALPORT}:${LOCALHOST}:${LOCALPORT} -o StrictHostKeyChecking=no ${BUSUSER}@${BUSHOST} 'echo "Logged as:" `whoami`; /bin/bash'