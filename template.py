#!/usr/bin/python
#template collection

_file = open("basic_template.html")
basic_template = _file.read()

index = "<br><p>Welcome to this beautiful library at this nice day.</p><p>Today it is the <i><?= date ?></i>. On the left you can see the interactive menu with all the functions you need. </p><p>If you need any assistance either contact the library master or don't hesitate to ask the programmer (murph@gmx.net) for assistance."

successful = "Your action has been done successfully!"

error = "Sorry for the inconvenience, but an error occured: <br><p><?= msg ?></p>"
###back from javascript should be included!


###########################################
###########################################
### Persons


call_add_person = """<p><table><tr><form action='/do_add_person'></tr>
<tr><td>Student ID</td><td><input name='person_id' type='text'></input></td></tr>
<tr><td>First Name</td><td><input name='firstname' type='text'></input></td></tr>
<tr><td>Surname</td><td><input name='surname' type='text'></input></td></tr>
<tr><td>Class</td><td><input name='_class' type='text'></input></td></tr>
<tr><td>Semester</td><td><input name='semester' type='text'></input></td></tr>
<tr><td>Cellphone Number</td><td><input name='cellphone' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p>"""

call_edit_person = """<p>Please specify which student should be edited<br><table><tr><form action='/do_edit_person'></tr>
<tr><td>Student ID</td><td><input name='person_id' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p>
<i>If the student's ID is supposed to be changed delete the student and add him/her again.</i>"""

do_edit_person = """<table><tr><form action='/do_edit_person_2'></tr>
<tr><td>Student ID</td><td><?= person_id?><input name='person_id' type='hidden' value='<?= person_id ?>'></input></td></tr>
<tr><td>First Name</td><td><input name='firstname' type='text' value='<?= firstname ?>'></input></td></tr>
<tr><td>Surname</td><td><input name='surname' type='text' value='<?= surname ?>'></input></td></tr>
<tr><td>Cellphone Number</td><td><input name='cellphone' type='text' value='<?= cellphone ?>'></input></td></tr>
<tr><td>Class</td><td><input name='_class' type='text' value='<?= _class ?>'></input></td></tr>
<tr><td>Semester</td><td><input name='semester' type='text' value='<?= semester ?>'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p><br>
The student ID cannot be changed. If that is necissary delete the student and add a new one."""
 
call_delete_person = """<p>Please specify which student should be <b>deleted</b><br><table><tr><form action='/do_delete_person'></tr>
<tr><td>Student ID</td><td><input name='person_id' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p>"""

call_show_persons_none = """<p>In the Library System following students are registered:<br>
  <p>No students are in the database</p>
"""

call_show_persons = """<p>In the Library System following students are registered:<br><br></p>
  <table border=1>
  <tr><td><b>Student ID</b></td><td><b>First Name</b></td><td><b>Surname</b></td><td><b>Class</b></td><td><b>Semester</b></td><td><b>Cellphone</b></td></tr>
  <? for student_set in res: ?>
    <tr>
      <? for el in student_set: ?>
        <td WIDTH=27% HEIGHT=19><?= el ?></td>
        <? end ?>
    </tr>
  <? end ?>
</table> 
"""

call_search_person = """<p>Please enter some keywords<table><tr><form action='/do_search_person'></tr>
<tr><td>Student ID</td><td><input name='person_id' type='text'></input></td></tr>
<tr><td>First Name</td><td><input name='firstname' type='text' </input></td></tr>
<tr><td>Surname</td><td><input name='surname' type='text'></input></td></tr>
<tr><td>Class</td><td><input name='_class' type='text'></input></td></tr>
<tr><td>Semester</td><td><input name='semester' type='text'></input></td></tr>
<tr><td>Cellphone Number</td><td><input name='cellphone' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p>
"""

do_search_person = """<p>The result of the search was as follows:<br><br></p>
  <table border=1>
  <tr><td><b>Student ID</b></td><td><b>First Name</b></td><td><b>Surname</b></td><td><b>Class</b></td><td><b>Semester</b></td><td><b>Cellphone</b></td></tr>
  <? for student_set in res: ?>
    <tr><? for el in student_set: ?>
      <td WIDTH=27% HEIGHT=19><?= el ?></td>
    <? end ?></tr>
  <? end ?>
<? end ?></table> 
"""

