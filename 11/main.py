from collections import UserDict
import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value:
            raise ValueError("Name must not be empty")


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits")


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value:
            return
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Wrong birthday format")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone = Phone(new_phone)
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = phone
                return
        raise ValueError(f"Phone number {old_phone} does not exist")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if not self.birthday or not self.birthday.value:
            return None

        today = datetime.datetime.today()
        birthday = datetime.datetime.strptime(self.birthday.value, "%Y-%m-%d")

        birthday = birthday.replace(year=today.year)

        if today > birthday:
            next_birthday = birthday.replace(year=today.year + 1)
        else:
            next_birthday = birthday

        return (next_birthday - today).days

    def __str__(self):
        birthday_info = f"Birthday: {self.birthday.value}" if self.birthday else ...
        days_to_birthday_info = f"Days to birthday: {self.days_to_birthday()}" if self.birthday else "Days to birthday: N/A"

        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, {birthday_info}, {days_to_birthday_info}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):           
        self.data[record.name.value] = record        # додавання до адресної книги даних з класу class Record з ключем name.value

    def find(self, name):
        if name not in self.data:
            return None
        return self.data[name]

    def delete(self, name):
        if name not in self.data:
            return None
        del self.data[name]

    def iterator(self, n=10):               # реалізує метод iterator, який повертає генератор за записами AddressBook і за одну ітерацію повертає уявлення для N записів.
        for i in range(0, len(self.data), n):
            names = list(self.data.keys())  # Перетворення dict_keys на список
            records = [str(self.data[name]) for name in names[i:i + n]]
            if records:
                yield '\n'.join(records)   
                


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення запису для Jane
jane_record = Record("Jane", "1999-01-01")
jane_record.add_phone("9876543210")

# Додавання запису Jane до адресної книги
book.add_record(jane_record)

# Виведення всіх записів у адресній книзі
for record in book.iterator():
    print(record)

# Виведення перших 10 записів у адресній книзі
for record in book.iterator(10):
    print(record)
    
