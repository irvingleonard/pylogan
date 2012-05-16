
def readeable_size(size):
	"""Function to convert number of bytes to a 1:1024 range with unit

	It uses the 1024 powers, it could be implemented for others scales (like 1000 or metric)
	"""
	multiplier = 0
	while size >= 1024:
		size = size / 1024
		multiplier += 1
	
	size = str(round(size, 2))
	if multiplier == 0:
		size += ""
	elif multiplier == 1:
		size += "K"
	elif multiplier == 2:
		size += "M"
	elif multiplier == 3:
		size += "G"
	elif multiplier == 4:
		size += "T"
	elif multiplier == 5:
		size += "E"
	elif multiplier == 6:
		size += "P"
	else:
		size += "TooMuch!"
	
	size += "B"
	
	return size