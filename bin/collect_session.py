from wlp_collect import *
connection = connect(sys.argv[1],sys.argv[2],sys.argv[3])
collect( connection, True, "WebSphere:*,type=SessionManager","*",sys.argv[3])
collect( connection, True, "WebSphere:*,type=JSP","*",sys.argv[3])
collect( connection, True, "WebSphere:*,type=Servlet","*",sys.argv[3])
#disconnect( connection) 
