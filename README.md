# Basic Contact Book in Python

With smart querying functionality and database compatability checking
Based in sqlite3 and vanilla Python
Accepted fields: 'name', 'firstname', 'lastname', 'address', 'phonenum', 'worknum', 'e mail', 'added'

## Resources

### Modules used

(all built-ins)

- sqlite3
- time
- re
- os
- sys

## About

This is the second "big" project by a beginner.  I built this mostly from scratch, with references to the Python manual and some StackExchange searches for some specific issues I came upon, like checking if all items of a list are members of a predefined set in order to validate user selections.
There's plenty of updating that can be done with this, perhaps beginning with modifying the user interaction with argparse and making a wrapper program to create attractive output for results, or a realtime ASCII graphic CLI user interface.  Great fun!

## Usage
1.  Create a class object, passing in the name of the db you want to load/create, or optionally passing in "mode='m'" to create in memory if testing is desired.  The arg 'dbg' can also be set to True to provide debug messages.  
The __init__ function has a built-in db checker for existing db's to ensure compatability and give the user flexibility to change their mind and create a fresh db without having to exit the program.
2.  Call use the *Contact public methods to populate, modify or read from the db

## WHAT I LEARNED & REFINED:
- database manipulation and control through Python
- database compatability checking including use of sqlite SCHEMA and master table
- database use flexibility 
- sqlite3 regex functionality
- interactive and stable user choice prompting using vanilla methods
- exception catching with clear explanations for user
- list comprehensions
- creating flexible sql insertion methods
- creating robust sql search methods
<br>


## Methods

### \_\_init\_\_(db=None, mode=None, dbg=False)

**Takes:**
- db - name of database to load if desired, creates one of the name if the db doesn't exist, or asks user to give a path+name for a new one if none given.  If an existing one is given, it's checked for existing tables, existing 'contacts' table and whether the table has all of the valid columns.  Default is None and creates a new db.
- mode - use to choose whether to make the db in memory or not. Default creates/uses a file based database. Argument 'm' uses a memory based database, which is intended for testing.
- dbg - when True, enables extra informational messages throughout program. Intended for debugging.  Default is False.

This method loads & initializes a sqlite3 databse and ensures it has a table 'contacts' with the correct fields for use as a contact book.  A string representing the filepath of an existing, or desired new, database can be passed in as an argument during class object creation to load/create that database.  
Argument "mode='m'" can optionally be passed it to alternatively create the db in memory, but this is intended for testing & debugging.
Argument 'dbg' when set to True will enable extra informational messaging throughout the program, and is intended for debugging.
During instantiation with an existing database, it is checked automatically for the correct table and columns with options to abort the program or create a new database instead through an interactive prompt.  Several internal methods are used within __init__ for all of this processing (see code for details)
Finally, a regexp function for SQLite is declared, since there is no built-in regexp function in Sqlite3.
<br>
### \_\_str\_\_()

A method for "print(clsObj)" to return custom information.
Returns a few lines including an instruction for the 'm' mode, the list of valid columns so the user knows how to address insertions, and a list of the current entry names in the db.
<br>
### \_\_addContact\_\_(name\[, addr=None, phnum=None, wknum=None, email=None, added=time.ctime()\])

**Takes:**

- name - *required*, a string representing the full name of the entry, first and last name separated by spaces
- addr - *opt*, a string represeting the entry's address
- phnum - *opt*, a string representing the entry's personal/home phone number
- wknum - *opt*, a string representing the entry's work phone number
- email - *opt*, a string representing the entry's primary email address
- added - *apt*, the time the entry was created. It can be provided as a string, otherwise is generated automatically.

This is a very basic contact entry method. Strings are supplied for the entry name and any other desired optional field keyword. The provided name is also automatically split into first and last name, which are then added to the insertion automatically. Generally this was used for testing while building the program and is superceded by **insQ**
<br>
### \_\_insQ\_\_(\[dbg=False\], **kwargs)

Versatile insertion method.  Generates a valid insertion statement from input args and executes it.  Has built-in validation of kwargs to ensure the correct columns are given.

**Takes:**

- kwargs - any number of keyword=value pairs, where the keyword must be a valid column name given as a NON-string.

> ex. name='Roger Moore'

**Returns:** \- nothing, save for debugging prints if arg 'dbg=True' given

Kwargs are checked to ensure that valid column names were used. Then the function checks for 'name' in the given columns, and if given automatically adds first & last name entries to the insertion statement.
The optional argument 'dbg' when set to True enables a few detailed printouts strategically placed around the function. Most importantly, it enables a query of what you just inserted, to ensure everything was entered correctly.
<br>
### \_\_doQ\_\_(cols='*', where=False, like=False, tgt_col=None, qry=None, pos='any')

The querying workhorse. Generates valid queries from given arguments. Can query by full/first/last name, 'where' direct lookup of value, 'where/like' lookup of partial values, or regex searches. If no direct matching produces results, it automatically finds and suggests possible matches.
It was built with expandabilty in mind, so future versions of this program can easily implement methods for searching by other columns besides 'name'.

