#!/usr/bin/python

"""
Simple script to compair DNS records 
requires dnspython which is provided by the python-dns package in RHEL
or if you're on a mac like me "pip install dnspython"
"""

import dns.resolver, getopt, sys

def main():
  """
  Main fuction
  """
  #check to make sure arguments are passed
  if len(sys.argv) < 2:
    usage()
    sys.exit(2)
  #loads arguments and errors out if passed an unknown arg
  try:
    opts, args = getopt.getopt(sys.argv[1:], "f:ht:", [ 'server1=' ,'server2=', 'file=', 'type=', 'help'])
  except getopt.GetoptError as err:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit()
  r_type = ""
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit()
    elif o == "--server1":
      server1 = a
    elif o == "--server2":
      server2 = a
    elif o in ( "-f", "--file"):
      infile = a
    elif o in ("-t", "--type"):
      r_type = a.upper()
      if r_type not in ("A","CNAME", "TXT", "PTR", "MX"):
        print "Invalide Record Type"
        usage()
        sys.exit()

  records = open(infile)

  if r_type == "":
    get_all(server1, server2, records)
  else:
    rlist = get_records(records, r_type)
    print "starting query, please wait"
    try:
      for i in range(len(rlist)):
        response1 = resolve(server1, rlist[i], r_type)
        response2 = resolve(server2, rlist[i], r_type)
        if response1 != response2:
          print "server 1: ", rlist[i], "=", response1, " - ", "server 2: ", rlist[i], "=",  response2
    except KeyboardInterrupt:
      print 'OK! OK! I\'ll stop.'
      sys.exit()

# - End Main - #

def resolve(server, record, r_type):
  dns_serv = dns.resolver.Resolver()
  dns_serv.nameservers = [server]
  try:
    answer = str(dns_serv.query(record, r_type)[0])
    return answer
  except:
    return "NXDOMAIN"
# https://answers.splunk.com/answers/110437/editing-dnslookup-for-specific-dns-server.html


def ptr2ip(records):
  c = []
  for line in records:
    if "PTR" in line:
      a = line.split()
      b = a[0].split('.')
      c.append(b[3] + '.' + b[2] + '.' + b[1] + '.' + b[0]) # this probably can be done cleaner with str.join()
  return c

def get_records(datafile, record):
  b = []
  if record == "ALL":
    record = " IN "
  else:
    record = " IN " + record
  for line in datafile:
    if record in line:
      a = line.split()
      if record == "IN CNAME":
        b.append(a[0].lower())
      else:
        b.append(a[0])
  return b

def get_all(server1, server2, datafile):
  types = ["A","CNAME", "TXT", "PTR", "MX"]
  print "starting query of all records, please wait"
  for t in types:
    print "Starting ", t, " query"
    rlist = get_records(datafile, t)
    try:
      for i in range(len(rlist)):
        response1 = resolve(server1, rlist[i], t)
        response2 = resolve(server2, rlist[i], t)
        if response1 != response2:
          print "server 1: ", rlist[i], "=", response1, " - ", "server 2: ", rlist[i], "=",  response2

    except KeyboardInterrupt:
      print 'OK! OK! I\'ll stop.'



def usage():
  """prints usage for user """
  print "Usage: ", sys.argv[0], "--server1 <ip address> --server2 <ip address> --file <DNS input file> [--type <record type>] " 

  print '\nThe DNS record file should be generaged using "rndc dumpdb -zones" command on your DNS server.'


#calls main if the file was run directly 
if __name__ == '__main__':
  main()
