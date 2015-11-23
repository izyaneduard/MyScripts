#!/usr/bin/python

'''
Usage ./config_compare.py -l list of boxes -c 
'''

import sys
import os


sys.path.append('/home/eduardi/python/bin')

import paramiko
 
########################################################################
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
 
#if __name__ == "__main__":
#    host = "alx64dev6.he.cqg"
#    username = "eduardi"
#    pw = "eduardi"
# 
#    origin = '/home/eduardi/OUT/hoplya.txt'
#    dst = '/home/eduardi/scripts/python/config_compare/cp/hoplya.txt'
# 
#    ssh = SSHConnection(host, username, pw)
#    ssh.get(origin, dst)
#    ssh.put(dst,origin)
#    ssh.close()


 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('tlghe.he.cqg', username='bvt', password='baseline')
except paramiko.SSHException:
    print "Connection Error"
sftp = ssh.open_sftp()
sftp.chdir("/usr/he/config/")
#print sftp.listdir()

ssh2 = SSHConnection('tlghe.he.cqg', username='bvt', password='baseline')

for i in sftp.listdir() :
    print "i = ",i
    origin = '/usr/he/config/%s' % (str(i))
    dst = '/home/eduardi/scripts/python/config_compare/cp/%s' % (str(i))

    sftp.get(origin, dst)        
 
#    ssh2.get(origin, dst) 
ssh.close()
