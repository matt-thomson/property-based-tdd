import re

UNIT_WITH_POWER = re.compile("(.+)\^(-?\d+)")

class TypedValue:
	def __init__(self,value,unit):
		self.value = value
		self.unit = unit

	def add(self, otherTypedValue):
		if (self.unit != otherTypedValue.unit):
			raise ValueError("Can't add typed values with mismatching units")

		return TypedValue(self.value + otherTypedValue.value, self.unit)

	def multiply(self, otherTypedValue):
		parsedUnit = self.getParsedUnit()
		otherParsedUnit = otherTypedValue.getParsedUnit()

		if (parsedUnit[0] == otherParsedUnit[0]):
			if (parsedUnit[1] + otherParsedUnit[1] == 1):
				newUnit = parsedUnit[0]
			else:
				newUnit = "%s^%s" % (parsedUnit[0], parsedUnit[1] + otherParsedUnit[1])
		else:	
			newUnit = self.unit + otherTypedValue.unit

		return TypedValue(self.value * otherTypedValue.value, newUnit)

	def divide(self, otherTypedValue):
		newUnit = self.unit + "/" + otherTypedValue.unit

		return TypedValue(self.value / otherTypedValue.value, newUnit)

	def getParsedUnit(self):
		unitWithPowerMatch = UNIT_WITH_POWER.match(self.unit)

		if unitWithPowerMatch:
			baseUnit = unitWithPowerMatch.group(1)
			power = int(unitWithPowerMatch.group(2))
			return (baseUnit, power)
		else:
			return (self.unit, 1)