import contacts as c

# To test not-exists-make-new functionality
# IT WORKS
#book = c.contactBook()

# To test exists-is-good? functionality
# testing db with only 'contacts' w/ correct cols (C)
#book = c.contactBook('fatshit.db')
# testing db with multicols, w/ correct contacts (A)
#book = c.contactBook('testwcontacts.db')
# testing db w/ multicols, w/ contacts but bad cols (A)
#book = c.contactBook('testBadCols.db')
# testing db w/ multicols w/o contacts (B)
book = c.contactBook('test.db')
# testing empty db
#book = c.contactBook('testempty.db')
# testing memory db
#book = c.contactBook(mode='m')

#print(book.__globals__.__getCols__())

# should fail
#book = c.contactBook('old/holyshit.db')

# Add contacts
book.mkContact('Roger Moore','354 Baker St.','645-333-2352', '124-442-2623','rm007@gmail.com')
book.mkContact('Donal Toaph','16-23 Money Ln.','888-362-3425', '888-262-3631','bigToaph@proton.me')
book.mkContact('Magda Davis','12 Appalachian Rd.','845-252-4738', '845-232-1121','mdTulip3@gmail.com')
book.mkContact('Roger Bacon','111 Bacon St.','212-252-9811','212-582-2182','baconator55@hotmail.com')

# Find By Name
book.findContactByName('Roger',dbg=True)
