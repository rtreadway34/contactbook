''' Simple Contact Book
A program to organize contacts
'''
import sqlite3 as sql
import time, re
import os
import sys

class contactBook:
    '''Arg 'db' can be given if the user wants to use an existing db. It will be checked for compatability later.
    Arg 'mode' only will take 'm' for an argument, and specifies using a memory db.  This was used for easier debugging.''' 
    def __init__(self,db=None,mode=None, dbg=False):
        self.db = db
        self.mode = mode
        self.dbobj = None
        self.dbg = dbg
        # This list of valid column names
        self.cols = ['id', 'name', 'firstname', 'lastname', 'address', 'phonenum', 'worknum', 'email', 'added']
        ### Inner method to init SQL db if not exists, or none given
        # db can be the db name if it's in the same folder as the program OR if creating a new one in the current dir.  It can also be the path leading to the target db, or location to make a new one.
        def __dbconnect__(db):
            try:
                self.dbobj = sql.connect(db)
            except Exception as e:
                print("Failed to load db. Review and try again.")
                print(e.__class__,'-',e)
            else:
                print(f"Connection made to {db}")

        def __colChkr__(expected, dbcols):
            print("COLCHKR input: ",dbcols)
            #if all((c in set(expected))for c in dbcols) == True:
            if all((c in set(dbcols))for c in expected) == True:
                return 0
            else:
                return 1

        def __getCols__(db):
            ''' Method to grab just the column names, returning a list of them. '''
            tmp_dbobj = sql.connect(db)
            contact_crs = tmp_dbobj.cursor()
            contact_crs.execute("PRAGMA table_info('contacts')")
            cols = [x[1] for x in contact_crs.fetchall()]
            tmp_dbobj.close()
            print("GETCOLS: ", cols)
            return cols


        def __dbChkr__(db):
            ''' Internal Database Validator 
            This internal method ensures a given database is compatable with the program by checking for the
            'contacts' table and then the valid columns.
            User propmpt loops are given so the user can easily determine the course of action depending on what the method
            determines.
            It's divided into sections to account for different situations of an existing database (see SECTION comments below)
            Each section will return a tuple whose first element is the section letter and the second an informational string or 
            int result of __colChkr__() which are used in the MAIN INIT BLOCK to determine what to ask of and present to the user, 
            and what actions will be taken in processing. (for ex. ('a', 'new') reflects user choice within Section A to make a new db)'''
            tmp_dbobj = sql.connect(db)
            chk_dbobj = tmp_dbobj.cursor()
            chk_dbobj.execute("SELECT name FROM sqlite_master WHERE type='table'")
            db_list = chk_dbobj.fetchall()
            db_list = [x[0] for x in db_list]
            if self.dbg == True:
                print(db_list)
            # SECTION A: accounting for multiple tables and the existence of 'contacts' table
            if len(db_list) > 1 and 'contacts' in db_list:
                print("Has other tables besides contacts")
                while True:
                    dbchk_q = input("Do you want to use the table 'contacts' in this db? [y|n or m to make new]: ")
                    ans = dbchk_q.lower()
                    if ans  == 'y':
                        print(f"Using 'contacts' from db '{db}'")
                        print("Checking columns from table 'contacts'")
                        colchk_result = __colChkr__(self.cols, __getCols__(db))
                        tmp_dbobj.close()
                        return ('a',colchk_result)
                    elif ans == 'n':
                        print("Exiting program")
                        tmp_dbobj.close()
                        sys.exit()
                    elif ans == 'm':
                        print("Making new db(To be implemented)")
                        return ('a', 'new')
                    else:
                        print("Incorrect choice. Please choose 'y' to use, 'n' to quit or 'm' to make new")
            # SECTION B: accounting for multiple tables WITHOUT the existence of 'contacts' table
            elif len(db_list) > 1 and 'contacts' not in db_list:
                while True:
                    print("Has multiple tables, but no contacts.")
                    dbchk_q = input("Do you want to add contacts table to this db? [y|n|m]: ")
                    ans = dbchk_q.lower()
                    if ans == 'y':
                        print(f"Adding table 'contacts' to db '{db}'")
                        tmp_dbobj.close()
                        return ('b','add')
                    elif ans == 'n':
                        print("Exiting program")
                        tmp_dbobj.close()
                        sys.exit()
                    elif ans == 'm':
                        print("Making new db")
                        return ('b','new')
                    else:
                        print("Incorrect choice. Please choose 'y' to add table contacts, 'n' to quit or 'm' to make new")
            # SECTION C: accounting for a single 'contacts' table
            elif len(db_list) == 1 and db_list[0] == 'contacts':
                print("Contacts table found and is the only table. Checking tables.")
                colchk_result = __colChkr__(self.cols, __getCols__(db))
                tmp_dbobj.close()
                return ('c',colchk_result)
            # SECTION D: accounting for an empty database
            elif len(db_list) < 1:
                print("Empty db. We're going to use this.")
                tmp_dbobj.close()
                return ('d', 'good')
            else:
                raise Exception("Unknown exception while checking tables in db")
        
        def __makeNewdb__():
            while True:
                new_q = input("Do you want to make a new db? [y|n]: ")
                new_q = new_q.lower()
                if new_q == 'y':
                    name_q = input("Enter the path and db name, or just the db name to create in current dir: ")
                    name_q = name_q.lower()
                    __dbconnect__(name_q)
                    __tableInit__()
                    break
                elif new_q == 'n':
                    print("Aborting new db creation. Exiting.")
                    sys.exit()
                else:
                    print("Please choose 'y' or 'n'.")
                    continue 
        def __tableInit__():
            try:
                self.dbobj.execute('''CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY, name TEXT NOT NULL, firstname TEXT NOT NULL, lastname TEXT NOT NULL, address TEXT NULL, phonenum TEXT NULL, worknum TEXT NULL, email TEXT NULL, added TIMESTAMP)''')
            except Exception as e:
                print("Table initialization failed for some reason.  Try again.",e.__class__,'-',e)
            else: 
                print("Table initialized. Please Continue.")


        ''' MAIN INIT BLOCK 
        First checks for arg "mode" to determine whether db will be made in memory for testing.
        Then checks whether a db name was given, and if so leverages __dbChkr__ to determine 
        the course of action dependent on the state of the db and the subsequent user choice.
        This can account for existing dbs with mulitple tables with or without the required 'contacts' table,  
        can account for incorrect columns if 'contacts' table is found, and can utilize existing empty databases.
        The user is given options throughout to use the given existing database depending on its state, opt to 
        create a new database instead, or simply abort the program without changes.
        If no database is given, the user is given the option to create and initialize a new one.'''
        if self.dbg == True:
            print("self.db: ",self.db)
        if self.mode == 'm':
            __dbconnect__(':memory:')
        elif self.mode == None:
            if self.db != None:
                # Does it pre-exist?
                if os.path.exists(self.db) == True:
                    # check the db for validity
                    dbchk_return = __dbChkr__(self.db)
                    if self.dbg == True:
                        print(dbchk_return)
                    if dbchk_return[0] == 'a':
                        if dbchk_return[1] == 0:
                            # table & cols good
                            __dbconnect__(self.db)
                        elif dbchk_return[1] == 1:
                            print("column check failed. Exiting.")
                            sys.exit()
                        elif dbchk_return[1] == 'new':
                            # go to makeNew
                            __makeNewdb__()
                    elif dbchk_return[0] == 'b':
                        if dbchk_return[1] == 'add':
                            # add contacts to db & init
                            __dbconnect__(self.db)
                            __tableInit__()
                        elif dbchk_return[1] == 'new':
                            # go to makeNew
                            __makeNewdb__()
                    elif dbchk_return[0] == 'c':
                        if dbchk_return[1] == 0:
                            # table cols good
                            __dbconnect__(self.db)
                        elif dbchk_return[1] == 1:
                            # table cols bad
                            print("Table column check failed. Exiting.")
                            sys.exit()
                    elif dbchk_return[0] == 'd':
                        print("Good, using empty db")
                        __dbconnect__(self.db)
                        __tableInit__()
            else:
                print("No db given")
                __makeNewdb__()
        
        # Sqlite3 regex function
        def regexp(qry,tgt):
            reg = re.compile(qry)
            return reg.search(tgt) is not None
        self.dbobj.create_function("REGEXP",2,regexp)
        # Finally...
        print("db initialized")


    def __str__(self):
        # Basic print formatting
        # NOTE: modify with better layout & info
        return "***************\nContact Book Class\nPass mode='m' to run db in memory\nTakes columns:{}\nExisting entries: {}".format(self.cols[1:],self.__allCol__())


    def __addContact__(self, name, addr=None, phnum=None, wknum=None,email=None,added=time.ctime()):
        ''' Simple inflexible Method to add contact information '''
        # split the full name into first and last
        fname, lname = name.split()[0], name.split()[1]
        stmt = "INSERT INTO contacts(name,firstname,lastname,address,phonenum,worknum,email,added)VALUES(?,?,?,?,?,?,?,?)"
        vals = (name,fname,lname,addr,phnum,wknum,email,added)
        try:
            self.dbobj.execute(stmt,vals)
        except Exception as e:
            print("Exception encountered when trying to insert.",e.__class__,'-',e)
        else:
            return "New contact added successfully"


    def __insQ__(self,dbg=self.dbg,**kwargs):
        ''' Flexible insertion method, used by other funcs
        kwarg Syntax: column='value'
        column must be entered as a keyword, without quotes, and must be a valid column
        Kwarg keywords converted to usable strings and put in a list
        Kwarg values get their own list
        Currently not really used much in program, but is very ready for expandability.'''
        cols = [str(k) for k,v in kwargs.items()]
        vals = [v for k,v in kwargs.items()]
        # Check for empty resultant lists
        if cols == [] or vals == []:
            raise Exception("Error: column=value arguments missing")
        # The 'base' for building the query insertion placeholder string
        valQs='?'
        
        # Run column check on given kwargs columns, to ensure they're correct
        if self.__chkCols__(cols) == 0:
            # If the columns are good, check for a full name and prepare a first & last name for insertion.  Also update the valQs query insertion placeholder string
            if 'name' in cols:
                # process into firstname & lastname, then append to where & vals
                firstname = kwargs['name'].split()[0]
                lastname = kwargs['name'].split()[1]
                valQs += "?," * 2
                cols.append('firstname')
                cols.append('lastname')
                vals.append(firstname)
                vals.append(lastname)
            # Next, check how many columns we have, so we can accurately build the string of columns for the query, as well as the matching insertion placeholder string
            if len(cols) > 1 :
                cols = ",".join(cols)
                valQs = "?,"* len(vals)
        # Check the built insertion placeholder string for a trailing comma and remove it
        if valQs.endswith(',') == True:
                valQs = valQs.rstrip(',')
        # build the SQL insertion statement        
        stmt= f"INSERT INTO contacts({cols})VALUES({valQs})"
        # debug info output, if arg dbg=True
        if dbg == True:
            print("cols: ", cols)
            print("valQs: ", valQs)
            print("Values: ",vals)
            print("Constructed Statement: ",stmt)
        # Create a cursor object for the insertion
        ins_crs = self.dbobj.cursor()
        # Attempt the insertion
        try:
            ins_crs.execute(stmt,vals)
        except Exception as e:
            print(e.__class__,'-',e,":: Something went wrong with the insertion. Check & try again.")
        else:
            print("Insert executed successfully")
            # Debug only: check the insertion is correct, searches by the kwargs fullname
            if dbg == True:
                print("Testing last insertion. Should produce row inserted")
                print(self.__doQ__(tgt_col='name',where=True,pos='rgx',qry=kwargs['name']))


    def __doQ__(self, cols='*',where=False,like=False, tgt_col=None, qry=None, pos='any'):
        ''' Robust query builder and executor 
        Arg 'cols' are the columns you wish to get info from. Default is ALL
        Arg 'where' enables additional WHERE statement for refining searches. Default is DISABLED
        Arg 'like' enables additional LIKE statement to refine WHERE statements. This requires where=True.  Default is DISABLED.
        Arg 'tgt_col' is the column used in a WHERE statement for refining a search. It's codependent with arg 'where'.  Default is None.
        Arg 'qry' is the value you want to target in WHERE, WHERE..LIKE and WHERE..REGEX statements.  Default is None.
        Arg 'pos', given where=True and like=true,  is used to select the type of query desired from choices any(LIKE %qry%), start(LIKE qry%), end(LIKE %qry), rgx(REGEXP qry) or None(disabled). If using where & like, this is required.  If using REGEX, like must be False.  Default is 'any'.'''

        crs = self.dbobj.cursor()
        # Default selection is "all"
        # Converting list of col names into SQL compatable string:
        if type(cols) == list:
            cols = ", ".join(cols)
        # building statement foundation
        stmt = f"SELECT {cols} FROM contacts"
        # building various statement extensions
        wh_blk = f" WHERE {tgt_col} = '{qry}'"
        wh_rgx = f" WHERE {tgt_col} REGEXP '{qry}'"
        whlk_stwth = f" WHERE {tgt_col} LIKE '{qry}%'"
        whlk_endwth = f" WHERE {tgt_col} LIKE '%{qry}'"
        whlk_any = f" WHERE {tgt_col} LIKE '%{qry}%'"
        
        # Block to control selection of query type
        if where == True and like == True:
            if tgt_col != None and qry != None:
                if pos == 'any':
                    stmt = stmt + whlk_any
                elif pos == 'start':
                    stmt = stmt + whlk_stwth
                elif pos == "end":
                    stmt = stmt + whlk_endwth
                elif pos == "rgx":
                    raise Exception("Argument pos='rgx' can only be selected when like=False")
                else:
                    raise Exception("Bad choice for 'pos'. Choose any|start|end")
            else:
                raise Exception("Missing tgt_col and/or qry args")
        elif where == True and like == False:
            if tgt_col != None and qry != None:
                if pos == 'rgx':
                    stmt = stmt + wh_rgx
                else:
                    stmt = stmt + wh_blk
            else:
                raise Exception("Missing tgt_col and/or qry args. [elif-non-like]")
        try:
            crs.execute(stmt)
        except Exception as e:
            print("Something went wrong with the query. Check your args.",e.__class__,'-',e)
        else:
            # If query successful, capture the output, then ensure it's not empty. If not empty, return it
            out = crs.fetchall()
            if out == []:
                return "Nothing found"
            else:
                return out


    def __allCol__(self,col='name'):
        ''' Method to grab the rows for given column(s).  Input 'cols' can be a string or list of strings representing valid column names.  Returns the result of the __doQ__ query.'''
        if type(col) == list:
            return self.__doQ__(cols=",".join(col))
        else:
            out = self.__doQ__(cols=col)
            return [x[0] for x in out]

    
    def __delContact__(self,name):
        ''' Method for deleting an entire entry
        Arg 'name' is a string representing the full name of the entry to delete'''
        # Leveraging __doQ__ to get the row for the given name, so we can first ensure it exists
        sel = self.__doQ__(cols='name',where=True,tgt_col='name',qry=name)
        if sel == []:
            raise Exception("Name '{}' not found in db.".format(name))
        elif sel[0][0] == name:
            print("Name '{}' found.".format(name))
            # Double check with user prior to delete.
            q = input("Are you sure you want to permanently delete entry for '{}' ? [y|n] ".format(name))
            if q == 'y':
                try:
                    self.dbobj.execute(r"DELETE FROM contacts WHERE name='{}'".format(name))
                except SyntaxError as se:
                    print("Name not found. Make sure you spelled it correctly.")
                    print(se.__class__,'-',se)
                else:
                    self.dbobj.commit()
                    print("Entry for '{}' successfully deleted".format(name))
            else:
                print("Deletion of '{}' aborted. No changes made.".format(name))
        else:
            raise Exception("Name not found in db. Check spelling and try again.")


 
    def __chkCols__(self, cols:list):
        '''Method to compare a list of column names against the list of valid columns.  ALL must match to be considered correct.'''
        if all((c in set(self.cols[1:])) for c in cols):
            print("Given columns check out. Prepping args for update")
            return 0
        else:
            return 1

    def __chkForRgx__(self,qry):
        ''' Checks a query for existence of regex chars '''
        spchars = ['.','^','$','-','[',']','(',')','|']    
        if any((c in set(spchars)) for c in qry):
            return 0
        else:
            return 1

    def findContactByName(self,qry,pos='any',verbose=True,dbg=self.dbg):
        ''' Forward facing method for finding a contact in the db by their name.  User can choose to match by full, first or last name. '''
        ### FIRST ROUND: Lookup by the specific name ###
        # Ask user if they are checking by first/last/full name initially, then run check based on their answer
        q_name = input("Do you want to attept to match first, last or full name for the initial search? [first|last|full], enter to skip ")
        if q_name == 'first':
            output = self.__doQ__(where=True,tgt_col='firstname',qry=qry)
            outlike = self.__doQ__(where=True, like=True,tgt_col='firstname',qry=qry,pos=pos)
        elif q_name == 'last':
            output = self.__doQ__(where=True,tgt_col='lastname',qry=qry)
            outlike = self.__doQ__(where=True, like=True,tgt_col='lastname',qry=qry,pos=pos)
        elif q_name == 'full':
            output = self.__doQ__(where=True,tgt_col='name',qry=qry)
            outlike = self.__doQ__(where=True, like=True,tgt_col='name',qry=qry,pos=pos)
        else:
            output = "Nothing found"
            outlike = "Nothing found"
            if verbose == True:
                print("Skipping check-by-name")

        ### SECOND ROUND: When name based check fails, check for a regex char in the qry
        if output == "Nothing found":
            if verbose == True:
                print(f"Nothing coming up for whole word '{qry}', digging deeper...")
            # First check if input qry has rgx chars, then use
            if verbose == True:
                print("Proceeding with regex char check...")
            if self.__chkForRgx__(qry) == 0: 
                if verbose == True:
                    print("Rgx char found")
                output = self.__doQ__(where=True,tgt_col='name',qry=qry, pos='rgx')

            ### THIRD ROUND When rgx char not found in qry, check for a space in qry. If space, assume space-sep fullname, split it and qry each name. This can help account for typos
            elif ' ' in qry:
                if verbose == True:
                    print("No rgx chars, but space found. Attempting to split whole name into 2 queries...")
                qry = qry.split()
                outlist = set()
                likelist = set() 
                # Loop through the split
                for i in qry:
                    # tmp qry output storage to check returned value first
                    if dbg == True:
                        print("Space round i:",i)
                    tmp = self.__doQ__(where=True,like=True,tgt_col='name',qry=i)
                    if dbg == True:
                        print("Space round tmp:",tmp)
                    if tmp != 'Nothing found':
                        outlist.add(tmp[0])
                # If outlist collected no matches, run the same kind of loop for possible matches
                # NOTE: These should be checking for empty set, not empty list, right?
                if outlist == set():
                    if verbose == True:
                        print("No direct matches, testing possibilities...")
                    for i in qry: 
                        tmp = self.__doQ__(where=True, like=True,tgt_col='name',qry=i,pos=pos)
                        if tmp != "Nothing found":
                            likelist.add(tmp[0])
                    outlike = likelist
                    if outlike == []:
                        outlike = "Nothing found"
                # If we did get matches for 'output' in our collection list(actually a set), then make that 'output'
                else:
                    output = outlist

        ### FOURTH ROUND ###
        # If there IS NOT something in output, first process as rgx string for possibilities
        # If there IS something in output, go to that block
        if output == "Nothing found":
            if verbose == True:
                print("No regular matches. Checking accumulated possibilities...")
            # Process possibilities by rgx
            if outlike == "Nothing found":
                tmp = self.__doQ__(where=True,tgt_col='name',pos='rgx',qry=qry)
                # If rgx matching found something, print each match (will have to create an output func to format text)
                if tmp != "Nothing found":
                    outlike = tmp
                if outlike != "Nothing found":
                    if verbose == True:
                        print("***********************")
                        print("Possibilities found: ")
                    outlike_list = []
                    for i in outlike:
                        outlike_list.append(i)
                    print(outlike_list)
                    if verbose == True:    
                        print("Total possibilities considered: ",len(outlike))
            # If nothing at all found, print msg
            else:
                print("End of the line. Nothing matched.")
        # If we did get actual matches (not including possibilities)
        elif output != "Nothing found":
            if verbose == True:
                print("Matches Ping! (First 3 rounds produced nothing)")
                print("Total matches found: ",len(output))
            q_prnt = input("Would you like to print the list of matches? [y|n]")
            if q_prnt == 'y':
                for i in range(len(output)):
                    print(output[i])

    def findContactByRgx(self, what_col, query):
        ''' Method for finding contacts by REGEX 
        Arg 'what_col' is the 'tgt_col' of the __doQ__ internal method, and is a string representing the target column for a WHERE statement
        Arg 'query' is a REGEX string to use'''
        # First ensure Regex characters are used in the query arg
        if self.__chkForRgx__(query) == 0: 
            # If so, then execute the query, returning the output list of matches
            output = self.__doQ__(where=True,tgt_col=what_col,qry=query, pos='rgx')
            print(f"Found {len(output)} matches")
            return output
        else:
            return f"No contact found with regex string '{query}'"
    
    def updContact(self, where='name', who=None, dbg=self.dbg, **kwargs: str):
        ''' Method for updating an existing contact with new information
        Arg 'where' is the target column for the WHERE statement used to determine existing contact.  Default is 'name'
        Arg 'who' is used to select the desired contact to update. It's value depends on the 'where' column targeted, for example if where='name', 'who' should be the fullname of the target. Default is None, but it's obviously recommended to use it.
        Arg dbg enables additional debug info printouts.  Default is DISABLED.
        Kwargs represent the the actual information to update the contact with. These must be a comma separated sequence of column='value' args, where the column must be a valid column name.'''
        # Checking the 'who' argument, since it's required
        if who == None:
            raise Exception("Please enter the name of the target to update as the 'who' arg")
        else:
            # If we have a 'who', leverage __doQ__ to query the db and ensure it's existence in the db
            check = self.__doQ__(cols='name', where=True, tgt_col='name',qry=who)
            if dbg == True:
                print(check)
            if check[0][0] == who:
                print("Name found")
            else:
                raise Exception("Name not found in database.")
        # Checking the given kwargs for whether valid columns are keywords. 
        # IF so, build the set of arguments to pass into the statment 
        cols = [str(k) for k,v in kwargs.items()]
        if self.__chkCols__(cols) == 0: 
            arg_set = ''
            # Loop to build a SQL compatable string of column/value pairs to use as the update
            for col, val in kwargs.items():
                arg_set += f"{col}='{val}',"
            arg_set = arg_set.rstrip(',')
            if dbg == True:
                print(arg_set)
        else:
            raise Exception("Bad columns given as keywords. Double check spelling & usage of valid column names")
        # Build the statement and attempt execution
        stmt = f"UPDATE contacts SET {arg_set} WHERE {where}='{who}'"
        if dbg == True:
            print("STMT is: ",stmt)
        try:
            self.dbobj.execute(stmt)
        except Exception as e:
            print("Update failed")
            print(e.__class__,'-',e)
        else:
            # Confirm to user update success.  Optional debug block to visually confirm given information got into the db appropriately
            print("Update completed successfully")
            if dbg == True:
                print("Checking update..")
                dbg_cols = ['name']+cols
                print("DBGCOLS: ",dbg_cols)
                check = self.__doQ__(cols=dbg_cols,where=True,tgt_col='name',qry=who)
                print("UPD CHECK:",check)
                print(f"Versus: \n{kwargs}")

    def mkContact(self, name, address, phone, workphone, email):
        ''' A forward facing wrapper for the internal __addContact__, with exception checking
        All args are required and represent the values to insert for the contact'''
        try: 
            self.__addContact__(name,addr=address,phnum=phone,wknum=workphone,email=email)
        except Exception as e:
            print("Something went wrong with the add")
            print(e.__class__,'-',e)
        else:
            print("Contact successfully added")
            
    def delContact(self,name):
        ''' Method wrapper for internal __delContact__, based on target fullname, with exception checking'''
        try:
            self.__delContact__(name)
        except Exception as e:
            print("Deletion failed for some reason.")
            print(e.__class__,'-',e)
        else:
            print("Delete executed successfully")