do_search_person_none = """<p>The result of the search was as follows:<br>
  <p>No students could be found</p>
"""

####################################################
####################################################
###   BOOKS   ######################################

call_add_book = """<p><table><tr><form action='/do_add_book'></tr>
<tr><td>Author</td><td><input name='author' type='text'></input></td></tr>
<tr><td>Title</td><td><input name='title' type='text'></input></td></tr>
<tr><td>Amount</td><td><input name='amount' type='text'></input></td></tr>
<tr><td>Tags</td><td><input name='tags' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p><br>
Please seperate the tags by colons (',')"""

call_edit_book = """<p>Please specify which book should be edited<br><table><tr><form action='/do_edit_book'></tr>
<tr><td>Book ID</td><td><input name='book_id' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p>
"""

do_edit_book = """<p><table><tr><form action='/do_edit_book_2'></tr>
<tr><td>Book ID</td><td><?= book_id?><input name='book_id' type='hidden' value='<?= book_id ?>'></td></tr>
<tr><td>Author</td><td><input name='author' type='text' value='<?= author ?>'></input></td></tr>
<tr><td>Title</td><td><input name='title' type='text' value='<?= title?>'></input></td></tr>
<tr><td>Amount</td><td><input name='amount' type='text' value='<?= amount ?>'></input></td></tr>
<tr><td>Tags</td><td><input name='tags' type='text' value='<?= tags ?>'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p><br>
Please seperate the tags by colons (',')<br>
The Book ID cannot be edited. Please delete the book and add it again if a new ID is nessicary."""

call_delete_book = """<p>Please specify which book should be <b>deleted</b><br><table><tr><form action='/do_delete_book'></tr>
<tr><td>Book ID</td><td><input name='book_id' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p>"""

call_show_books_none = """<p>In the Library System following books are registered:<br>
  <p>No books are in the database</p>
"""

call_show_books = """<p>In the Library System following books are registered:<br><br></p>
  <table border=1>
<tr><td><b>Book ID</b></td>
<td><b>Author</b></td>
<td><b>Title</b></td>
<td><b>Amount</b></td>
<td><b>Tags</b></td></tr>
  <? for student_set in res: ?>
    <tr><? for el in student_set: ?>
      <td WIDTH=24% HEIGHT=19><? if el: ?><?= el ?><? end ?><? if not el: ?><i>None</i><? end ?></td>
    <? end ?></tr>
  <? end ?>
<? end ?></table> 
"""

call_search_book = """<p>Please enter some keywords<table><tr><form action='/do_search_book'></tr>
<tr><td>Book ID</td><td><input name='book_id' type='text'></input></td></tr>
<tr><td>Author</td><td><input name='author' type='text'></input></td></tr>
<tr><td>Title</td><td><input name='title' type='text'></input></td></tr>
<tr><td>Tags</td><td><input name='tags' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p><br>
Please seperate the tags by colons (',')
"""

do_search_book = """<p>The result of the search was as follows:<br><br></p>
  <table border=1>
<tr><td><b>Book ID</b></td>
<td><b>Author</b></td>
<td><b>Title</b></td>
<td><b>Amount</b></td>
<td><b>Tags</b></td></tr>
  <? for row in res: ?>
    <tr><? for el in row: ?>
      <td WIDTH=27% HEIGHT=19><?= el ?></td>
    <? end ?></tr>
  <? end ?>
<? end ?></table> 
"""

do_search_book_none = """<p>The result of the search was as follows:<br>
  <p>No books could be found</p>
"""

############################################
############################################
###Library 

call_lend_book = """Please specify which book will be lent to whom:<br><br>
<table><form action='/do_lend_book'>
<tr><td>Student ID</td><td><input name='person_id' type='text'></input></td></tr>
<tr><td>Book ID</td><td><input name='book_id' type='text'></input></td></tr>
<tr><td>Amount</td><td><input name='amount' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p>
"""

