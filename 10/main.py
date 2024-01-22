from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value          # ініціалізуємо введене значення 

    def __str__(self):          # повертає текстове поле
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)         # ініціалізуємо ім"я викликаючи батьківський метод __init__ класу Field
        if not value:                                   # якщо не ініціалізоване (не введене, not True) ім"я, викликаємо помилку ValueError
            raise ValueError("Name must not be empty")          


class Phone(Field):
    def __init__(self, value):              
        super().__init__(value)             # ініціалізуємо ім"я викликаючи батьківський метод __init__ класу Field
        if not value.isdigit() or len(value) != 10:             # якщо введене значення не дорівнює 10 символам
            raise ValueError("Phone number must be 10 digits")      # викликаємо помилку ValueError


class Record:
    def __init__(self, name):
        self.name = Name(name)              # створюємо зімнну self.name з значення value з класу class Name
        self.phones = []                    # створюємо список

    def add_phone(self, phone):
        phone = Phone(phone)                # створюємо зімнну phone з значення value з класу class Phone
        self.phones.append(phone)           # додаємо phone до списку self.phones

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]  # видалення phone з перевіркою на наявність

    def edit_phone(self, old_phone, new_phone):         # змінюєм н телефону зі списку на введений новий
        phone = Phone(new_phone)                     
        for i, p in enumerate(self.phones):     # чи існує номер телефону old_phone у списку телефонів. Якщо не існує, то метод викидає ValueError.
            if p.value == old_phone:
                if p is not None:                   
                    self.phones[i] = phone
                    return
        raise ValueError(f"Phone number {old_phone} does not exist")

    def find_phone(self, phone):                # пошук телефону у списку 
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):                      # вивід строки 
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()          # ініціалізація методів та змінних від батьківського класу

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