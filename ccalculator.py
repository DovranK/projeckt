import tkinter as tk

def button_click(number):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + str(number))

def clear():
    entry.delete(0, tk.END)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Ошибка")

# Создание окна
window = tk.Tk()
window.title("Графический калькулятор")
window.geometry("300x400")

# Поле ввода
entry = tk.Entry(window, width=20, font=('Arial', 14))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Кнопки
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

row = 1
col = 0
for button in buttons:
    if button == '=':
        cmd = calculate
    else:
        cmd = lambda x=button: button_click(x)
    tk.Button(window, text=button, width=5, height=2, font=('Arial', 12), command=cmd).grid(row=row, column=col, padx=2, pady=2)
    col += 1
    if col > 3:
        col = 0
        row += 1

# Кнопка очистки
tk.Button(window, text="C", width=5, height=2, font=('Arial', 12), command=clear).grid(row=row, column=col, columnspan=4, padx=2, pady=2)

# Запуск приложения
window.mainloop()
