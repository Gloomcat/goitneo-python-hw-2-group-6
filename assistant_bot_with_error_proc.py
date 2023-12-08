SUPPORTED_COMMANDS = """
    hello  - supported commands list
    add    - save contact with username and phone (required: <username> <phone>)
    change - change contact phone by username provided (required: <username> <phone>)
    phone  - show contact by username provided (required: <username>)
    all    - show all saved contacts
    exit   - exit from assistant
    close  - same as `exit`
"""


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            return "Give me name (and phone) please."
        except KeyError:
            return "Contact doesn't exist."
        except:
            return "Oops! Something wrong happened."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def show_all(contacts):
    if not contacts:
        return "Contacts book is empty.", False
    return "Saved contacts:", True


@input_error
def add_contact(args, contacts):
    username, phone = args
    contacts[username] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    username, phone = args
    if username in contacts:
        contacts[username] = phone
        return "Contact updated."
    else:
        return "Contact doesn't exist."


@input_error
def show_contact(args, contacts):
    username = args[0]
    return contacts[username]


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    print(SUPPORTED_COMMANDS)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command == "hello":
            print("How can I help you?")
            print(SUPPORTED_COMMANDS)
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_contact(args, contacts))
        elif command == "all":
            string, ok = show_all(contacts)
            print(string)
            if ok:
                for username, phone in contacts.items():
                    print(f"{username}: {phone}")
        elif command in ["close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
