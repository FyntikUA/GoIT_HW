def input_error(func):
    def wrapper(user_input:str):
            try:
                string = user_input.split(' ')
                func(user_input)
            except KeyError:
                print(f'There are no {string[1]} in phonebook.')
            except ValueError:
                print(f'{string[2]} - is a wrong number. Only digits are available.')
            except IndexError:
                print('Looks like you forgot to write something.')
    return wrapper


@input_error
def add_contact(user_input:str):
    string = user_input.split(' ')
    int(string[2])
    phone_book[string[1]] = string[2]


@input_error
def change_phone(user_input:str):
    string = user_input.split(' ')
    if string[1] not in phone_book: 
        raise KeyError 

    phone_book[string[1]] = string[2]


def command_handler(command):
    return OPERATIONS.get(command, wrong_command)


def greeting(_):
    print('How can i help you?')


def parse_user_input(user_input:str):
    return user_input if user_input == 'show all' else user_input.split(' ')[0]


def show_all(_):

    if len(phone_book) == 0:
        print('No contacts in fb')
    
    for k, w in phone_book.items():
        print(f"{k.title()}'s phone number is: {w}")


@input_error
def show_phone(user_input:str):

    string = user_input.split(' ')
    print(f"{string[1].title()}'s phone is {phone_book[string[1]]}")

def wrong_command(command):
    print(f"{command} is a wrong command, use some of this commands {list(OPERATIONS.keys())[:-1]} ")
    

def main():

    stop_words = ('close', 'exit', 'good bye')

    print(f"If you wont to exit, print:", stop_words)

    while True:
        user_input = input('--->>> ').lower() 
        if user_input in stop_words or '.' in user_input:
            print('Good bye!')
            break

        command = parse_user_input(user_input)

        action = command_handler(command)
        action(user_input)


if __name__ == '__main__':
    
    OPERATIONS = {
    'hello': greeting,
    'add': add_contact,
    'change': change_phone,
    'phone': show_phone,
    'show all': show_all,
    'wrong command': wrong_command,
    }

    print(f"Hi, I'm a bot assistant and I can perform the following tasks:", list(OPERATIONS.keys())[:-1])

    phone_book = {}

    main()