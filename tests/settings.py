#
#   Settings
#
import os

# During early development, the debug mode can be very helpful.
# In this mode, Bottle is much more verbose and provides helpful 
# debugging information whenever an error occurs. It also 
# disables some optimisations that might get in your way and adds 
# some checks that warn you about possible misconfiguration.
# Here is an incomplete list of things that change in debug mode:
#
# - The default error page shows a traceback.
# - Templates are not cached.
# - Plugins are applied immediately.
#
# Just make sure not to use the debug mode on a production server.
DEBUG_MODE = True

# The absolute path to the logfile of http server
HTTP_SERVER_LOGFILE = os.path.join(os.getcwd(), 'logs/http_server.log')

# The absolute path to the pidfile. It's required when http server is 
# running as service
HTTP_SERVER_PIDFILE = os.path.join(os.getcwd(), 'run/http_server.pid')
