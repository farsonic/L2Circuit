#!/usr/bin/python
import sys, getopt
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

def main(argv):
   endpointA = ''
   endpointAInterface = ''
   endpointB = ''
   endpointBInterface = ''
   vlan = ''
   
   try:
      opts, args = getopt.getopt(argv, 'a:b:c:d:v:')
   except getopt.GetoptError:
      print 'l2circuit.py -a <endpointA> -b <endpointB> -c <endpointA interface> -d <endpointB interface> -v <vlan>'
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print 'l2circuit.py -a <endpointA> -b <endpointB> -c <endpointA interface> -d <endpointB interface> -v <vlan>'
         sys.exit()

      elif opt in ("-a"):
         endpointA = arg
      elif opt in ("-v"):
         vlan = arg
      elif opt in ("-b"):
         endpointB = arg
      elif opt in ("-c"):
         endpointAInterface = arg
      elif opt in ("-d"):
         endpointBInterface = arg


   dev1 = Device(host=endpointA,user='admin',password='jun1per')
   dev2 = Device(host=endpointB,user='admin',password='jun1per')
   
   dev1.open()
   dev2.open()

   cu1 = Config(dev1)
   cu2 = Config(dev2)

   set_cmd1a = 'set interfaces ' + endpointAInterface + ' vlan-tagging'
   set_cmd1b = 'set interfaces ' + endpointAInterface + ' encapsulation flexible-ethernet-services'
   set_cmd1c = 'set interfaces ' + endpointAInterface + ' unit ' + vlan + ' encapsulation vlan-ccc'
   set_cmd1d = 'set interfaces ' + endpointAInterface + ' unit ' + vlan + ' vlan-id ' + vlan 
   set_cmd1e = 'set protocols l2circuit neighbor ' + endpointB + ' interface ' + endpointAInterface + '.' + vlan + ' virtual-circuit-id ' + vlan

   set_cmd2a = 'set interfaces ' + endpointBInterface + ' vlan-tagging'
   set_cmd2b = 'set interfaces ' + endpointBInterface + ' encapsulation flexible-ethernet-services'
   set_cmd2c = 'set interfaces ' + endpointBInterface + ' unit ' + vlan + ' encapsulation vlan-ccc'
   set_cmd2d = 'set interfaces ' + endpointAInterface + ' unit ' + vlan + ' vlan-id ' + vlan 
   set_cmd2e = 'set protocols l2circuit neighbor ' + endpointA + ' interface ' + endpointBInterface + '.' + vlan + ' virtual-circuit-id ' + vlan

   print 'applying configuration changes to '  + endpointA
   cu1.load(set_cmd1a, format='set')
   cu1.load(set_cmd1b, format='set')
   cu1.load(set_cmd1c, format='set')
   cu1.load(set_cmd1d, format='set')
   cu1.load(set_cmd1e, format='set')

   print 'applying configuration changes to '  + endpointB
   cu2.load(set_cmd2a, format='set')
   cu2.load(set_cmd2b, format='set')
   cu2.load(set_cmd2c, format='set')
   cu2.load(set_cmd2d, format='set')
   cu2.load(set_cmd2e, format='set')




   #cu1.pdiff()
   #cu2.pdiff()
   print 'Committing changes to ' + endpointA
   cu1.commit()
   print 'Committing changes to ' + endpointB
   cu2.commit()
   dev1.close()
   dev2.close()
   print 'Done....'

if __name__ == "__main__":
   main(sys.argv[1:])

