#!/usr/bin/python
import re


print  '__________Start__________\n'




class Netlist :
	cell_pins = {}
	cellss = {}
	inst_w = {}
	all_cells = {}
	cell_name_list = []
	def __init__ (self) :
		self.all_cells	= {}
		self.lists = 0
		self.pin_hash = {}

	def read (self, file) :
		try :
			f = open(file,'r')
		except :
			print "Error: can\'t find file"
		else :
			lists = []
			for i in f:
				lists.append(i)
	
			f.close()
			self.lists = lists
			self.get_all_cells1(self.lists)
			return lists

			
	
	def get_all_cells1(self, ll) :
		cell_name = []
		cell_subckt = {}
		pin_hash = {}
		flag = 0
		ll_subckt = []
		for i in ll :
			cell = re.match( '^\s*\.subckt\s+(\w+)(.*)', i)
			end_find = re.match( '^\.ends', i)
			if (cell) :
				cell_name.append(cell.group(1))
				name = cell.group(1)
				self.pin_hash[name] = cell.group(2)  #only pins
				flag = 1
			
			elif (end_find) :
				flag = 0
				ll_subckt = []
			elif (flag) :
				ll_subckt.append(i)
				self.all_cells[name] = ll_subckt
		return pin_hash

	def get_all_cells (self) :
		return self.all_cells.keys()
		
	def get_cell (self,cell_name) :
		self.cell_name = cell_name
		return Cell(self.pin_hash[cell_name], self.all_cells[cell_name],cell_name)
		#return all_cells[self.cell_name]

			
	def write (self, file_name) :
		f = open(file_name,"w")
		flag = 0
		for a in self.lists :
			x = re.match( '^\s*\.subckt\s+(\w+)\s*(.*)', a)
			
			if x :
				if x.group(1) in Netlist.cell_pins :
					flag2 = 0
					name_cell = x.group(1)
					f.write('.subckt '+x.group(1) +" "+Netlist.cell_pins[x.group(1)]+'\n')
					if name_cell in Netlist.cellss :
						for g in Netlist.cellss[name_cell] :
							inst = g.split(' ')
							if inst[0] in Netlist.inst_w :
								f.write(Netlist.inst_w[inst[0]])
							else:
								f.write(g)
					else :
						flag2 = 1
					flag = 1
				else :
					f.write('.subckt '+x.group(1) + " "+x.group(2)+'\n')
			elif (flag) :
				if (re.match( '^\.ends\s*', a)):
					#f.write('.ends\n')
					f.write(a)
					flag = 0
				elif(flag2) :
					f.write(a)
			else :
				f.write(a)
		f.close()
	

		

						
class Cell :
	def __init__ (self,pins,instances,cell_name) :
		self.pins = pins
		self.inst = instances
		self.cell_name = cell_name
				
	def get_pin_order(self) :
		return self.pins
	def set_pin_order(self,pin_order) :
		self.pins = pin_order
		Netlist.cell_pins[self.cell_name] = pin_order
	def get_all_instances(self) :
		Netlist.cellss[self.cell_name] = self.inst
		return self.inst
		
	def get_instance(self,inst_name) :
		for i in self.inst :
			inst_search = re.search( "^\s*" + inst_name + "\s+(.*)", i)
			if(inst_search and inst_name[0] == 'M' ) :
				return Transistor(i,inst_name,self.cell_name)
			elif (inst_search and inst_name[0] == 'D') :
				return Diode(i,inst_name,self.cell_name)
	

	
class Transistor :

	def __init__ (self,transistor_line,inst_name,cell_name) :
		self.inst_name = inst_name
		self.transistor_line = transistor_line
		self.cell_name = cell_name
		array = self.transistor_line.split(' ')
		p = 0
		for j in ['Name','S','D','G','B','Model','L','W'] :
			setattr(self,j,array[p])
			p += 1
	def set_attribute (self,key,value) :
		setattr(self,key,value)
		self.run()
	def run (self) :
		Netlist.inst_w[self.inst_name] = (self.Name + ' '+ self.S +' ' + self.D +' ' 
		 + self.G +' ' + self.B +' ' + self.Model 
		 + ' ' + self.L  +' ' + self.W + '\n')
	
	
class Diode :
		
	def __init__ (self,diode_line,inst_name,cell_name) :
		self.inst_name = inst_name
		self.diode_line = diode_line
		self.cell_name = cell_name
		array = self.diode_line.split(' ')
		p = 0
		for j in ['Name','PLUS','MINUS','AREA','PJ'] :
			setattr(self,j,array[p])
			p += 1
	def set_attribute (self,key,value) :
		setattr(self,key,value)
		self.run()
	def run (self) :
		Netlist.inst_w[self.inst_name] = self.Name + ' '+ self.PLUS +' ' + self.MINUS +' ' + self.AREA +' ' + self.PJ + '\n'
	
