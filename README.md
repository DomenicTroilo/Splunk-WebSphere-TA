# Splunk-WebSphere-TA
Collect JMX Data From WebSphere Instances

This TA is compatible with the ITSI Application KPI searches.  It requires the installation of the "splunk add on for ibm websphere application server" to collect the meta data required for applicable KPI searches. This executes on a Splunk Univerisal Forwarder, not a Splunk Server.  

The TA will pull it's configuration from the file bin/wlp_collect_conf_HOSTNAME.py, you require a configuration for each host you run the TA on. See the example file for details.  Note passwords stored in this file are currently NOT encrypted.

Author: Domenic Troilo
