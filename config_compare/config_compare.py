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
#import xlsxwriter
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
    boxPath = {}
# Checking arguments existing
    if boxes and not args.configPath :
        configPath = "/usr/he/config"
        configFiles = config_copy(boxes,configPath)
        for box in boxes.split(',') :
            boxPath[box] = configPath
    elif not boxes and not args.configPath :
        print '\033[91m\'Error: Please provide box name.  \'\033[0m'
        sys.exit()
    else:
#        print "configPath = \'%s\'" % args.configPath
        configFiles = config_copy(boxes,args.configPath)
        for box in boxes.split(',') :
            boxPath[box] = args.configPath

    compare(configFiles, boxPath)


def compare(cfgFiles, boxPath):
    ignoreFile = "./ignore"
    inter = set(cfgFiles[cfgFiles.keys()[0]]).intersection(cfgFiles[cfgFiles.keys()[-1]])
    
    noMatch = {}
    for key in cfgFiles :
        noMatch[key] = [x for x in cfgFiles[key] if x not in inter ]
        print "\nExtra files on ", key
        for extraFile in noMatch[key] :
            print extraFile


    compareAll(inter ,ignoreFile, boxPath)

#    noMatch[cfgFiles.keys()[0]] = [x for x in cfgFiles[cfgFiles.keys()[0]] if x not in inter ]
#    print "No Match = ",noMatch

def compareAll(inter ,ignoreFile, boxPath):
    with open(ignoreFile) as inFile:
        ignoreList = inFile.readlines()
    ignoreList = [x.rstrip() for x in ignoreList ]
    print "Following words will be ignored",ignoreList
    print inter  # intersection. matched files
    print "-"*20
#    for boxName in boxPath:
#        print "Box path = ", boxPath[boxName]
    for config in inter:
        a = 'cmp/%s/%s/%s' % (boxPath.keys()[0], boxPath[boxPath.keys()[0]].split('/')[-1], config,)
        b = 'cmp/%s/%s/%s' % (boxPath.keys()[-1], boxPath[boxPath.keys()[-1]].split('/')[-1], config)
        compareFile(a, b, ignoreList)

def compareFile(a, b, ignoreList):
    print "\n",
    print bcolors.FAIL +  a + bcolors.ENDC, 
    print "  VS  ", b
    print '_'*20
    cmpFile = {}
    for files in (a, b ):  
        if os.path.isfile(files):
            with open(files) as inFile:
                cmpFile[files] =  [ lines.strip() for lines in inFile if not re.match("^\s*\#+.*",lines) ]
#                print cmpFile[files]
#    print "\n\nintersection = ",set(cmpFile[a]).intersection(cmpFile[b])
#    print "\n ", a, " have extra lines :\n " #,list(set(cmpFile[a]).difference(cmpFile[b]))
    diffA = list(set(cmpFile[a]).difference(cmpFile[b]))
    diffB = list(set(cmpFile[b]).difference(cmpFile[a]))
    for x in list(set(cmpFile[a]).difference(cmpFile[b])):
#        for ignore in ignoreList:
#        if  len(x) > 0 and [p for p in ignoreList if re.match(p, x)] :
#            pass
        if len(x) > 0 : #and [p for p in ignoreList if re.match(p, x)] :
#            print "p = ", p
            flag = 0
            for p in ignoreList:
                match = re.match('.*'+p+'.*', x) 
                if match:
                    flag = 1
                    break
                else:
                    flag = 0
            if flag == 0 :
                print bcolors.FAIL + x + bcolors.ENDC

#    print "\n ", b, " have extra lines :\n " #,list(set(cmpFile[a]).difference(cmpFile[b]))
    for x in list(set(cmpFile[b]).difference(cmpFile[a])):
#        print x
        if len(x) > 0 :
#            print bcolors.OKBLUE + x + bcolors.ENDC
            flag = 0
            for p in ignoreList:
                match = re.match('.*'+p+'.*', x)
                if match:
                    flag = 1
                    break
                else:
                    flag = 0
            if flag == 0 :
                print x


#    print '/'*35
#    diffLines(cmpFile[a],cmpFile[b])

#    print "\n\ndifference list(a,b)= ",list(set(cmpFile[a]) & set(cmpFile[b]))
#    print "\n\ndifference b,a = ", diff(cmpFile[b],cmpFile[a])
#    sys.exit()


def diff(list1, list2):
    c = set(list1).union(set(list2))
    d = set(list1).intersection(set(list2))
    return list(c - d)

def diffLines(list1,list2):  #ignoreList):
    maxLen = max(len(list1),len(list2))
#    for num in range(maxLen):
    Found = 0
    for i in range(len(list1)):
        for j in range(len(list2)): 
            if list1[i] != list2[j]:
#                print list1[i]
                #print bcolors.FAIL + list1[i] + bcolors.ENDC
                Found = 0
            else:
                Found = 1
                break
        if Found == 0 :
            print bcolors.FAIL + list1[i] + bcolors.ENDC
            

#    for i in range(len(list2)):
#        for j in range(len(list1)): 
#            if list1[i] != list2[j]:
#                print list2[i]
#            else:
#                break
    

#        i = num
#        j = num
#        if list1[i] != list2[j]:
#            for ig in ignoreList:
#                if not re.match(ig,list1[i]) and not re.match(ig,list1[j]):
#                    pass
#                    print 

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

            path = "%s/cmp/%s" % (str(os.getcwd()),str(i))
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
    ''' Reading file to list
    '''
 
    with open(filename) as in_file:
        txt_file = in_file.readlines()
    return txt_file


def parse_args(argv):
    """ Parse the arguments.
    Parameters:
        argv - the list of arguments
    """
    parser = optparse.OptionParser(description='This script is for compare config files between different remote boxes')
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