call_return_book = """Please specify who wants to return which book<br><br>
<table><form action='/do_return_book'>
<tr><td>Student ID</td><td><input name='person_id' type='text'></input></td></tr>
<tr><td>Book ID</td><td><input name='book_id' type='text'></input></td></tr>
<tr><td>Amount</td><td><input name='amount' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p>
"""

call_show_lent_books = """<p>The result of the search was as follows:<br><br></p>
  <table border=1>
  <tr><td><b>Lend ID</b></td>    
  <td><b>Student ID</b></td>
  <td><b>First name</b></td>
  <td><b>Surname</b></td>
  <td><b>Book ID</b></td>
  <td><b>Author</b></td>
  <td><b>Title</b></td>
  <td><b>Amount</b></td>
  <td><b>Return Date</b></td></tr>
  <? for student_set in res: ?>
    <tr><? for el in student_set: ?>
      <td WIDTH=16% HEIGHT=19><?= el ?></td>
    <? end ?></tr>
  <? end ?>
<? end ?></table> 
"""
call_show_lent_books_none = """<p>The result of the search was as follows:<br>
  <p>No lent books could be found</p>
"""

call_lent_books_to = """<p>Please specify for which student you want to have the list of the books to return<br><table><tr><form action='/do_lent_books_to'></tr>
<tr><td>Student ID</td><td><input name='person_id' type='text'></input></td></tr>
<tr><td></td></tr>
<tr><td><input lable='submit' type='submit'></td></td></form></table></p>
"""

call_show_lent_books_to = """<p>The result for student '<?= person_id ?>' was as follows:<br><br></p>
  <table border=1>
<tr><td><b>Lend ID</b></td>
<td><b>Book ID</b></td>
<td><b>Author</b></td>
<td><b>Title</b></td>
<td><b>Amount</b></td>
<td><b>Return Date</b></td></tr>
  <? for student_set in res: ?>
    <tr><? for el in student_set: ?>
      <td WIDTH=16% HEIGHT=19><?= el ?></td>
    <? end ?></tr>
  <? end ?>
<? end ?></table> 
"""

call_show_lent_books_to_when_deleting = """<p>The student '<?= person_id ?>' could not be deleted because s/he still possesses books of the library:<br><br></p>
  <table border=1>
<tr><td><b>Lend ID</b></td><td><b>Book ID</b></td><td><b>Author</b></td><td><b>Title</b></td><td><b>Amount</b></td><td><b>Return Date</b></td></tr>
  <? for student_set in res: ?>
    <tr><? for el in student_set: ?>
      <td WIDTH=16% HEIGHT=19><?= el ?></td>
    <? end ?></tr>
  <? end ?>
<? end ?></table> 
"""

call_show_lent_books_to_none = """<p>The result of the search was as follows:<br>
  <p>No lent books could be found</p>
"""

call_lent_books_none = """<p>The result of the search was as follows:<br>
  <p>No lent books could be found</p>
"""

call_show_books_over_limit = """
"<p>The result of the search was as follows:<br><br></p>
  <table border=1>
  <tr><td><b>Lend ID</b></td>    
  <td><b>Student ID</b></td>
  <td><b>First name</b></td>
  <td><b>Surname</b></td>
  <td><b>Book ID</b></td>
  <td><b>Author</b></td>
  <td><b>Title</b></td></tr>
  <? for student_set in res: ?>
    <tr><? for el in student_set: ?>
      <td WIDTH=16% HEIGHT=19><?= el ?></td>
    <? end ?></tr>
  <? end ?>
<? end ?></table> 
"""

call_show_books_over_limit_none = """<p>The result of the search was as follows:<br>
  <p>No lent books over limit could be found</p>
"""

call_backup = """<p>Welcome to the backup function</p><br>
<table>
  <tr>
     <td>
       For creating a backup, please press:
     </td>
     <td>
       <a href='/create_backup'>HERE</a></td>
  </tr>
  <tr>
     <td>
       For inserting an old backup:
     </td>
     <td>
       <form action='/upload_backup' method="post" enctype="multipart/form-data"><input type="file" name="myFile" /><br />
            <input type="submit" value="INSERT BACKUP" />
     </td>
  </tr>
</table>
"""
