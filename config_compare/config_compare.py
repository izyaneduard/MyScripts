#!/usr/bin/python

'''
Usage ./config_compare.py -l list of boxes -c 
'''

import sys
import os

sys.path.append('/home/eduardi/python/bin')
 
#import argparse
import optparse
import subprocess
import re
import xlsxwriter
#import paramiko
#import crypto

import logging
import inspect
import pdb

import paramiko


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class SSHConnection(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, host, username, password, port=22):
        """Initialize and setup connection"""
        self.sftp = None
        self.sftp_open = False

        # open SSH Transport stream
        self.transport = paramiko.Transport((host, port))

        self.transport.connect(username=username, password=password)

    #----------------------------------------------------------------------
    def _openSFTPConnection(self):
        """
        Opens an SFTP connection if not already open
        """
        if not self.sftp_open:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.sftp_open = True

    #----------------------------------------------------------------------
    def get(self, remote_path, local_path=None):
        """
        Copies a file from the remote host to the local host.
        """
        self._openSFTPConnection()
        self.sftp.get(remote_path, local_path)

    #----------------------------------------------------------------------
    def put(self, local_path, remote_path=None):
        """
        Copies a file from the local host to the remote host
        """
        self._openSFTPConnection()
        self.sftp.put(local_path, remote_path)

    #----------------------------------------------------------------------
    
    def close(self):
        """
        Close SFTP connection and ssh connection
        """
        if self.sftp_open:
            self.sftp.close()
            self.sftp_open = False
        self.transport.close()


def main(args):

    if args.log != None :
        logFile = args.log
        print "Log file:", logFile
        f = open(str(args.log), 'w') 
        sys.stdout = f

#    if args.rm != None :
        
    boxes = args.list_name
# Checking arguments existing
    if boxes and not args.configPath :
        configPath = "/usr/he/config"
        configFiles = config_copy(boxes,configPath)
    elif not boxes and not args.configPath :
        print '\033[91m\'Error: Please provide box name.  \'\033[0m'
        sys.exit()
    else:
#        print "configPath = \'%s\'" % args.configPath
        configFiles = config_copy(boxes,args.configPath)

    compare(configFiles)


def compare(cfgFiles):
    for key in cfgFiles :
        print "box = ", key
        for value in cfgFiles[key]:
            print  "value = ", value



def config_copy(boxes, configPath):
    if boxes:
        config = {}
        for i in boxes.split(',') :
            print "Copy from " + '%s:%s'  % (i, configPath) 
            i = str(i).rstrip()
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                boxname = "%s.he.cqg" %(str(i).rstrip())
                ssh.connect(boxname, username='bvt', password='baseline')
            except paramiko.SSHException:
                print "Connection Error"

            sftp = ssh.open_sftp()
            try:
                 sftp.chdir(configPath) # /usr/he/config/
            except:
                printText = "Can't find %s:%s"  %(i, configPath)    
                print bcolors.FAIL + printText + bcolors.ENDC # %(i, configPath)
                sys.exit()

            path = "%s/cp/%s" % (str(os.getcwd()),str(i))
            if not os.path.isdir(path):
                cmd = "mkdir -p %s" % (path)
                if subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) :
                    print "path = ",path
            else:
                print bcolors.WARNING + " Already exist! " + path + bcolors.ENDC
            config[i] = []

            if not os.path.isdir(path + '/' + os.path.basename(configPath)) :
                cmd = "mkdir -p %s/%s" % (path,os.path.basename(configPath))
                subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

                for files in sftp.listdir() :
                    config[i].append(files)
                    origin = '%s/%s/%s' % (str(os.path.dirname(configPath)),str(os.path.basename(configPath)),str(files))
#                    print "orig = \'%s\'" % origin
                    dst = "%s/%s/%s" % (path,str(os.path.basename(configPath)),str(files))
                    sftp.get(origin, dst)
            elif os.path.isdir(path + '/' + os.path.basename(configPath)) :
                print bcolors.WARNING + " Already exist! " + path + '/' + os.path.basename(configPath) + bcolors.ENDC 

        ssh.close()
    return config



def read_txt(filename):
    ''' Reading file to hash
    '''
 
    with open(filename) as in_file:
        txt_file = in_file.readlines()
    return txt_file


def parse_args(argv):
    """ Parse the arguments.
    Parameters:
        argv - the list of arguments
    """
    parser = optparse.OptionParser(description='This module is for get latest checkout files')
    parser.add_option('-l', '--list', dest='list_name', help="list of modules")
    parser.add_option('-p', '--path', dest='configPath', help="Destination path of config folder")
    parser.add_option('--log', dest='log', help="Redirecting output into log file. Please provide file name")
    options, args = parser.parse_args(argv)
    return options
#    return args

if __name__ == "__main__":
    # Parse command line args
    ARGS = parse_args(sys.argv[1:])
    sys.exit(main(ARGS))
#    pdb.run(main(ARGS))
