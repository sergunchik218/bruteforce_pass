import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import threading
import string
import clipboard
from pywinauto import Application

last_found_password = None
theme = "dark"

languages = {
    "en": {
        "title": "Password Cracker",
        "window": "Enter Password Window",
        "error_window": "Error Window",
        "length": "Max Password Length",
        "type": "Password Type",
        "log": "Log",
        "copy_log": "Copy Log",
        "toggle_theme": "Toggle Theme",
        "change_language": "Change Language"
    },
    "ru": {
        "title": "Перебор паролей",
        "window": "Окно ввода пароля",
        "error_window": "Окно ошибки",
        "length": "Максимальная длина пароля",
        "type": "Тип пароля",
        "log": "Лог",
        "copy_log": "Копировать лог",
        "toggle_theme": "Сменить тему",
        "change_language": "Сменить язык"
    }
}

password_type_translations = {
    "Digits": {
        "en": "Digits",
        "ru": "Цифры",
    },
    "Digits and Letters": {
        "en": "Digits and Letters",
        "ru": "Цифры и буквы",
    },
    "Digits, Letters, and Symbols": {
        "en": "Digits, Letters, and Symbols",
        "ru": "Цифры, буквы и символы",
    }
}

current_language = "en"

button_styles = {
    "light": {
        "button_bg": "white",
    },
    "dark": {
        "button_bg": "#2E2E2E",
    }
}

def enter_password(password, target_window, error_window_title):
    try:
        app = Application().connect(title=target_window)
        app.top_window().Edit.set_text(password)
        app.top_window().type_keys("{ENTER}")
        return True
    except Exception as e:
        pass

    try:
        error_app = Application().connect(title=error_window_title, timeout=1)
        error_app.top_window().close()
    except Exception as e:
        pass

def start_password_cracking():
    target_window = window_selector.get()
    error_window_title = error_window_selector.get()
    max_password_length = int(length_selector.get())
    password_type = type_selector.get()

    if not target_window:
        messagebox.showerror(languages[current_language]["title"], "Enter the window title for password cracking.")
        return

    chars = string.digits

    if password_type == password_type_translations["Digits"][current_language]:
        chars = string.digits
    elif password_type == password_type_translations["Digits and Letters"][current_language]:
        chars = string.digits + string.ascii_letters
    elif password_type == password_type_translations["Digits, Letters, and Symbols"][current_language]:
        chars = string.digits + string.ascii_letters + string.punctuation

    def password_cracking():
        global last_found_password
        try:
            for length in range(1, max_password_length + 1):
                for password in generate_passwords(chars, length):
                    while not enter_password(password, target_window, error_window_title):
                        pass
                    log_text = f"Password entered: {password}\n"
                    log.insert(tk.END, log_text)
                    log.see(tk.END)
                    log.update_idletasks()
                    last_found_password = password
        except KeyboardInterrupt:
            if last_found_password:
                log_text = f"Password cracking was interrupted. Last found password: {last_found_password}\n"
                log.insert(tk.END, log_text)
                log.see(tk.END)
                log.update_idletasks()
                show_last_password(last_found_password)

    t = threading.Thread(target=password_cracking)
    t.start()

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

def save_log(log_text):
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_text)

def show_last_password(password):
    last_password_window = Toplevel(app)
    last_password_window.title(languages[current_language]["title"])
    label = tk.Label(last_password_window, text=f"Last found password: {password}")
    label.pack()

def toggle_theme():
    global theme
    if theme == "light":
        theme = "dark"
    else:
        theme = "light"
    apply_theme()

def change_language():
    global current_language
    if current_language == "en":
        current_language = "ru"
    else:
        current_language = "en"
    update_language()

def apply_theme():
    button_style = button_styles[theme]
    app.configure(bg=button_style["button_bg"])
    log.config(bg=button_style["button_bg"])
    change_button_styles()

def change_button_styles():
    button_bg = button_styles[theme]["button_bg"]
    style = ttk.Style()
    style.configure("TButton", foreground="black", background=button_bg)

    copy_button.config(style="TButton", compound=tk.CENTER, padding=0)
    theme_button.config(style="TButton", compound=tk.CENTER, padding=0)
    language_button.config(style="TButton", compound=tk.CENTER, padding=0)

def update_language():
    app.title(languages[current_language]["title"])
    window_label.config(text=languages[current_language]["window"])
    error_window_label.config(text=languages[current_language]["error_window"])
    length_label.config(text=languages[current_language]["length"])
    log_label.config(text=languages[current_language]["log"])
    start_button.config(text=languages[current_language]["title"])
    copy_button.config(text=languages[current_language]["copy_log"])
    theme_button.config(text=languages[current_language]["toggle_theme"])
    language_button.config(text=languages[current_language]["change_language"])

    type_selector["values"] = [password_type_translations[type][current_language] for type in
                               ["Digits", "Digits and Letters", "Digits, Letters, and Symbols"]]
    type_selector.set(password_type_translations[type_selector.get()][current_language])

    if last_found_password:
        show_last_password(last_found_password)

app = tk.Tk()
app.title(languages[current_language]["title"])
app.configure(bg="white")

window_label = tk.Label(app, text=languages[current_language]["window"])
window_label.grid(row=0, column=0)

window_selector = tk.Entry(app)
window_selector.grid(row=0, column=1)

error_window_label = tk.Label(app, text=languages[current_language]["error_window"])
error_window_label.grid(row=1, column=0)

error_window_selector = tk.Entry(app)
error_window_selector.grid(row=1, column=1)

length_label = tk.Label(app, text=languages[current_language]["length"])
length_label.grid(row=2, column=0)

length_selector = tk.Entry(app)
length_selector.grid(row=2, column=1)

type_label = tk.Label(app, text=languages[current_language]["type"])
type_label.grid(row=3, column=0)

type_selector = ttk.Combobox(app, values=["Digits", "Digits and Letters", "Digits, Letters, and Symbols"])
type_selector.set("Digits")
type_selector.grid(row=3, column=1)

start_button = ttk.Button(app, text=languages[current_language]["title"], command=start_password_cracking, style="TButton")
start_button.grid(row=4, column=0, columnspan=2)

log_label = tk.Label(app, text=languages[current_language]["log"])
log_label.grid(row=5, column=0, columnspan=2)

log = tk.Text(app, height=10, width=40)
log.grid(row=6, column=0, columnspan=2)

copy_button = ttk.Button(app, text=languages[current_language]["copy_log"], command=lambda: clipboard.copy(log.get("1.0", "end-1c")), style="TButton")
copy_button.grid(row=7, column=0, columnspan=2)

theme_button = ttk.Button(app, text=languages[current_language]["toggle_theme"], command=toggle_theme, style="TButton")
theme_button.grid(row=8, column=0, columnspan=2)

language_button = ttk.Button(app, text=languages[current_language]["change_language"], command=change_language, style="TButton")
language_button.grid(row=9, column=0, columnspan=2)

apply_theme()
update_language()

app.mainloop()