**Takes:**
- cols - The column name as a string or a list of strings representing valid column names. The values are used in the "SELECT ... FROM" part of the statement. Defaults to '*' to return all columns per match
- where - *requires tgt_col & qry* \- set to True to enable WHERE direct lookup, with arg "pos='rgx'" to use regex matching, or with arg "like=True" to enable "WHERE...LIKE" matching. Default is False.
- like - *requires where=True, tgt_col and qry* \- when True it enables "WHERE...LIKE" matching. Default is False.
- tgt_col - *required for all where uses* \- a string representing the column whose values you'll be checking with a WHERE, WHERE...LIKE or REGEX statement.
- qry - *required for all where uses* \- a string representing the search term, whether it be a full name, partial name (first, last or chars in name), alpha character(s) or a regex string.
- pos - used to toggle between different WHERE...LIKE matching modes, or to select REGEX matching when used with where=True & like=False.  The acceptable values are:
    - any - matches chars at any location in string  AKA:  %qry%
    - start - matches chars at start of string AKA: qry%
    - end - matches chars at end of string AKA: %qry
    - rgx - enables use of regex strings as 'qry' when like=False (or is left omitted)

**Returns:**
List of tuples containing match data.  The elements of returned data are determined by the 'cols' argument, which by default returns all rows.
<br>
### \_\_allCol\_\_(col='name')
Method to produce a list of desired column values.  Accepts a string or a list of strings representing valid column names.

**Takes:** 
- col - The string name of the target column, or a list of string names.  Default is column 'name'.

**Returns:**
A list of the full names of existing entries for given column(s)
<br>

### \_\_delContact\_\_(name)
A method to delete an entire entry (row) by it's name column value.  

**Takes:**
- name - a string representing the full name of the entry to delete

A name 'string' is passed to a __doQ__() call, which performs a where statement lookup.  IF the name is found, it asks the user for confirmation before doing the actual delete. 
(Could be expanded to lookup by different column types, and to print the proposed deletion row to the user along with the confirmation dialog)
<br>

### \_\_getCols\_\_()
Very simple method to return all of the column names.  Used for testing & debugging and a few internal functions
<br>

### \_\_chkCols\_\_(cols)
Private method to check a given input of columns against the list of valid columns.  

**Takes:**
A list of column names, even if a single entry.

**Returns:**
0 if the given columns are in the list of valid columns.  1 otherwise.
<br>

### \_\_chkForRgx__(qry)
Private method to check a given string for existence of regex special characters.

**Takes:**
A string

**Returns:**
0 if there is a regex special character in the string.  1 otherwise.
<br>

### findContactByName(qry, pos='any', verbose=True, dgb=False)
Robust public method leveraging \_\_doQ\_\_() to do a complex entry lookup by entry name.  
 **Takes:**
 - qry - *required* - a string representing the search term, whether it be a full name, partial name (first, last or chars in name), alpha character(s) or a regex string
 - pos - used to toggle between different WHERE...LIKE matching modes, or to select REGEX matching when used with where=True & like=False.  *See __doQ__ section for allowed values*
 - verbose - set to True to enable extra prints detailing the process.  Default is True
 - dgb - set to True to enable additional debug messages and internal value prints.  Default is False

**Returns:**
A printed list of the matching rows or a printed list of suggested potential matches, depending on the query.
 
 Begins by asking the user whether they want to match their 'qry' by first/last/full name, or to skip ahead.  
 Next the 'qry' is checked for the existence of a regex special char.  If there is one in the qry string, use it in a __doQ__ Where...Regex query.  
 If not, then check the string for a space.  If there is a space, split the string and use each resulting element in __doQ__ calls.
 Next, check for any matches so far, and if there is None, go through testing for rgx based possibilities.
<br>

### findContactByRgx(what_col, query):
A simple public method to look up entries by name using regex.

**Takes:**
- what_col - *required* - is a string or list of strings representing valid column names
- query - *required* - a string, which is at best an actual regex string

**Returns:**
An output list containing the full match rows along with a prinout of the number of matches.

This method leverages \_\_chkForRgx\_\_() to confirm a regex character in the query string, and \_\_doQ\_\_() to do the actual sql query.
<br>

### updContact(where='name', who=None, dbg=False, **kwargs)

A public method to update select values in an entry.

**Takes:**
- where - a string representing the column to use in the WHERE condition check.  Default is 'name'
- who - the string representing the value to use in the WHERE condition check
- dbg - set to True to enable additional debug messages and internal value prints.  Default is False
- \*\*kwargs - arguments to be used as the actual data to update and update with.  Must be in "column='value', column2='value2'..." format, where the *column* is an unquoted keyword and the  *value* is a quoted string.

First the value of 'who' is checked for whether a value was given, and if so, the db is queried to check for whether that 'who' exists.  If it does, we can continue.
Next, the given column names are extracted from kwargs and compared to the list of valid columns.  If it passes, the string arguments to pass into the query are built and appended to the query statement.
The statement is executed in a try/except block.  If debug is enabled, there is a final check to confirm the update applied correctly (to be visually confirmed by user)
<br>

### mkContact(name, address, phone, workphone, email)

A very basic method to create a new contact.

**Takes:** 
All required arguments map to valid columns for the entry.

This method leverages private \_\_addContact\_\_() within a try/except block
<br>

### delContact(name)

A method to completely delete the row of an entry by it's full name

**Takes:**
- name - *required* - a string representing the full name of the entry to delete

This method leverages private \_\_delContact\_\_() within a try/except block.
