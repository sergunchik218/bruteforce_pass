import msvcrt
from pywinauto import Application
from pywinauto.timings import TimeoutError, wait_until
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
import datetime

log_file = open('log.txt', 'a')

# Подключение к уже открытому окну приложения
app = Application().connect(title='PNOZmulti Configurator')

# Получение главного окна приложения
main_window = app.window(title='Login')


# Найдите поле ввода по его заголовку
edit = main_window.Edit



#нажать кнопку
ok_button = main_window.Button
ok_button.click()

startnuber = 0
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_file.write(f"{current_time} start at: {startnuber}\n")

for i in range(startnuber, 100000):
    print(i)
    try:
        edit.set_text(i)
        ok_button.click()
    except ElementNotFoundError:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{current_time} password: {i-1}\n")
        print(f"{current_time} пароль: {i-1}")
        break  # Выход из цикла, если окно не появилось в течение 3 секунд

    try:
        # Попытка получения окна с заданным индексом и заголовком в течение 3 секунд
        window = app.window(found_index=1, title='PNOZmulti Configurator')
        wait_until(timeout=3, retry_interval=0.5, func=window.exists)
        print("\nОкно найдено!")
    except TimeoutError:
        print("\nОкно не появилось в течение 3 секунд.")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{current_time} password: {i}\n")
        input("Продолжить...")  # Ожидание нажатия Enter для продолжения


    new_window = app.window(found_index=0, title='PNOZmulti Configurator')
    ok_button2 = new_window.Button
    ok_button2.click()

    if msvcrt.kbhit():  # Проверка, нажата ли клавиша на клавиатуре
        key = msvcrt.getch()  # Получение кода клавиши
        if key == b' ':  # Проверка, является ли клавиша пробелом
            input("Продолжить...")  # Ожидание нажатия Enter для продолжения

log_file.close()