from wlp_collect import *
connection = connect(sys.argv[1],sys.argv[2],sys.argv[3])
collect( connection, True, "WebSphere:*,type=Application","*",sys.argv[3])
#disconnect( connection)

