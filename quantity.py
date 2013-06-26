import re

UNIT_WITH_POWER = re.compile("(.+)\^(-?\d+)")

class Quantity:
	def __init__(self,value,unit):
		self.value = value
		self.unit = unit

	def add(self, otherQuantity):
		if (self.unit != otherQuantity.unit):
			raise ValueError("Can't add typed values with mismatching units")

		return Quantity(self.value + otherQuantity.value, self.unit)

	def multiply(self, otherQuantity):
		parsedUnit = self.getParsedUnit()
		otherParsedUnit = otherQuantity.getParsedUnit()

		if (parsedUnit[0] == otherParsedUnit[0]):
			if (parsedUnit[1] + otherParsedUnit[1] == 1):
				newUnit = parsedUnit[0]
			else:
				newUnit = "%s^%s" % (parsedUnit[0], parsedUnit[1] + otherParsedUnit[1])
		else:	
			newUnit = self.unit + otherQuantity.unit

		return Quantity(self.value * otherQuantity.value, newUnit)

	def divide(self, otherQuantity):
		newUnit = self.unit + "/" + otherQuantity.unit

		return Quantity(self.value / otherQuantity.value, newUnit)

	def getParsedUnit(self):
		unitWithPowerMatch = UNIT_WITH_POWER.match(self.unit)

		if unitWithPowerMatch:
			baseUnit = unitWithPowerMatch.group(1)
			power = int(unitWithPowerMatch.group(2))
			return (baseUnit, power)
		else:
			return (self.unit, 1)