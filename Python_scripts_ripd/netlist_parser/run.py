#!/usr/bin/python
"""Comments"""


import netlist


NETLIST_NAME = netlist.Netlist()   # N1 # netlist object 

NETLIST_NAME.read("./netlist.lvs")           # N2 # read spice netlist 


print "get_all_cells"
print NETLIST_NAME.get_all_cells()  #N3 # print all cells

CELL_NAME = NETLIST_NAME.get_cell("NAND")

print "PINS NAND"
print CELL_NAME.get_pin_order()

CELL_NAME.set_pin_order("PIN1 PIN2 PIN3 PIN4")

print "NEW PINS"
print CELL_NAME.get_pin_order()

print "get_all_instances"
print CELL_NAME.get_all_instances()

TRANSISTOR_NAME = CELL_NAME.get_instance('MP2A')
TRANSISTOR_NAME.set_attribute("Name","M_NEW_NAME")
TRANSISTOR_NAME.set_attribute("S","SOURCE")
TRANSISTOR_NAME.set_attribute("D","DRAIN")
TRANSISTOR_NAME.set_attribute("Model","PCHAN")


DIODE_NAME = CELL_NAME.get_instance('DN21')
DIODE_NAME.set_attribute("Name","DIODE_NAME")
DIODE_NAME.set_attribute("MINUS","VSS")


NETLIST_NAME.write('netlist.lvs_out')

print '_____________'


CH_NETLIST_NAME = netlist.Netlist()   # N1 # netlist object 

CH_NETLIST_NAME.read("./netlist.lvs_out")           # N2 # read  changed spice netlist 


print "get_all_cells"
print CH_NETLIST_NAME.get_all_cells()  #N3 # print all cells

CH_CELL_NAME = CH_NETLIST_NAME.get_cell("NAND")

print "PINS"
print CH_CELL_NAME.get_pin_order()

print "get_all_instances"
print CH_CELL_NAME.get_all_instances()


"""
NETLIST_NAME.read1("./netlist.lvs")   
CELL_NAME = NETLIST_NAME.get_cell1("NAND")

print CELL_NAME.get_pin_order()

CELL_NAME.set_pin_order("PIN1 PIN2 PIN3 PIN4")

print CELL_NAME.get_all_instances()

TRANSISTOR_NAME = CELL_NAME.get_instance('MP2A')
TRANSISTOR_NAME.set_attribute("Name","M_NEW_NAME")

NETLIST_NAME.write1('netlist.lvs_out')

"""
