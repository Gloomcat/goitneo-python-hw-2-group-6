from collections import UserDict


class Field:
    def __init__(self, value, validate=None, validation_fail=""):
        self.validate = validate
        self.validation_fail = validation_fail
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.validate and not self.validate(value):
            raise ValueError(self.validation_fail)
        self.__value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, value):
        return self.value == value

    def __hash__(self):
        return self.value.__hash__()


class Name(Field):
    def __init__(self, value):
        validation_fail_message = (
            "Incorrect name provided. Name must contain only letters."
        )
        super().__init__(value, lambda v: v.isalpha(), validation_fail_message)


class Phone(Field):
    def __init__(self, value):
        validation_fail_message = (
            "Incorrect phone provided. Phone must consist of 10 digits."
        )
        super().__init__(
            value, lambda v: v.isnumeric() and len(v) == 10, validation_fail_message
        )


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = set()

    def add_phone(self, phone):
        self.phones.add(Phone(phone))

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def find_phone(self, phone):
        if phone in self.phones:
            return f"{self.name}: {phone}"
        return "Phone not found!"

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            self.phones.remove(old_phone)
            self.phones.add(Phone(new_phone))

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name in self.data:
            return
        self.data[record.name] = record

    def delete(self, name):
        self.data.pop(Name(name))

    def find(self, name):
        return self.data[Name(name)]


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Try create `John` record with invalid name
    try:
        john_record = Record("John123")
    except ValueError as e:
        print(e)

    # Create `John` record
    john_record = Record("John")

    # Try add invalid phone to `John` record
    try:
        john_record.add_phone("1234567890_")
    except ValueError as e:
        print(e)

    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Add record `John`
    book.add_record(john_record)

    # Create and add new record: `Jane`
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Print all records from the book
    for name, record in book.data.items():
        print(record)

    # Find and edit phone in `John` record
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    john.remove_phone("5555555555")

    # Output: Contact name: John, phones: 1112223333; 5555555555
    print(john)

    # Find exact phone in `John` record. Output: 5555555555
    print(john.find_phone("1112223333"))

    # Видалення запису Jane
    book.delete("Jane")
