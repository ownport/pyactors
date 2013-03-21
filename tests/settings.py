#
#   Settings
#
import os

# Simple server IP address
SIMPLE_SERVER_IP_ADDRESS = '127.0.0.1'

# Simple server IP port
SIMPLE_SERVER_IP_PORT = 8800

# The absolute path to the logfile of simple server
SIMPLE_SERVER_LOGFILE = os.path.join(os.getcwd(), 'logs/simple_server.log')

# The absolute path to the pidfile. It's required when simple server is 
# running as service
SIMPLE_SERVER_PIDFILE = os.path.join(os.getcwd(), 'run/simple_server.pid')
