# Property-based TDD (As If You Meant It) #

This repository contains the exercises from [Nat Pryce](https://twitter.com/natpryce) and [Keith Braithwaite](https://twitter.com/keithb_b)'s session at [SPA 2013](http://www.spaconference.org).

I worked with [https://twitter.com/MrAndrew](https://twitter.com/MrAndrew "Andrew Seward") during this session.  This repo is forked from the code we had at the end of the session - further commits are experimentation I did later.

Below are the notes that I took during the session.  You can see Nat's writeup [here](http://natpryce.com/articles/000802.html).

## Example based TDD ##

* Triangulates behaviour using examples
* Often not obvious which cases are special, or why examples are significant
* Easy to miss negative cases

## Property based testing ##

* Invented around 2000 - comes from Haskell community
* Don't define examples, define properties of the system
* Tests generate inputs (often random) to verify those properties
* Leads to as good (or better) coverage as selecting examples
* Need to be careful not just to write same code twice
* Has been treated as an "after the fact" testing tool, rather than a true red-green-refactor TDD tool

## Exercise ##

We tried the units of measure exercise, described [here](http://natpryce.com/presentations/spa2013-b.pdf).

## Learnings ##

* One test drives out much more behaviour than an example test
* As code becomes more specific, properties become more complicated
* Harder to tell whether you've got the test right or not
* Opaque - not much output about what's happened
* Units of measure exercise much easier than [Tic Tac Toe](http://natpryce.com/presentations/spa2013-a.pdf) - fits better into the framework
* Need to get right representation of data in order to get started with tests - but could start with an empty type and TDD its implementation with properties
* We're unfamiliar with the "baby steps" to take with property testing, but very familiar when example testing
* Need to be aware of what generators are creating, not just using one that's a bit similar.  
	* Might need to test generators!
* When would it be useful?
	* Parsers
	* Working with legacy code
	* Porting to a new language
* Found some errors we hadn't expected (e.g. divide by zero error)
* Need to be careful not to reimplement code logic in tests - instead:
    * have more tests
    * have simpler tests
    * filter out special cases from general tests 