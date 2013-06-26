from factcheck import *
from hamcrest import *
import unittest
from TypedValue import *

class TypedValueTests(unittest.TestCase):
	def values():
		return floats(lower = 0)

	def units():
		return choices(['m', 's', 'w', 'h'])
		
	def powers():
		return ints()

	@forall(firstValue = values(), secondValue = values(), unit = units())
	def test_adding_same_unit(self, firstValue, secondValue, unit):
		value_a = TypedValue(firstValue, unit)
		value_b = TypedValue(secondValue, unit)

		result = value_a.add(value_b)
		assert_that(result.unit, equal_to(unit))
		assert_that(result.value, equal_to(firstValue+secondValue))

	@forall(firstValue = values(), secondValue = values(), firstUnit = units(), secondUnit = units(), 
		where = lambda firstUnit, secondUnit : firstUnit!=secondUnit)
	def test_adding_different_units(self, firstValue, secondValue, firstUnit, secondUnit):
		value_a = TypedValue(firstValue, firstUnit)
		value_b = TypedValue(secondValue, secondUnit)

		try:
			value_a.add(value_b)
		except ValueError:
			pass
		else:
			self.fail("expected a ValueError")

	@forall(firstValue = values(), secondValue = values(), firstUnit = units(), secondUnit = units(), 
		where = lambda firstUnit, secondUnit : firstUnit!=secondUnit)
	def test_multiplying_different_units(self, firstValue, secondValue, firstUnit, secondUnit):
		value_a = TypedValue(firstValue, firstUnit)
		value_b = TypedValue(secondValue, secondUnit)

		result = value_a.multiply(value_b)
		assert_that(result.unit, equal_to(firstUnit + secondUnit))
		assert_that(result.value, equal_to(firstValue*secondValue))

	@forall(firstValue = values(), secondValue = values(), unit = units())
	def test_multiplying_same_unit(self, firstValue, secondValue, unit):
		value_a = TypedValue(firstValue, unit)
		value_b = TypedValue(secondValue, unit)

		result = value_a.multiply(value_b)
		assert_that(result.unit, equal_to(unit + "^2"))
		assert_that(result.value, equal_to(firstValue * secondValue))

	@forall(firstValue = values(), secondValue = values(), firstUnit = units(), secondUnit = units(), 
		where = lambda firstUnit, secondUnit, secondValue : firstUnit!=secondUnit and secondValue > 0)
	def test_dividing_different_units(self, firstValue, secondValue, firstUnit, secondUnit):
		value_a = TypedValue(firstValue, firstUnit)
		value_b = TypedValue(secondValue, secondUnit)

		result = value_a.divide(value_b)
		assert_that(result.unit, equal_to(firstUnit + "/" + secondUnit))
		assert_that(result.value, equal_to(firstValue / secondValue))

	@forall(firstValue = values(), secondValue = always(0), firstUnit = units(), secondUnit = units())
	def test_dividing_by_zero(self, firstValue, secondValue, firstUnit, secondUnit):
		value_a = TypedValue(firstValue, firstUnit)
		value_b = TypedValue(secondValue, secondUnit)

		try:
			value_a.divide(value_b)
		except ZeroDivisionError:
			pass
		else:
			self.fail("expected a ZeroDivisionError")		

	@forall(firstValue = values(), secondValue = values(), unit = units(), firstPower = powers(), secondPower = powers(),
		where = lambda firstPower, secondPower : firstPower + secondPower > 1)
	def test_multiplying_same_unit_different_powers(self, firstValue, secondValue, unit, firstPower, secondPower):
		value_a = TypedValue(firstValue, "%s^%s" % (unit, firstPower))
		value_b = TypedValue(secondValue, "%s^%s" % (unit, secondPower))

		result = value_a.multiply(value_b)
		assert_that(result.unit, equal_to("%s^%s" % (unit, firstPower+secondPower)))
		assert_that(result.value, equal_to(firstValue * secondValue))

	@forall(firstValue = values(), secondValue = values(), unit = units(), firstPower = powers(), secondPower = powers(),
		where = lambda firstPower, secondPower : firstPower + secondPower == 1)
	def test_multiplying_same_unit_different_powers_totalling_1(self, firstValue, secondValue, unit, firstPower, secondPower):
		value_a = TypedValue(firstValue, "%s^%s" % (unit, firstPower))
		value_b = TypedValue(secondValue, "%s^%s" % (unit, secondPower))

		result = value_a.multiply(value_b)
		assert_that(result.unit, equal_to(unit))
		assert_that(result.value, equal_to(firstValue * secondValue))

if __name__ == "__main__":
	unittest.main()