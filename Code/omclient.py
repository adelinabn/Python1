"""

Network client that connects to a server and sends file contents.

"""

###############
#   imports   #
###############

import socket
import sys


#######################
#  Client functions   #
#######################

def run():
    """
    runs a client application that connects to a server and sends files
    as strings

    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    try:
        print("Connecting to %s port %s" % server_address)
        sock.connect(server_address)
    except:
        print("Could not connect to %s port %s" % server_address)
        return

    # File loop
    while True:
        try:
            # Get input filename
            filename = \
                input("What file would you like to send? (CTRL-D to quit)\n")
            if not filename:
                break
            # Read file
            message = open(filename).read()
            # Send data
            print("Sending \"%s\"..." % filename)
            sock.sendall(message.encode())
            # Receive data
            result = sock.recv(4096).decode()
            # Write result to file if required
            if result.startswith("error:"):
                _, msg = result.split("error:")
                print("Error received: %s" % msg)
            else:
                print("Received result:\n%s\n" % result)
                if getinput( \
                       "Would you like to save this to a file? (y - yes)" \
                   ) == "y":
                    write_to_file(result)
        except (FileNotFoundError, IsADirectoryError):
            print("Please enter a valid filename!")
        except socket.error:
            print("Disconnected from server!")
            break
        except EOFError:
            break

    print('Closing socket...')
    sock.close()

def getinput(prompt):
    """
    gets a line of input from stdin and returns the value stripped
    of whitespace

    """
    if not prompt == "":
        print(prompt)
    ans = sys.stdin.readline()
    if not ans:
        return ""
    return ans.strip()

def write_to_file(string):
    """
    writes string to a file (filename is queried from user)

    """
    while True:
        outfile = getinput("Enter the filename (CTRL-D or "" to cancel):")
        if not outfile == "":
            try:
                open(outfile, "w").write(string)
                print("File written successfully!")
                break
            except:
                print("Please enter a valid filename!")
        else:
            print("File write cancelled.")
            break


#################
#  Run client   #
#################

if __name__ == '__main__':
    run()
