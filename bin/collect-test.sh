#!/usr/bin/ksh
# Created 07/10/2020
# Author: Domenic Troilo
# Usage: collect websphere JMX data
#        NOTE:  a file: wlp_collect_conf_HOSTNAME.py must exist and contain the domain manager 
#               connection information.  See wlp_collect_conf_HOSTNAME.py for example data
#        This file is identical to collect.sh but does not have error out to /dev/null

#
# Function Find dmgr config by port
# 
# return 1 if port is found in a config file
#
function findport {
#set -x
filelist=`find ${1}/cells/ -name serverindex.xml 2>/dev/null`
for fileid in ${filelist}
do
  grep -q ${2} ${fileid}
  if [[ $? -eq 0 ]]; then
    echo 1
    exit 1
  fi
done
echo 0
}

# Function find password in file
#
# return the ID in file based on the port
#
function findpass {

echo `cat $1 | awk -v PORT=$2 '{if ($1 ~ /user/) user=substr($2,2,length($2)-3) 
                          if ($1 ~ /port/) fport=substr($2,2,length($2)-3) 
                          if ($1 ~ /password/) password=substr($2,2,length($2)-3) 
                          if ($1 ~ /\}/) { 
                             if (PORT == fport) printf "%s",password }}'`

}

# Function find ID in file
#
# return the ID in file based on the port
#
function findid {

echo `cat $1 | awk -v PORT=$2 '{if ($1 ~ /user/) user=substr($2,2,length($2)-3) 
                          if ($1 ~ /port/) fport=substr($2,2,length($2)-3) 
                          if ($1 ~ /password/) password=substr($2,2,length($2)-3)
                          if ($1 ~ /\}/) { 
                             if (PORT == fport) printf "%s",user }}'`

}

#set -x
collectlist=$1
splunkdir=`dirname $0`
# get domain manager list
dmgrlist=`${splunkdir}/getdmgrlist.sh`
# get running java executeable
javarun=`${splunkdir}/getjava.sh`
hostname=`hostname`
# load user and password for ID collecting metrics and create sas.client.props based off current running file
if [ -e ${splunkdir}/wlp_collect_conf_${hostname}.py ]; then

  portlist=`grep port  ${splunkdir}/wlp_collect_conf_${hostname}.py | awk '{printf " %s",substr($2,2,length($2)-3)}'`
  for dmid in ${dmgrlist}
  do
    for portid in ${portlist}
    do
      found=`findport "$dmid" "$portid"`
      if [[ $found -eq 1 ]]; then
        username=`findid ${splunkdir}/wlp_collect_conf_${hostname}.py $portid`
        password=`findpass ${splunkdir}/wlp_collect_conf_${hostname}.py $portid`
        port=$portid
        #echo $dmid $port $username $password
        propshome=$dmid"/../properties/"
        dmgretc=$dmid"/../etc/"
        sed -e 's/^com.ibm.CORBA.loginSource.*/com.ibm.CORBA.loginSource=properties/' ${propshome}sas.client.props | sed -e "s/^com.ibm.CORBA.loginUserid.*/com.ibm.CORBA.loginUserid=${username}/"|sed -e "s/^com.ibm.CORBA.loginPassword.*/com.ibm.CORBA.loginPassword=${password}/" > ${splunkdir}/sas.client.props.${port}
        $javarun -Dhttps.protocols="TLSv1,TLSv1.1,TLSv1.2" -Dcom.ibm.CORBA.ConfigURL=file:${splunkdir}/sas.client.props.${port} -Dcom.ibm.SSL.ConfigURL=file:${propshome}ssl.client.props -cp ${splunkdir}/lib/jython-standalone-2.7.0.jar:${splunkdir}/lib/restConnector.jar:${splunkdir}/lib/com.ibm.ws.orb_8.5.0.jar:${splunkdir}/lib/com.ibm.ws.admin.client_8.5.0.jar:${splunkdir}/lib/com.ibm.ws.ejb.thinclient_8.5.0.jar:${splunkdir}/lib/javax.management.j2ee-api-1.1.1.jar org.python.util.jython ${splunkdir}/$collectlist $username $password $port 
      fi
    done
  done
else
  exit 255
fi
