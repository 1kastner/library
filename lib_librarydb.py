#!/usr/bin/python
#library programm function library

import sqlite3

import datatypes
import wrapper_set

class Persons:
    """
    Just everything about adding, editing and removing persons
    """

    def __init__(self, sqldbconnection, sqldbcursor):
        self.con = sqldbconnection
        self.cur = sqldbcursor
        self.cur.execute("""CREATE TABLE IF NOT EXISTS persons (person_id TEXT, 
                                                                firstname TEXT, 
                                                                surname TEXT, 
                                                                class TEXT,
                                                                semester TEXT,
                                                                cellphone TEXT)""")
        self.con.commit()

    def _person_exists(self, person_id):
        self.cur.execute("SELECT person_id FROM persons WHERE person_id = ?", (person_id, ))
        if self.cur.fetchone():
            return True
        else:
            return False

    def add_person(self, person_id, firstname, surname, _class, semester, cellphone, edit_mode=False):

        if not person_id:
            return False, 'Please specify a person id'
        if not firstname:
            return False, 'Please specify a first name'
        if not surname:
            return False, 'Please specify a surname'
        if not _class:
            return False, 'Please specify a class'
        if not semester:
            return False, 'Please specify a semester'

        person_id = datatypes.PersonID(person_id)
        firstname = datatypes.Name(firstname)
        surname = datatypes.Name(surname)
        _class = datatypes._Class(_class)
        semester = datatypes.Semester(semester)
        cellphone = datatypes.Cellphone(cellphone)

        if not person_id.isvalid():
            return False, 'The person ID contains bad elements: '+person_id.value
        if not firstname.isvalid():
            return False, 'The first name contains bad elements: '+firstname.value
        if not surname.isvalid():
            return False, 'The surname contains bad elements: '+surname.value
        if not _class.isvalid():
            return False, 'The class contains bad elements: '+_class.value
        if not semester.isvalid():
            return False, 'The semester contains bad elements: '+semester.value
        if not cellphone.isvalid():
            return False, 'The cellphone contains bad elements: '+cellphone.value

        if self._person_exists(person_id) and not edit_mode:   
            return False, "There is already one person with this person ID in the database: " + person_id

        if edit_mode:
            self.cur.execute("DELETE FROM persons WHERE person_id = ?", (person_id,))

        values = (person_id, firstname, surname, _class, semester, cellphone.database_format())

        self.cur.execute("""INSERT INTO persons (person_id, firstname, surname, class, semester, cellphone)
                                         VALUES (?, ?, ?, ?, ?, ?)""", values)
        return True, None

    def edit_person(self, person_id, firstname, surname, _class, semester, cellphone):
        return self.add_person(person_id, firstname, surname, _class, semester, cellphone, edit_mode = True)

    def delete_person(self, person_id):
        person_id = datatypes.PersonID(person_id)
        if not person_id.isvalid():
            return False, "The person ID contains bad elements: "+person_id, None
        if not self._person_exists(person_id):
            return False, "This person ID does not belong to anybody: "+person_id, None

        _is, msg = Books(self.con, self.cur).lent_books_to(person_id)
        if _is and msg:
            return False, "This person still possesses books", msg

        self.cur.execute("DELETE FROM persons WHERE person_id = ?", (person_id, ))
        return True, None, None

    def search_person(self, person_id, firstname, surname, _class, semester, cellphone):
        #empty string if none
        res = list() # the result

        if not (person_id or firstname or surname or cellphone or _class or semester):
            return False, "No search parameters given"

        person_id = datatypes.PersonID(person_id)
        firstname = datatypes.Name(firstname)
        surname = datatypes.Name(surname)
        _class = datatypes._Class(_class)
        semester = datatypes.Semester(semester)
        cellphone = datatypes.Cellphone(cellphone)

        if person_id and not person_id.isvalid():
            return False, 'The person ID contains bad elements: '+person_id
        if firstname and not firstname.isvalid():
            return False, 'The first name contains bad elements: '+firstname
        if surname and not surname.isvalid():
            return False, 'The surname contains bad elements: '+surname
        if _class and not _class.isvalid():
            return False, 'The class contains bad elements: '+_class
        if semester and not semester.isvalid():
            return False, 'The semester contains bad elements: '+semester
        if cellphone and not cellphone.isvalid():
            return False, 'The cellphone contains bad elements: '+cellphone

        if person_id:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE person_id = ?""", (person_id,))
            res.extend(self.cur.fetchall())

        if cellphone:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE cellphone = ?""", (cellphone.database_format(),))
            res.extend(self.cur.fetchall())

        if firstname and surname:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE lower(firstname) = ? and lower(surname) = ?""", (firstname.lower(), surname.lower()))
            res.extend(self.cur.fetchall())

        if surname and _class and semester:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE lower(surname) = ? and class = ? and semester = ?""",
                            (surname.lower(), _class, semester))
            res.extend(self.cur.fetchall())

        if surname and _class:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE lower(surname) = ? and class = ?""", (surname.lower(), _class))
            res.extend(self.cur.fetchall())

        if firstname and _class and semester:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE lower(firstname) = ? and class = ? and semester = ?""",
                            (firstname.lower(), _class, semester))
            res.extend(self.cur.fetchall())

        if firstname and _class:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE lower(firstname) = ? and class = ?""", (firstname.lower(), _class))
            res.extend(self.cur.fetchall())

        if firstname and len(res)<5:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE lower(firstname) = ?""", (firstname.lower(), ))
            res.extend(self.cur.fetchall())

        if surname and len(res)<5:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE lower(surname) = ?""", (surname.lower(),))
            res.extend(self.cur.fetchall())

        if _class and semester and len(res)<5:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE class = ? and semester = ?""", (_class, semester))
            res.extend(self.cur.fetchall())

        if _class and not res:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE class = ?""", (_class,))
            res.extend(self.cur.fetchall())

        if semester and not res:
            self.cur.execute("""SELECT person_id, 
                                       firstname, 
                                       surname, 
                                       class, 
                                       semester, 
                                       cellphone FROM persons WHERE semester = ?""", (semester,))
            res.extend(self.cur.fetchall())

        result = list()
        for row in res:
            if row[0] not in result:
                result.append(row)
        return True, result

    def show(self):
        self.cur.execute("SELECT person_id, firstname, surname, class, semester, cellphone FROM persons WHERE 1")
        return self.cur.fetchall()


class Books:
    """
    Just everything about adding, editing and removing books
    """
    
    def __init__(self, sqldbconnection, sqldbcursor):
        self.con = sqldbconnection
        self.cur = sqldbcursor
        self.cur.execute("""CREATE TABLE IF NOT EXISTS books (book_id INTEGER PRIMARY KEY ASC AUTOINCREMENT, 
                                                              author TEXT, 
                                                              title TEXT,
                                                              amount INTEGER,
                                                              tags TEXT)""")

    def _book_exists(self, book_id):
        self.cur.execute("SELECT book_id FROM books WHERE book_id = ?", (book_id, ))
        if self.cur.fetchone():
            return True
        else:
            return False

    def add_book(self, author, title, amount, tags, edit_mode=False, book_id_to_edit=None):
        author = datatypes.Name(author)
        if not author.isvalid():
            return False, 'The author contains bad elements: '+author
        if int(amount) == 0 or not str(amount).isdigit():
            return False, 'The amount contains nondigit elements: '+str(amount)

        self.cur.execute("SELECT book_id FROM books WHERE author=? and title=?", (author, title,))
        
        if self.cur.fetchone() and not edit_mode:
            return False, "There is already the book '"+title+"' written by '"+author
        
        if edit_mode:
            if not self._book_exists(book_id_to_edit):
                return False, 'The book supposed to be edited does not exist: '+book_id_to_edit
            self.cur.execute("DELETE FROM books WHERE book_id = ?", (book_id_to_edit,))
            self.cur.execute("""INSERT INTO books (book_id, author, title, amount, tags)
                                         VALUES (?, ?, ?, ?, ?)""", (book_id_to_edit, author, title, amount, tags))
        else:
            self.cur.execute("""INSERT INTO books (author, title, amount, tags)
                                         VALUES (?, ?, ?, ?)""", (author, title, amount, tags))

        return True, None

    def edit_book(self, book_id, author, title, amount, tags):
        return add_book(author, title, amount, tags, edit_mode=True, book_id_to_edit=book_id)

    def delete_book(self, book_id):
        if not self._book_exists(book_id):
            return False, "No such book in the database: " + str(book_id)  

        self.cur.execute("SELECT person_id FROM librarysystem WHERE book_id = ?", (book_id,))
        res = self.cur.fetchall()
        if not res:
            self.cur.execute("DELETE FROM books WHERE book_id = ?", (book_id, ))
            return True, None
        else:
            answer = "The book is still lent to students with the following ids: "
            for person_pack in res:
                person_id = person_pack[0]
                answer += str(person_id) + ", "
            return False, answer[:-2]

    def search_book(self, book_id, author, title, _wanted_tags):        
        #empty string if none
        res = list() # the result

        if not (book_id or author or title or _wanted_tags):
            return False, "No search parameters given"

        book_id = datatypes.BookID(book_id)
        author = datatypes.Name(author)
        title = datatypes.BookTitle(title)
        wanted_tags = datatypes.Tags(_wanted_tags)

        if book_id and not book_id.isvalid():
            return False, 'The book ID contains bad elements: '+book_id
        if author and not author.isvalid():
            return False, 'The author contains bad elements: '+author
        if title and not title.isvalid():
            return False, 'The title contains bad elements: '+title
        if wanted_tags and not wanted_tags.isvalid():
            return False, 'The tags contain bad elements: '+wanted_tags

        if book_id:
            self.cur.execute("SELECT book_id, author, title, amount, tags FROM books WHERE book_id = ?", (book_id,))
            res.extend(self.cur.fetchall())

        if author:
            self.cur.execute("SELECT book_id, author, title, amount, tags FROM books WHERE author = ? ", (author,))
            res.extend(self.cur.fetchall())

        if title:
            self.cur.execute("SELECT book_id, author, title, amount, tags FROM books WHERE title = ?", (title,))
            res.extend(self.cur.fetchall())

        if len(wanted_tags):
            self.cur.execute("SELECT book_id, author, title, amount, tags FROM books WHERE 1")
            for book_id, author, title, amount, _tags in self.cur.fetchall():
                tags = datatypes.Tags(_tags).comparison_format()
                for el in wanted_tags.comparison_format():
                    if el in tags:
                        res.append((book_id, author, title, amount, _tags))

        result = list()
        for el in res:
            if el not in result:
                result.append(el)
        return True, result

    def show(self):
        self.cur.execute("SELECT book_id, author, title, amount, tags FROM books WHERE 1")
        return self.cur.fetchall()

    def lent_books(self): #shows also to whom
        self.cur.execute("SELECT id, book_id, person_id, amount, return_date FROM librarysystem WHERE 1 ORDER BY return_date")
        res = self.cur.fetchall()
        if not res:
            return True, list()
        result = list()
        for _id, book_id, person_id, amount, return_date in res:
            self.cur.execute("SELECT author, title FROM books WHERE book_id = ?", (book_id,))
            res = self.cur.fetchone()
            if not res:
                author = "##ERROR##"
                title = "##ERROR##"
            else:
                author, title = res
            self.cur.execute("SELECT firstname, surname FROM persons WHERE person_id = ?", (person_id,))
            res = self.cur.fetchone()
            if not res:
                firstname = "##ERROR##"
                surname = "##ERROR##"
            else:
                firstname, surname = res
            result.append((_id, person_id, firstname, surname, book_id, author, title, amount, return_date))
        return True, result

    def books_should_be_returned(self):
        self.cur.execute("SELECT id, book_id, person_id, amount, return_date FROM librarysystem WHERE return_date <= date('now') ORDER BY return_date")
        res = self.cur.fetchall()
        if not res:
            return True, list()
        result = list()
        for _id, book_id, person_id, amount, return_date in res:
            self.cur.execute("SELECT author, title FROM books WHERE book_id = ?", (book_id,))
            res = self.cur.fetchone()
            if not res:
                author = "##ERROR##"
                title = "##ERROR##"
            else:
                author, title = res
            self.cur.execute("SELECT firstname, surname FROM persons WHERE person_id = ?", (person_id,))
            res = self.cur.fetchone()
            if not res:
                firstname = "##ERROR##"
                surname = "##ERROR##"
            else:
                firstname, surname = res
            result.append((_id, person_id, firstname, surname, book_id, author, title, amount))
        return True, result

    def lent_books_to(self, person_id):
        if not Persons(self.con, self.cur)._person_exists(person_id):
            return False, "No such person in the database: " + person_id
        self.cur.execute("SELECT id, book_id, amount, return_date FROM librarysystem WHERE person_id = ?", (person_id,))
        res = self.cur.fetchall()
        if not res:
            return True, list()
        result = list()
        for _id, book_id, amount, return_date in res:
            self.cur.execute("SELECT author, title FROM books WHERE book_id = ?", (book_id,))
            res = self.cur.fetchone()
            if not res:
                author = "##ERROR##"
                title = "##ERROR##"
            else:
                author, title = res
            result.append((_id, book_id, author, title, amount, return_date))
        return True, result

    def show_available_book(self, book_id):
        cur.execute("SELECT amount FROM librarysystem WHERE book_id = ?", (book_id,))
        res = cur.fetchall()
        form_sum = list()
        for el in res:
            form_sum.append(el[0])
        return sum(form_sum)

class LibrarySystem:
    """
    Here a Person lends a book
    """

    def __init__(self, sqldbconnection, sqldbcursor):
        self.con = sqldbconnection
        self.cur = sqldbcursor
        self.cur.execute("""CREATE TABLE IF NOT EXISTS librarysystem
                                                             (id INTEGER PRIMARY KEY ASC AUTOINCREMENT, 
                                                              person_id INTEGER, 
                                                              book_id INTEGER,
                                                              return_date NUMERIC,
                                                              amount INTEGER)""")

    def lend_book(self, person_id, book_id, amount):
        if not person_id:
            return False, 'Please specify a person id'
        if not book_id:
            return False, 'Please specify a book id'
        if not amount:
            return False, 'Please specify an amount'

        person_id = datatypes.PersonID(person_id)
        book_id = datatypes.BookID(book_id)

        if not person_id.isvalid():
            return False, 'The person ID contains bad elements: '+person_id
        if not book_id.isvalid():
            return False, 'The book ID contains bad elements: '+book_id
        if int(amount) == 0 or not str(amount).isdigit():
            return False, "The amount contains nondigit elements: "+str(amount)

        if not Persons(self.con, self.cur)._person_exists(person_id):
            return False, "No such person in the database: " + person_id
        if not Books(self.con, self.cur)._book_exists(book_id):
            return False, "No such book in the database: " + book_id

        self.cur.execute("""INSERT INTO librarysystem (person_id, book_id, return_date, amount)
                                       VALUES (?, ?, date('now', '+21 day'), ?)""", (person_id, book_id, int(amount)))
        return True, None

    def return_book(self, person_id, book_id, amount):
        if not person_id:
            return False, 'Please specify a person id'
        if not book_id:
            return False, 'Please specify a book id'
        if not amount:
            return False, 'Please specify an amount'

        person_id = datatypes.PersonID(person_id)
        book_id = datatypes.BookID(book_id)

        if not person_id.isvalid():
            return False, 'The person ID contains bad elements: '+person_id
        if not book_id.isvalid():
            return False, 'The book ID contains bad elements: '+book_id
        if int(amount) == 0 or not str(amount).isdigit():
            return False, "The amount contains nondigit elements: "+str(amount)

        if not Persons(self.con, self.cur)._person_exists(person_id):
            return False, "No such person in the database: " + person_id
        if not Books(self.con, self.cur)._book_exists(book_id):
            return False, "No such book in the database: " + book_id

        self.cur.execute("SELECT id, amount FROM librarysystem WHERE person_id = ? AND book_id = ? ORDER BY id DESC", (person_id, book_id))

        res = self.cur.fetchall()

        if not res:
            return False, "person '"+str(person_id)+"' has not lent the book '"+str(book_id)+"'"

        amount = int(amount)

        too_much = False
        for _id, lent_amount in res:
            lent_amount = int(lent_amount)
            if too_much:
                amount = too_much
            if lent_amount == amount:
                self.cur.execute("DELETE FROM librarysystem WHERE id = ?", (_id,))
                self.con.commit()
                return True, None
            elif lent_amount > amount:
                self.cur.execute("UPDATE librarysystem SET amount = ? WHERE id = ? ", (int(lent_amount)-int(amount), _id))
                self.con.commit()
                return False, "This is not all what the person took. There are "+str(int(lent_amount)-int(amount))+" more books to bring back"
            else:
                self.cur.execute("DELETE FROM librarysystem WHERE id = ?", (_id,))
                self.con.commit()
                too_much = int(amount) - (lent_amount)
        return False, "The person brought more books than s/he lent. S/he was just supposed to bring back "+str(lent_amount)+" instead of "+str(amount)+"."


def integrity_test():
    con = wrapper_set.SQLiteConnectMultithreadWrapper(':memory:')
    cur = con.cursor()

    print "This test is successful if there is NO ERROR arising"

    persons = Persons(con, cur)
    books = Books(con, cur)
    ls = LibrarySystem(con, cur)

    print "\n\nAbout Persons:"
    #class: persons
    _is, msg = persons.add_person('12', 'Marvin', 'Kastner', 'diploma', 4, '0991283356')
    print "True, None || ", _is, msg
    _is, msg = persons.add_person('13', 'Peter', 'Hans', 'diploma', 4,'0991283354')
    print "True, None || ",_is, msg
    _is, msg = persons.edit_person('12', 'Patrick', 'Kuessner', 'diploma', 4,'0991283356')
    print "True, None || ",_is, msg
    _is, m1, m2 = persons.delete_person('12')
    print "True, None || ",_is, msg
    #provocing mistakes
    print "\nProvoke errors:"
    _is, msg = persons.add_person('13', 'Marvin', 'Kastner', 'diploma', 4,'0991283356') #13 already used
    print "False ||", _is, msg
    _is, msg = persons.edit_person('12', 'Peter', 'Hans', 'diploma', 4,'0991283354')#12 not existent
    print "False ||", _is, msg
    _is, m1, m2 = persons.delete_person('14')#not existent
    print "False ||", _is, msg

    #class: books
    print "\n\n","About Books"
    _is, lord_of_the_ring_id = books.add_book('JRR Tolkien', 'Lord of the Rings', 10, 'magic, fantasy')
    print "True ||", _is
    _is, book_id = books.add_book('Rawlings', 'Harry Potter', 3, 'magic, witch')
    print "True ||", _is, book_id
    _is, msg = books.edit_book(book_id, 'Rawlings', 'Harry Potter II', 10, 'magic, witch')
    print "True ||", _is, msg
    _is, msg = books.delete_book(book_id)
    print "True ||", _is, msg
    _is, harry_potter_id = books.add_book('Rawlings', 'Harry Potter', 3, 'magic, witch')
    print "True ||", _is, book_id

    print "\n\nProvocing mistakes:"
    #provocing mistakes
    _is, book_id = books.add_book('JRR Tolkien', 'Lord of the Rings', 45, 'magic, fantasy')#already there
    print "False ||", _is, msg
    _is, msg = books.edit_book(book_id, 'Rawlings', 'Harry Potter II', 44, 'magic, witch')#not existent
    print "False ||", _is, msg
    _is, msg = books.delete_book(10000)#not existent
    print "False ||", _is, msg

    #class: library system
    print "\n\nlibrary system"
    _is, msg = ls.lend_book('13', lord_of_the_ring_id, 1)
    print "True ||", _is, msg
    _is, book_id = books.add_book('Rawlings', 'Harry Potter', 2, 'magic, witch')
    _is, msg = persons.add_person('14', 'Till', 'Bunsen', 'diploma', 4, '0991283356')
    print "True ||", _is, book_id
    _is, msg = ls.lend_book('14', harry_potter_id, 1)
    print "True ||", _is, book_id
    _is, msg = ls.return_book('13', 'Lord of the Rings', 1)
    print "True ||", _is, msg
    #provocing mistakes
    print "\n\nprovoking errors:"
    _is, msg = ls.return_book('13', lord_of_the_ring_id, 1)
    print "False ||", _is, msg
    _is, msg = ls.lend_book('55', harry_potter_id, 1)
    print "False ||", _is, msg
    _is, msg = ls.lend_book('13', 7777, 1)
    print "False ||", _is, msg
    _is, msg = ls.return_book('55', harry_potter_id, 1)
    print "False ||", _is, msg
    _is, msg = ls.return_book('13', 889, 1)
    print "False ||", _is, msg
        
    #search functions:
    _is, msg = persons.add_person('8', 'Marvin', 'Kastner', 'diploma', 4, '0991283356')

    print persons.search_person('13' , '', '', '', '', '')
    print persons.search_person('333', '', '', '', '', '')
    print persons.search_person('' , 'Till', '', '', '', '')
    print persons.search_person('' , '', 'Bunsen', '','', '')
    print persons.search_person('' , '', '', '', '', '0991283356')
    print persons.search_person('13' , 'Marvin', '', '', '', '')
    print persons.search_person('' , 'Marvin', 'Kastner','', '', '')
    print persons.search_person('' , '', 'Kastner', '', '', '0991283356')

    print books.search_book(book_id, '', '', '')
    print books.search_book('', 'JRR Tolkien', '', '')
    print books.search_book('', '', 'Lord of the Rings', '')
    print books.search_book('', '', '', 'magic,')
    print books.search_book('', 'JRR Tolkien', '', 'magic,')
    print books.search_book('', '', 'Harry Potter', 'magic,')

    cur.execute("INSERT INTO librarysystem (person_id, book_id, amount, return_date) VALUES ('13','3', 1, date('now','-24 day'))")
    cur.execute("SELECT * FROM librarysystem")
    print cur.fetchall()
    print "too long: ", books.books_should_be_returned()

if __name__ == '__main__':
    integrity_test()
