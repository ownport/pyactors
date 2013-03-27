#
#   Settings
#
import os

# -------------------------------------------
# Echo server
# -------------------------------------------

# Echo server IP address
ECHO_SERVER_IP_ADDRESS = '127.0.0.1'

# Echo server IP port
ECHO_SERVER_IP_PORT = 8800

# The absolute path to the logfile of echo server
ECHO_SERVER_LOGFILE = os.path.join(os.getcwd(), 'logs/echoserver.log')

# The absolute path to the pidfile. It's required when echo server is 
# running as service
ECHO_SERVER_PIDFILE = os.path.join(os.getcwd(), 'run/echoserver.pid')

