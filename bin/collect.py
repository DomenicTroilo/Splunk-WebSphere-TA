from wlp_collect import *
#print sys.argv[1]
#print sys.argv[2]
#print sys.argv[3]
connection = connect(sys.argv[1],sys.argv[2],sys.argv[3])
  # Missing Jar file for this data
  #collect( connection, True, "WebSphere:*,type=J2EEApplication,j2eeType=J2EEApplication","*",sys.argv[3])
  #
  #Parsing not right
collect( connection, True, "WebSphere:*,type=Server,j2eeType=J2EEServer","*",sys.argv[3])
collect( connection, True, "WebSphere:*,type=JVM,j2eeType=JVM","*",sys.argv[3])
collect( connection, True, "WebSphere:*,type=Cluster","*",sys.argv[3])
collect( connection, True, "WebSphere:*,type=HAManager","*",sys.argv[3])
collect( connection, True, "WebSphere:*,type=NodeSync","*",sys.argv[3])
collect( connection, True, "WebSphere:*,type=PmiRmJmxService","*",sys.argv[3])
collect( connection, True, "WebSphere:*,type=ThreadPool","*",sys.argv[3])
  # Missing Jar file for this data
  # collect( connection, True, "WebSphere:*,type=PortletApplication","*",sys.argv[3])
  # Application list does not need to be checked on often.... create seperate input for this one.
  #collect( connection, True, "WebSphere:*,type=Application","*",sys.argv[3])
collect( connection, True, "WebSphere:*,type=NodeAgent","*",sys.argv[3])
  # No data found
  #collect( connection, True, "WebSphere:*,type=WLMAppServer","*",sys.argv[3])
#disconnect( connection)
