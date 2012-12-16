#
#   This module provides utilities for working with configuration
#   FERnfs application.
#

import sys

#
#   Reads a configuration file and returns a dictionary with
#   values mapped to their attribute names or None if file is 
#   not valid or could not be read.
#@param fileName
#@return
#
def readConfigFile(fileName):
    params = {}
    try:
        for line in open(fileName, "r"):
            line = line.strip()
            if line.startswith("#") or line is "":
                continue
            parts = line.split( "=", 1)
            params[parts[0].strip()] = parts[1].strip()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        return None
    except IndexError:
        print "Invalid configuration file."
        return None

    return params


if __name__ == "__main__":
    print readConfigFile(sys.argv[1])
