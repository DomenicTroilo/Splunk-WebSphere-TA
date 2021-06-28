# Created 07/10/2020
# Author: Domenic Troilo
# Usage: get list of domainmanager based off process list
dmlist=`ps -ef | grep -v grep |grep dmgr$ | awk '{counter=split($0, array, " "); printf " %s",array[counter-3];}'`
echo $dmlist
