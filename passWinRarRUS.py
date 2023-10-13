import datetime
import pygetwindow as gw
from pywinauto import Application, timings
import time
import pyautogui

log_file = open('log.txt', 'a')

# окна
open_windows = gw.getWindowsWithTitle("")
if not open_windows:
    print("Нет открытых окон.")
    exit(1)


print("Выберите окно для перебора пароля:")
for i, window in enumerate(open_windows):
    print(f"{i + 1}. {window.title}")

try:
    choice = int(input("Введите номер окна: ")) - 1
    if choice < 0 or choice >= len(open_windows):
        print("Неправильный выбор окна.")
        exit(1)
except ValueError:
    print("Введите корректный номер окна.")
    exit(1)

selected_window = open_windows[choice]

# Подключение к  окну
app = Application(backend='win32').connect(handle=selected_window._hWnd)
start_number = 0
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_file.write(f"{current_time} start at: {start_number}\n")

while True:
    print(start_number)
    try:
        main_window = app.top_window()
        main_window.set_focus()
        edit = main_window.Edit
        edit.set_text(str(start_number))
        time.sleep(1)
        pyautogui.press('enter')
    except Exception as e:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{current_time} password: {start_number - 1}\n")
        print(f"{current_time} пароль: {start_number - 1}")
        break

    try:
        error_window = app.window(title='Ошибка')
        error_window.set_focus()
        pyautogui.press('enter')
    except Exception as e:
        pass
    start_number += 1
log_file.close()