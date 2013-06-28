from factcheck import *
from hamcrest import *
from quantity import *

def values():
	return floats(lower = 0)

def units():
	return choices(['m', 's', 'w', 'h'])
	
def powers():
	return ints()

@forall(firstValue = values(), secondValue = values(), unit = units())
def test_adding_same_unit(firstValue, secondValue, unit):
	quantity_a = Quantity(firstValue, unit)
	quantity_b = Quantity(secondValue, unit)

	result = quantity_a.add(quantity_b)
	assert_that(result.unit, equal_to(unit))
	assert_that(result.value, equal_to(firstValue + secondValue))

@forall(firstValue = values(), secondValue = values(), firstUnit = units(), secondUnit = units(), 
	where = lambda firstUnit, secondUnit : firstUnit != secondUnit)
def test_adding_different_units(firstValue, secondValue, firstUnit, secondUnit):
	quantity_a = Quantity(firstValue, firstUnit)
	quantity_b = Quantity(secondValue, secondUnit)

	try:
		quantity_a.add(quantity_b)
	except ValueError:
		pass
	else:
		self.fail("expected a ValueError")

@forall(firstValue = values(), secondValue = values(), firstUnit = units(), secondUnit = units(), 
	where = lambda firstUnit, secondUnit : firstUnit!=secondUnit)
def test_multiplying_different_units(firstValue, secondValue, firstUnit, secondUnit):
	quantity_a = Quantity(firstValue, firstUnit)
	quantity_b = Quantity(secondValue, secondUnit)

	result = quantity_a.multiply(quantity_b)
	assert_that(result.unit, equal_to(firstUnit + secondUnit))
	assert_that(result.value, equal_to(firstValue*secondValue))

@forall(firstValue = values(), secondValue = values(), unit = units())
def test_multiplying_same_unit(firstValue, secondValue, unit):
	quantity_a = Quantity(firstValue, unit)
	quantity_b = Quantity(secondValue, unit)

	result = quantity_a.multiply(quantity_b)
	assert_that(result.unit, equal_to(unit + "^2"))
	assert_that(result.value, equal_to(firstValue * secondValue))

@forall(firstValue = values(), secondValue = values(), firstUnit = units(), secondUnit = units(), 
	where = lambda firstUnit, secondUnit, secondValue : firstUnit!=secondUnit and secondValue > 0)
def test_dividing_different_units(firstValue, secondValue, firstUnit, secondUnit):
	quantity_a = Quantity(firstValue, firstUnit)
	quantity_b = Quantity(secondValue, secondUnit)

	result = quantity_a.divide(quantity_b)
	assert_that(result.unit, equal_to(firstUnit + "/" + secondUnit))
	assert_that(result.value, equal_to(firstValue / secondValue))

@forall(firstValue = values(), secondValue = always(0), firstUnit = units(), secondUnit = units())
def test_dividing_by_zero(firstValue, secondValue, firstUnit, secondUnit):
	quantity_a = Quantity(firstValue, firstUnit)
	quantity_b = Quantity(secondValue, secondUnit)

	try:
		quantity_a.divide(quantity_b)
	except ZeroDivisionError:
		pass
	else:
		self.fail("expected a ZeroDivisionError")		

@forall(firstValue = values(), secondValue = values(), unit = units(), firstPower = powers(), secondPower = powers(),
	where = lambda firstPower, secondPower : firstPower + secondPower > 1)
def test_multiplying_same_unit_different_powers(firstValue, secondValue, unit, firstPower, secondPower):
	quantity_a = Quantity(firstValue, "%s^%s" % (unit, firstPower))
	quantity_b = Quantity(secondValue, "%s^%s" % (unit, secondPower))

	result = quantity_a.multiply(quantity_b)
	assert_that(result.unit, equal_to("%s^%s" % (unit, firstPower+secondPower)))
	assert_that(result.value, equal_to(firstValue * secondValue))

@forall(firstValue = values(), secondValue = values(), unit = units(), firstPower = powers())
def test_multiplying_same_unit_different_powers_totalling_1(firstValue, secondValue, unit, firstPower):
	secondPower = 1 - firstPower

	quantity_a = Quantity(firstValue, "%s^%s" % (unit, firstPower))
	quantity_b = Quantity(secondValue, "%s^%s" % (unit, secondPower))

	result = quantity_a.multiply(quantity_b)
	assert_that(result.unit, equal_to(unit))
	assert_that(result.value, equal_to(firstValue * secondValue))

@forall(firstValue = values(), secondValue = values(), unit = units(), firstPower = powers())
def test_multiplying_same_unit_different_powers_totalling_0(firstValue, secondValue, unit, firstPower):
	secondPower = - firstPower

	quantity_a = Quantity(firstValue, "%s^%s" % (unit, firstPower))
	quantity_b = Quantity(secondValue, "%s^%s" % (unit, secondPower))

	result = quantity_a.multiply(quantity_b)
	assert_that(result.unit, equal_to(""))
	assert_that(result.value, equal_to(firstValue * secondValue))