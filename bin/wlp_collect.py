import sys
import os
import socket
import string
import re

from javax.management.remote import JMXConnector
from javax.management.remote import JMXConnectorFactory
from javax.management.remote import JMXServiceURL
from javax.management import MBeanAttributeInfo
from javax.management import MBeanInfo
from javax.management import MBeanNotificationInfo
from javax.management import MBeanServerConnection
from javax.management import MBeanInfo
from javax.management import ObjectName
from javax.management import Notification
from javax.management import NotificationListener
from java.lang import String
 
from jarray import array
sys.stdout.softspace=False;
#
# load connection configuration data from host specific config file.
#
#package = "wlp_collect_conf_" + socket.gethostname()
#pkg_name = "Config"
#Config = getattr(__import__(package, fromlist=[pkg_name]), pkg_name)

#from wlp_collect_conf import Config
#envetc=os.environ['dmgretc']
sys.path.append("./Lib")


def make_printable(str):
    # """Replace non-printable characters in a string."""

    # the translate method on str removes characters
    # that map to None from the string
    return ''.join([c for c in str if ord(c) > 31 or ord(c) == 9])

def connect(user,password,port):
  """
    param : none BUT uses the Config object define in wlp_collect_conf.py
    result: return a connection object
    note  : use simple connect method
  """
  credentials = array([user,password],String)
  environment = {JMXConnector.CREDENTIALS:credentials}
  jmxServiceUrl = JMXServiceURL('service:jmx:iiop://localhost/jndi/corbaname:iiop:localhost:'+port+'/WsnAdminNameService#JMXConnector');
  connector = JMXConnectorFactory.connect(jmxServiceUrl,environment);
        
  return connector
 
def disconnect( connector):
  """
    param : a connection object (return by connect())
    result: none
  """
  connector.disconnect()
 
def collect( connector, details = False,objectName = "WebSphere:*", attributeName = "*",dmgr_port = 0):
  """
    param1: connection object (return by connect() function)
    param2: output with or without details (True|False)
    param3: mbean object like "WebSphere:type=JvmStats,*"
    param4: attribute to retrieve in the mbean object
    result: return an array of mbeans objects found
  """
  mconnection = connector.getMBeanServerConnection()
  #print dir( mconnection)
  # "WebSphere:type=endpoint,*"
  mbeans = mconnection.queryNames( ObjectName( objectName), None).toArray()
  for mbean in mbeans:
    sys.stdout.softspace=False
    print ("%s") % ("{"),
    bean_list=str(mbean).split(',')
  #  print ("BEGIN bean_list ---------------------------------------")
    for beandata in bean_list:
      bean_items=beandata.split('=')
      webspheretest=string.split(bean_items[0],':')
      if len(webspheretest) == 2:
        sys.stdout.softspace=False
        print ("\"mbean_domain\":\"%s\",") % ( webspheretest[0]),
        sys.stdout.softspace=False
        print ("\"mbean_property_%s\":\"%s\",") % ( webspheretest[1],bean_items[1]),
      else: 
        sys.stdout.softspace=False
        print ("\"mbean_property_%s\":\"%s\",") % ( bean_items[0],bean_items[1]),
      

    # --- printing attributes
    mbean_info = mconnection.getMBeanInfo( mbean)
    mbean_class = mbean_info.className
    mbean_attributes = mbean_info.getAttributes()
    attrnum = len( mbean_info.attributes)
    count = 1
    mycomma=","
    for attribute in mbean_attributes:
      #print ("BEGIN mbean_list ---------------------------------------")
      name = attribute.name
      bvalue = mconnection.getAttribute( mbean, name)
      btype = attribute.type
      #print ("mbean type %s ---------------------------------------") % (str(btype))
      if count == attrnum: 
        mycomma=""
      if (str(btype) == "javax.management.j2ee.statistics.Stats" and bvalue is not None):
        sys.stdout.softspace=False
        print ("\"%s\":{") % ( name),
        stats_data=str(bvalue).partition("{")[2].partition("}")[0]
        stats_list=stats_data.split('name=')
        #print stats_list
        count3=1
        mycomma3=","
        for statsdata in stats_list:
          if (len(stats_list) == count3):
            mycomma3=""
          data_list=statsdata.split(', ')
          count2=1    
          mycomma2=","
          for dataout in data_list:
            if (len(data_list) == count2):
              mycomma2=""
            count2=count2+1
            if (len(dataout) != 1):
              #print ("Length %s Dataout %s") % (len(dataout),str(dataout))
              #print ("data1 %s") % data_list[1]
              dataout2=dataout.split('=')
              if len(dataout2) == 1:
                sys.stdout.softspace=False
                print ("\"%s\":{") % (dataout2[0]),
              else:
                sys.stdout.softspace=False
                if (make_printable(dataout2[1]).isdecimal()):
                  print ("\"%s\":%d%s") % ( dataout2[0],int(make_printable(dataout2[1])),mycomma2),
                else:
                  print ("\"%s\":\"%s\"%s") % ( dataout2[0],make_printable(dataout2[1]),mycomma2),
          if count3 != 1:
            sys.stdout.softspace=False
            print ("%s%s") % ("}",mycomma3),
          count3=count3+1
        #print ("-----")
        sys.stdout.softspace=False
        print ("}%s") % ( mycomma),
      elif (str(btype) == "[Ljava.lang.String;" and bvalue is not None):
        sys.stdout.softspace=False
        print ("\"%s\":[\"%s\"]%s") % ( name,make_printable(re.sub(r'"','\\"',str(','.join(bvalue)))),mycomma),
      elif (str(btype) == "java.lang.String" and bvalue is not None):
        sys.stdout.softspace=False
        print ("\"%s\":\"%s\"%s") % ( name,make_printable(re.sub(r'"','\\"',str( bvalue.encode('ascii','ignore')))),mycomma),
      elif (bvalue is not None):
        sys.stdout.softspace=False
        print ("\"%s\":%s%s") % ( name,str( bvalue).lower(),mycomma),
      else: 
        sys.stdout.softspace=False
        print ("\"%s\":%s%s") % ( name,"null",mycomma),
      count=count+1
  #    print ("END mbean_list ---------------------------------------")
    sys.stdout.softspace=False
    print (",\"%s\":%s%s") % ("dmgr_port",dmgr_port,"}")
  #  print ("END bean_list ---------------------------------------")
  return mbeans
