# project.py
# Простой современный калькулятор на Tkinter

import tkinter as tk
from tkinter import ttk


def calculate():
    """Выполнение вычисления"""
    operation = operation_var.get()
    num1 = float(entry_num1.get())
    num2 = float(entry_num2.get())

    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        result = num1 / num2

    result_label.config(text=f"Результат: {result}")


# Создание главного окна
root = tk.Tk()
root.title("Калькулятор")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Основной фрейм
frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky="nsew")

# Стили
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
style.configure("TEntry", font=("Arial", 12))

# Поле для первого числа
ttk.Label(frame, text="Первое число:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_num1 = ttk.Entry(frame)
entry_num1.grid(row=0, column=1, padx=5, pady=5)

# Поле для второго числа
ttk.Label(frame, text="Второе число:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_num2 = ttk.Entry(frame)
entry_num2.grid(row=1, column=1, padx=5, pady=5)

# Выбор операции
ttk.Label(frame, text="Операция:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
operation_var = tk.StringVar(value="+")
operations = ["+", "-", "*", "/"]
ttk.OptionMenu(frame, operation_var, "+", *operations).grid(
    row=2, column=1, padx=5, pady=5
)

# Кнопка для вычисления
ttk.Button(frame, text="Вычислить", command=calculate).grid(
    row=3, column=0, columnspan=2, pady=10
)

# Метка для результата
result_label = ttk.Label(frame, text="Результат: ", font=("Arial", 14, "bold"))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
