from gdb.printing import PrettyPrinter, register_pretty_printer
import gdb

class VectorPrettyPrinter(object):
	"""Print vector in heap"""
	def __init__(self, val):
		self.val = val

	def to_string(self):
		return "TODO: implement"

class CustomPrettyPrinterLocator(PrettyPrinter):
	"""Search for custom pretty printer, given a gdb.Value"""
	def __init__(self):
		super(CustomPrettyPrinterLocator, self).__init__("incc_pretty_printers", [])

	def __call__(self, val):
		# return custom formatter if type can be handled
		inf = gdb.inferiors()[0] # gdb inferior to access raw memory

		addr = val.address # address of value
		# read 2 Byte [tag, ptr] of object
		obj_tag = inf.read_memory(addr, 1)
		obj_value_ptr = inf.read_memory(addr+1, 1)
		if obj_tag == 'V':
			return VectorPrettyPrinter(val)
		else:
			typename = val.type.name

register_pretty_printer(None, CustomPrettyPrinterLocator(), replace=True)
