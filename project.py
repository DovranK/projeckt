# calculator.py
# Профессиональный современный калькулятор на Tkinter

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import math
import json


class CalculatorApp:
    def __init__(self, root):
        """Инициализация калькулятора"""
        self.root = root
        self.root.title("Профессиональный Калькулятор")
        self.root.geometry("600x700")
        self.memory = 0  # Переменная для памяти
        self.history = []
        self.history_file = "history.json"
        self.load_history()

        # Настройки темы
        self.theme = "equilux"  # Тёмная тема по умолчанию
        self.root.set_theme(self.theme)

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        """Создание интерфейса"""
        # Основной фрейм
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Поле вывода
        self.display = ttk.Entry(self.main_frame, font=("Arial", 20), justify="right")
        self.display.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

        # Поля для чисел
        self.entry_num1 = ttk.Entry(self.main_frame, font=("Arial", 12))
        self.entry_num1.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.entry_num2 = ttk.Entry(self.main_frame, font=("Arial", 12))
        self.entry_num2.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        # Кнопки операций
        operations = ["+", "-", "*", "/", "^", "sqrt", "sin", "cos", "log"]
        self.operation_var = tk.StringVar(value="+")
        operation_menu = ttk.OptionMenu(
            self.main_frame, self.operation_var, "+", *operations
        )
        operation_menu.grid(row=1, column=4, padx=5, pady=5, sticky="ew")

        # Кнопки клавиатуры
        buttons = [
            ("7", 2, 0),
            ("8", 2, 1),
            ("9", 2, 2),
            ("C", 2, 3),
            ("4", 3, 0),
            ("5", 3, 1),
            ("6", 3, 2),
            ("=", 3, 3),
            ("1", 4, 0),
            ("2", 4, 1),
            ("3", 4, 2),
            ("M+", 4, 3),
            ("0", 5, 0),
            (".", 5, 1),
            ("M-", 5, 2),
            ("MR", 5, 3),
            ("MC", 6, 3),
        ]
        for text, row, col in buttons:
            cmd = lambda t=text: self.button_click(t)
            ttk.Button(self.main_frame, text=text, command=cmd).grid(
                row=row, column=col, padx=2, pady=2, sticky="ew"
            )

        # История
        ttk.Label(self.main_frame, text="История:").grid(
            row=7, column=0, columnspan=5, pady=5, sticky="w"
        )
        self.history_listbox = tk.Listbox(
            self.main_frame, height=10, font=("Arial", 10)
        )
        self.history_listbox.grid(
            row=8, column=0, columnspan=5, padx=5, pady=5, sticky="nsew"
        )
        scrollbar = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=self.history_listbox.yview
        )
        scrollbar.grid(row=8, column=5, sticky="ns")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # Кнопки управления
        ttk.Button(
            self.main_frame, text="Экспорт истории", command=self.export_history
        ).grid(row=9, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(
            self.main_frame, text="Сменить тему", command=self.toggle_theme
        ).grid(row=9, column=2, columnspan=2, pady=5, sticky="ew")

        # Загрузка истории
        for entry in self.history:
            self.history_listbox.insert(tk.END, entry)

        # Привязка клавиатуры
        self.root.bind("<Key>", self.key_press)

        # Настройка веса
        self.main_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)
        self.main_frame.rowconfigure(8, weight=1)

    def load_history(self):
        """Загрузка истории из файла"""
        try:
            with open(self.history_file, "r") as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def save_history(self):
        """Сохранение истории в файл"""
        with open(self.history_file, "w") as f:
            json.dump(self.history, f)

    def export_history(self):
        """Экспорт истории в файл"""
        with open("exported_history.json", "w") as f:
            json.dump(self.history, f)
        messagebox.showinfo("Успех", "История экспортирована в exported_history.json")

    def toggle_theme(self):
        """Переключение темы"""
        self.theme = "radiance" if self.theme == "equilux" else "equilux"
        self.root.set_theme(self.theme)

    def button_click(self, char):
        """Обработка нажатия кнопок"""
        if char == "C":
            self.entry_num1.delete(0, tk.END)
            self.entry_num2.delete(0, tk.END)
            self.display.delete(0, tk.END)
        elif char == "=":
            self.calculate()
        elif char in ["M+", "M-", "MR", "MC"]:
            self.memory_operation(char)
        else:
            self.display.insert(tk.END, char)

    def key_press(self, event):
        """Обработка ввода с клавиатуры"""
        if event.char in "0123456789.":
            self.display.insert(tk.END, event.char)
        elif event.keysym == "Return":
            self.calculate()
        elif event.keysym == "BackSpace":
            self.display.delete(tk.END + "-1c")

    def memory_operation(self, op):
        """Операции с памятью"""
        try:
            value = float(self.display.get())
            if op == "M+":
                self.memory += value
            elif op == "M-":
                self.memory -= value
            elif op == "MR":
                self.display.delete(0, tk.END)
                self.display.insert(0, str(self.memory))
            elif op == "MC":
                self.memory = 0
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное значение в дисплее")

    def calculate(self):
        """Выполнение вычисления"""
        try:
            operation = self.operation_var.get()
            num1 = float(self.entry_num1.get() or self.display.get())

            if operation != "sqrt" and operation not in ["sin", "cos", "log"]:
                num2 = float(self.entry_num2.get())
            else:
                num2 = None

            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 == 0:
                    raise ValueError("Деление на ноль невозможно")
                result = num1 / num2
            elif operation == "^":
                result = num1**num2
            elif operation == "sqrt":
                if num1 < 0:
                    raise ValueError(
                        "Квадратный корень отрицательного числа невозможен"
                    )
                result = math.sqrt(num1)
            elif operation == "sin":
                result = math.sin(math.radians(num1))
            elif operation == "cos":
                result = math.cos(math.radians(num1))
            elif operation == "log":
                if num1 <= 0:
                    raise ValueError("Логарифм неопределён для неположительных чисел")
                result = math.log10(num1)

            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))

            # Добавление в историю
            entry = (
                f"{operation}({num1}"
                + (f", {num2}" if num2 is not None else "")
                + f") = {result}"
            )
            self.history.append(entry)
            self.history_listbox.insert(tk.END, entry)
            self.save_history()

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = CalculatorApp(root)
    root.mainloop()
