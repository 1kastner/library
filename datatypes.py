#!/usr/bin/python

class Cellphone(str):
    def __init__(self, number):
        self.value = str(number)
    def isvalid(self):
        #a number can contain '+', ' ', '-', '/', '(', ')'
        _num = self.value.replace('+','')
        _num = _num.replace(' ','')
        _num = _num.replace('-','')
        _num = _num.replace('(','')
        _num = _num.replace(')','')
        #_num = _num.replace('/','') #this to add for german style telephone numbers
        return _num.isdigit()
    def database_format(self):
        #remove beauty:
        _num = self.value.replace(' ','')
        _num = _num.replace('-','')
        #remove malawian country code
        _num = _num.replace('+265','0')
        _num = _num.replace('(0)','')
        return _num
    def __str__(self):
         return self.value

class PersonID(str):
    def __init__(self, _id):
        self.value = str(_id)
    def isvalid(self):
        #an id can contain ***anything***
        return True
    def __str__(self):
         return self.value

class Name(str):
    def __init__(self, name):
        self.value = str(name)
    def isvalid(self):
        spacelessname = str()
        for el in [x for x in self.value.split(" ") if x]:
            spacelessname += el
        return spacelessname.isalpha()
 
    def __str__(self):
         return self.value

class _Class(str):
    def __init__(self, name):
        self.value = str(name)
    def isvalid(self):
        return True
    def __str__(self):
         return self.value

class Semester(str):
    def __init__(self, name):
        self.value = str(name)
    def isvalid(self):
        return True
    def __str__(self):
         return self.value

class Tags:
    def __init__(self, tagstring):
        self.value = tagstring.split(",")
    def isvalid(self):
        return True
    def __len__(self):
        return len(self.value)
    def comparison_format(self):
        return [tag.lower() for tag in self.value]

class BookTitle(str):
    def __init__(self, name):
        self.value = str(name)
    def isvalid(self):
        return True
    def __str__(self):
         return self.value

class BookID(str):
    def __init__(self, number):
        try:
            self.value = int(number)
            self._isvalid = True
        except ValueError:
            self._isvalid = False
    def isvalid(self):
        return self._isvalid
    def __str__(self):
         return str(self.value)
