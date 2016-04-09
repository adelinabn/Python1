"""

Multithreaded OpenMath server that evaluates OpenMath strings.

"""

###############
#   imports   #
###############

import socket
import _thread
import sys
from openmath import *


########################
#   thread functions  #
########################

def client_thread(threadname, connection):
    """
    handles a client connection

    """
    print("handling client: %s" % str(threadname))
    try:
        while not shutdown:
            # Receive the data from the connection
            data = connection.recv(4096).decode()

            # Handle received data
            if data:
                print("%s: received data" % str(threadname))
                # Parse the string as an OpenMath string
                try:
                    omobj = ParseOMstring(data)
                    # Prettify string to send
                    result = OMprettystring(OMobject(omobj), 0)
                except Exception as e:
                    result = "error:" + str(e)
                # Send result
                print("%s: sending data back to the client" % str(threadname))
                connection.sendall(result.encode('utf-8'))
            else:
                # No data received
                print("%s: no data received" % str(threadname))
                break
    finally:
        # Clean up the connection
        connection.close()
        print("%s: closed connection" % str(threadname))

def keyboard_thread(threadname, keyword):
    """
    wait for keyword input from keyboard then shuts down server

    """
    # Read keyboard input
    key_in = sys.stdin.readline()
    while key_in and not key_in.strip() == keyword:
        key_in = sys.stdin.readline()
    # Set shutdown flag
    global shutdown
    shutdown = True
    print("%s: server shutdown initiated" % threadname)


##################
#   run server   #
##################

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)

# Global flag for to stop all threads
shutdown = False

# Bind the socket to the port
server_address = ('localhost', 10000)
print("starting up OpenMath server on %s port %s" % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Start keyboard thread
quit_keyword = ":q"
_thread.start_new_thread(keyboard_thread, ("keyboard", quit_keyword))
print("type CTRL-D or \":q\" to shutdown server")

# Connection loop
while not shutdown:
    try:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        print('connected to', client_address)
        # Start new thread that handles client
        _thread.start_new_thread(client_thread, (client_address, connection))
    except socket.timeout:
        continue

# Shutdown socket read and write
sock.shutdown(socket.SHUT_RDWR)
