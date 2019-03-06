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
        today = Date.today()
        birthday = self.birthday
        if (birthday is None) or (today < birthday):
            return None
        leap = lambda y: 1 if y % 4 == 0 and (y % 400 == 0 or y % 100 != 0) \
            else 0
        count = lambda m, y: 28 + leap(y) if m == 2 \
            else 30 if (m in [4, 6, 9, 11]) else 31
        years = today.year - birthday.year
        months = today.month - birthday.month
        days = today.day - birthday.day
        if days < 0:
            months -= 1
            days += count(birthday.month, birthday.year)
        if months < 0:
            years -= 1
            months += 12
        return (years, months, days)
    
