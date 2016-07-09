#!/usr/bin/python

import sys, time, re, socket, smtplib
from multiprocessing import Pool
from email.mime.text import MIMEText

def main():

  if len(sys.argv) != 2:
    print 'usage: ' + sys.argv[0] + ' file'
    sys.exit(1)
  # gets file from arg
  filename = sys.argv[1]
  # load today's IPs into list
  ips = ipFinder(filename)
  #Count IPs
  count = ipCounter(ips)
  p = Pool(11)
  hostname = p.map(ipLookupMulti, count.keys())
  # mails results as email body
  mailer(hostname)

def ipCounter(ips):
  #takes a list of IPs and counts them
  count = {}
  for ip in ips:
    count[ip] = count.get(ip,0) + 1
  return count

def ipFinder(filename):
  # Find today's IP Addresses in DNS logs and returns the first one
  # it is assumed that the 2nd ip in the line is the DNS servers' IP
  # time formate of the logs = time.strftime("%d-%b-%Y")
  # import time, re
  ips = []
  date =  time.strftime("%d-%b-%Y") # 21-Jun-2016
  with open(filename,buffering=200000000) as doc:
    for line in doc:
      if date in line and "PTR" not in line:
        ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line ) # matches all IPs
        #ip = re.findall( r'[129,160,10,192,172]+(?:\.[0-9]+){3}', line ) # maches internal IPs
        ips.append(ip[0])
  return ips

def ipLookupMulti(host):
  #import socket
  try:
    hostlist = socket.gethostbyaddr(host)
    host = hostlist[0]
  except socket.herror as err:
    host = host
  return host

def mailer(body):
  #mails info to group
  # Import smtplib for the actual sending function
  #import smtplib
  # Import the email modules we'll need
  #from email.mime.text import MIMEText
  if not body:
    print "No Results: No email will be sent"
    sys.exit(1)
  sender = "no-reply@localhost"
  to = ['email1@foo.bar','email2@foo.bar']
  # convert list to string with carriage returns
  msg = MIMEText("\n".join(body))
  msg['Subject'] = "Systems still using old BIND server today" 
  msg['From'] = sender
  msg['To'] = ', '.join(to)

  s = smtplib.SMTP('localhost')
  s.sendmail(sender, to, msg.as_string())
  s.quit()

if __name__ == '__main__':
  main()
wturnage@wor
