# Created 07/10/2020
# Author: Domenic Troilo
# Usage: echo Websphere Domain Manager java process based off running process

javahome=`ps -eo args | grep dmgr$ | tail -1  |  cut -d' ' -f1`
#javahome=`dirname $0`/../java/jre/bin/java
$javahome  -version 2>&1 | grep -q 'version "1.6'
if [ $? -eq 0 ]
then
  javahome=~splunk/java/bin/java
fi
echo $javahome
