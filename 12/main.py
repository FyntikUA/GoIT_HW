from collections import UserDict
import datetime

import pickle

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
        birthday_info = f"Birthday: {self.birthday.value}" if self.birthday else ""
        days_to_birthday_info = f"Days to birthday: {self.days_to_birthday()}" if self.birthday else "Days to birthday: N/A"

        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, {birthday_info}, {days_to_birthday_info}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, search_str):
        found_records = []
        for record in self.data.values():
            if search_str.lower() in record.name.value.lower():
                found_records.append(record)
            for phone in record.phones:
                if search_str in phone.value:
                    found_records.append(record)
        return found_records

    def delete(self, name):
        if name not in self.data:
            return None
        del self.data[name]

    def iterator(self, n=10):
        for i in range(0, len(self.data), n):
            names = list(self.data.keys())
            records = [str(self.data[name]) for name in names[i:i + n]]
            if records:
                yield '\n'.join(records)

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print('File not found')



# Приклад створення контакту та додавання його до адресної книги
john_record = Record("John", "1990-01-15")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book = AddressBook()
book.add_record(john_record)

# Збереження адресної книги у файл
book.save_to_file('address_book.pkl')

# Відновлення адресної книги з файлу (можна викликати цей метод на початку програми)
book.load_from_file('address_book.pkl')

# Пошук контакту за ім'ям чи номером телефону
search_results_name = book.find("John")
print("Search results by name:")
for result in search_results_name:
    print(result)

search_results_phone = book.find("555")
print("\nSearch results by phone:")
for result in search_results_phone:
    print(result)




