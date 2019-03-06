import datetime

Date = datetime.date

class Patient(object):
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.name == other.name \
            and self.gender == other.gender \
            and self.birthday == other.birthday
    
    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.birthday < other.birthday
    
    def __init__(self, name, gender, birthday):
        super(Patient, self).__init__()
        self.name = name
        self.gender = gender
        self.birthday = birthday
   
    def __repr__(self):
        return '%s.%s(%r, %r, %r)' % (self.__class__.__module__, \
                                      self.__class__.__name__, \
                                      self.name, self.gender, self.birthday)
    
    @property
    def age(self):
        pass
