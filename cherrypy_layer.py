#!/usr/bin/python
#library layer

import os.path
import time

import cherrypy
from cherrypy.lib import static
import stpy

import wrapper_set
import lib_librarydb
import template

class LibrarySoftware:
    """
    This will be the website
    """
    def __init__(self, conf):
        self.basic_template = stpy.Template(template.basic_template)
        dbcon = wrapper_set.SQLiteConnectMultithreadWrapper(conf['dbpath'])
        dbcur = dbcon.cursor()
        self.persons = lib_librarydb.Persons(dbcon, dbcur)
        self.books = lib_librarydb.Books(dbcon, dbcur)
        self.libsys = lib_librarydb.LibrarySystem(dbcon, dbcur)

    def index(self):
        tpl = self.basic_template.render({'TEXTFIELD':template.index})
        page = stpy.Template(tpl).render({'date':time.strftime("%d-%m-%Y")})
        return page
    index.exposed = True

  #Person

    def call_add_person(self):
        page = self.basic_template.render({'TEXTFIELD':template.call_add_person})
        return page
    call_add_person.exposed = True

    def do_add_person(self, person_id, firstname, surname, _class, semester, cellphone):
        _is, msg = self.persons.add_person(person_id, firstname, surname, _class, semester, cellphone)
        if _is:
            page = self.basic_template.render({'TEXTFIELD':template.successful})
            return page
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
            return page     
    do_add_person.exposed = True

    def call_edit_person(self):
        return self.basic_template.render({'TEXTFIELD':template.call_edit_person})
    call_edit_person.exposed = True

    def do_edit_person(self, person_id):
        _is, res = self.persons.search_person(person_id, '', '', '', '', '')
        if not _is:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':res})
        elif not res:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':'No such student'})
        else:
            person_id, firstname, surname, _class, semester, cellphone = res[0]
            tpl = self.basic_template.render({'TEXTFIELD':template.do_edit_person})
            page = stpy.Template(tpl).render({'person_id':person_id,
                                          'firstname':firstname,
                                          'surname':surname,
                                          'cellphone':cellphone,
                                          '_class':_class,
                                          'semester':semester})
        return page
    do_edit_person.exposed = True

    def do_edit_person_2(self, person_id, firstname, surname, _class, semester, cellphone):
        _is, msg = self.persons.edit_person(person_id, firstname, surname, _class, semester, cellphone)
        if _is:
            page = self.basic_template.render({'TEXTFIELD':template.successful})
            return page
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
            return page     
    do_edit_person_2.exposed = True

    def call_delete_person(self):
        return self.basic_template.render({'TEXTFIELD':template.call_delete_person})
    call_delete_person.exposed = True

    def do_delete_person(self, person_id):
        _is, msg, books = self.persons.delete_person(person_id)
        if _is:
            page = self.basic_template.render({'TEXTFIELD':template.successful})
        elif books and not _is:
            tpl = self.basic_template.render({'TEXTFIELD':template.call_show_lent_books_to_when_deleting})
            page = stpy.Template(tpl).render({'res':books, 'person_id':person_id})
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
        return page
    do_delete_person.exposed = True

    def call_show_persons(self):
        res = self.persons.show()
        if not res:
            page = self.basic_template.render({'TEXTFIELD':template.call_show_persons_none})
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.call_show_persons})
            page = stpy.Template(tpl).render({'res':res})
        return page 
    call_show_persons.exposed = True       

    def call_search_person(self):
        page = self.basic_template.render({'TEXTFIELD':template.call_search_person})
        return page
    call_search_person.exposed = True

    def do_search_person(self, person_id, firstname, surname, _class, semester, cellphone):
        _is, res = self.persons.search_person(person_id, firstname, surname, _class, semester, cellphone)
        if not _is:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':res})
        elif not res:
            page = self.basic_template.render({'TEXTFIELD':template.do_search_person_none})
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.do_search_person})
            page = stpy.Template(tpl).render({'res':res})
        return page 
    do_search_person.exposed = True

  #books
    def call_add_book(self):
        page = self.basic_template.render({'TEXTFIELD':template.call_add_book})
        return page
    call_add_book.exposed = True

    def do_add_book(self, author, title, amount, tags):
        _is, msg = self.books.add_book(author, title, amount, tags)
        if _is:
            page = self.basic_template.render({'TEXTFIELD':template.successful})
            return page
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
            return page     
    do_add_book.exposed = True

    def call_edit_book(self):
        return self.basic_template.render({'TEXTFIELD':template.call_edit_book})
    call_edit_book.exposed = True

    def do_edit_book(self, book_id):
        _is, res = self.books.search_book(book_id, '', '', '')
        if not _is:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':res})
        elif not res:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':'No such book'})
        else:
            book_id, author, title, amount, tags = res[0]
            tpl = self.basic_template.render({'TEXTFIELD':template.do_edit_book})
            page = stpy.Template(tpl).render({'book_id':book_id,
                                          'author':author,
                                          'title':title,
                                          'amount':amount,
                                          'tags':tags})
        return page
    do_edit_book.exposed = True

    def do_edit_book_2(self, book_id, author, title, amount, tags):
        _is, msg = self.books.edit_book(book_id, author, title, amount, tags)
        if _is:
            page = self.basic_template.render({'TEXTFIELD':template.successful})
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg}) 
        return page   
    do_edit_book_2.exposed = True

    def call_delete_book(self):
        return self.basic_template.render({'TEXTFIELD':template.call_delete_book})
    call_delete_book.exposed = True

    def do_delete_book(self, book_id):
        _is, msg = self.books.delete_book(book_id)
        if _is:
            page = self.basic_template.render({'TEXTFIELD':template.successful})
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
        return page
    do_delete_book.exposed = True

    def call_show_books(self):
        res = self.books.show()
        if not res:
            page = self.basic_template.render({'TEXTFIELD':template.call_show_books_none})
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.call_show_books})
            page = stpy.Template(tpl).render({'res':res})
        return page 
    call_show_books.exposed = True       

    def call_search_book(self):
        return self.basic_template.render({'TEXTFIELD':template.call_search_book})
    call_search_book.exposed = True

    def do_search_book(self, book_id, author, title, tags):
        _is, msg = self.books.search_book(book_id, author, title, tags)
        res = msg
        if not _is:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
        elif not res:
            page = self.basic_template.render({'TEXTFIELD':template.do_search_book_none})
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.do_search_book})
            page = stpy.Template(tpl).render({'res':res})
        return page 
    do_search_book.exposed = True

  ##library

    def call_lend_book(self):
        page = self.basic_template.render({'TEXTFIELD':template.call_lend_book})
        return page
    call_lend_book.exposed = True

    def do_lend_book(self, person_id, book_id, amount):
        _is, msg = self.libsys.lend_book(person_id, book_id, amount)
        if _is:
            page = self.basic_template.render({'TEXTFIELD':template.successful})
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
        return page
    do_lend_book.exposed = True

    def call_return_book(self):
        return self.basic_template.render({'TEXTFIELD':template.call_return_book})
    call_return_book.exposed = True

    def do_return_book(self, person_id, book_id, amount):
        _is, msg = self.libsys.return_book(person_id, book_id, amount)
        if _is:
            page = self.basic_template.render({'TEXTFIELD':template.successful})
        else:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
        return page
    do_return_book.exposed = True

    def call_show_lent_books(self):
        _is, msg = self.books.lent_books()
        if not _is:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
        elif not msg:
            page = self.basic_template.render({'TEXTFIELD':template.call_lent_books_none})
        else: 
            tpl = self.basic_template.render({'TEXTFIELD':template.call_show_lent_books})
            page = stpy.Template(tpl).render({'res':msg})
        return page
    call_show_lent_books.exposed = True

    def call_books_over_limit(self): 
        _is, msg = self.books.books_should_be_returned()
        if not _is:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
        elif msg:
            tpl = self.basic_template.render({'TEXTFIELD':template.call_show_books_over_limit})
            page = stpy.Template(tpl).render({'res':msg})
        else:
            page = self.basic_template.render({'TEXTFIELD':template.call_show_books_over_limit_none})
        return page
    call_books_over_limit.exposed = True

    def call_lent_books_to(self):
        return self.basic_template.render({'TEXTFIELD':template.call_lent_books_to})
    call_lent_books_to.exposed = True

    def do_lent_books_to(self, person_id):
        _is, msg = self.books.lent_books_to(person_id)
        if not _is:
            tpl = self.basic_template.render({'TEXTFIELD':template.error})
            page = stpy.Template(tpl).render({'msg':msg})
        elif msg:
            tpl = self.basic_template.render({'TEXTFIELD':template.call_show_lent_books_to})
            page = stpy.Template(tpl).render({'res':msg, 'person_id':person_id})
        else:
            page = self.basic_template.render({'TEXTFIELD':template.call_show_lent_books_to_none})
        return page
    do_lent_books_to.exposed = True

    def call_backup(self):
        return self.basic_template.render({'TEXTFIELD':template.call_backup})
    call_backup.exposed = True

    def create_backup(self):
        localDir = os.path.dirname(__file__)
        absDir = os.path.join(os.getcwd(), localDir)
        path = os.path.join(absDir, "library.sdb")
        ts = time.gmtime()
        timestamp = str(ts.tm_year)+"-"+str(ts.tm_mon)+"-"+str(ts.tm_mday)+"-"+str(ts.tm_hour)
        timestamp += "-"+str(ts.tm_min)+"-"+str(ts.tm_sec)
        filename = "library_"+timestamp+".sdb"
        return static.serve_file(path, "application/x-download", "attachment", filename)
    create_backup.exposed = True

    def upload_backup(self, myFile):
        localDir = os.path.dirname(__file__)
        absDir = os.path.join(os.getcwd(), localDir)
        ts = time.gmtime()
        path = os.path.join(absDir, "library.sdb")
        new_database = open(path, "w")
        while True:
            data = myFile.file.read(8192)
            if not data:
                break
            new_database.write(data)
        new_database.close()
        return self.basic_template.render({'TEXTFIELD':template.successful})
    upload_backup.exposed = True


conf={'dbpath':'library.sdb'}

def run():
    cherrypy.quickstart(LibrarySoftware(conf), config=os.path.join('./tutorial.conf'))

if __name__ == '__main__':
    print "Please start this programm by using start.py"
    print "Anyhow, if you are very sure about what you are doing, continue with <enter>"
    i = raw_input()
    run()
