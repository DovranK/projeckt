# calculator.py
# Калькулятор с научными и финансовыми операциями

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import math
import json
import csv
from datetime import datetime


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("600x700")
        self.history = []
        self.history_file = "history.json"
        self.load_history()
        self.root.set_theme("equilux")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        self.display = ttk.Entry(frame, font=("Arial", 20), justify="right")
        self.display.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

        self.entry_num1 = ttk.Entry(frame, font=("Arial", 12))
        self.entry_num1.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.entry_num2 = ttk.Entry(frame, font=("Arial", 12))
        self.entry_num2.grid(row=1, column=3, columnspan=2, padx=5, pady=5, sticky="ew")

        self.operation_var = tk.StringVar(value="+")
        operations = [
            "+",
            "-",
            "*",
            "/",
            "^",
            "sqrt",
            "sin",
            "cos",
            "log",
            "%",
            "amort",
        ]
        operation_menu = ttk.OptionMenu(frame, self.operation_var, "+", *operations)
        operation_menu.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.angle_mode = tk.StringVar(value="deg")
        ttk.Radiobutton(
            frame, text="Градусы", variable=self.angle_mode, value="deg"
        ).grid(row=2, column=3, padx=5)
        ttk.Radiobutton(
            frame, text="Радианы", variable=self.angle_mode, value="rad"
        ).grid(row=2, column=4, padx=5)

        buttons = [
            ("7", 3, 0),
            ("8", 3, 1),
            ("9", 3, 2),
            ("C", 3, 3),
            ("sin", 3, 4),
            ("4", 4, 0),
            ("5", 4, 1),
            ("6", 4, 2),
            ("=", 4, 3),
            ("cos", 4, 4),
            ("1", 5, 0),
            ("2", 5, 1),
            ("3", 5, 2),
            (".", 5, 3),
            ("log", 5, 4),
            ("0", 6, 0),
            ("√", 6, 1),
            ("^", 6, 2),
            ("%", 6, 3),
            ("amort", 6, 4),
        ]
        for text, row, col in buttons:
            cmd = lambda t=text: self.button_click(t)
            ttk.Button(frame, text=text, command=cmd).grid(
                row=row, column=col, padx=2, pady=2, sticky="ew"
            )

        ttk.Label(frame, text="История:").grid(
            row=7, column=0, columnspan=5, pady=5, sticky="w"
        )
        self.history_listbox = tk.Listbox(frame, height=10, font=("Arial", 10))
        self.history_listbox.grid(
            row=8, column=0, columnspan=5, padx=5, pady=5, sticky="nsew"
        )
        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.history_listbox.yview
        )
        scrollbar.grid(row=8, column=5, sticky="ns")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        ttk.Button(frame, text="Экспорт CSV", command=self.export_csv).grid(
            row=9, column=0, columnspan=3, pady=5, sticky="ew"
        )
        ttk.Button(frame, text="Экспорт JSON", command=self.export_json).grid(
            row=9, column=3, columnspan=2, pady=5, sticky="ew"
        )

        for entry in self.history:
            self.history_listbox.insert(
                tk.END,
                f"{entry['timestamp']}: {entry['expression']} = {entry['result']}",
            )

        frame.columnconfigure([0, 1, 2, 3, 4], weight=1)
        frame.rowconfigure(8, weight=1)
        self.root.bind("<Key>", self.key_press)

    def load_history(self):
        try:
            with open(self.history_file, "r") as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f)

    def export_json(self):
        with open("exported_history.json", "w") as f:
            json.dump(self.history, f)
        messagebox.showinfo("Успех", "История экспортирована в JSON")

    def export_csv(self):
        with open("exported_history.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Дата", "Операция", "Результат"])
            for entry in self.history:
                writer.writerow(
                    [entry["timestamp"], entry["expression"], entry["result"]]
                )
        messagebox.showinfo("Успех", "История экспортирована в CSV")

    def key_press(self, event):
        if event.char in "0123456789.+-*/":
            self.display.insert(tk.END, event.char)
        elif event.keysym == "Return":
            self.calculate()
        elif event.keysym == "BackSpace":
            self.display.delete(tk.END + "-1c")

    def button_click(self, char):
        if char == "C":
            self.entry_num1.delete(0, tk.END)
            self.entry_num2.delete(0, tk.END)
            self.display.delete(0, tk.END)
        elif char == "=":
            self.calculate()
        elif char in ["sin", "cos", "log", "√", "^", "%", "amort"]:
            self.operation_var.set({"√": "sqrt"}.get(char, char))
            self.calculate()
        else:
            self.display.insert(tk.END, char)

    def calculate(self):
        try:
            operation = self.operation_var.get()
            num1 = float(self.entry_num1.get() or self.display.get())

            if operation not in ["sqrt", "sin", "cos", "log"]:
                num2 = float(self.entry_num2.get())
            else:
                num2 = None

            angle = num1
            if operation in ["sin", "cos"] and self.angle_mode.get() == "deg":
                angle = math.radians(num1)

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
                result = math.sin(angle)
            elif operation == "cos":
                result = math.cos(angle)
            elif operation == "log":
                if num1 <= 0:
                    raise ValueError("Логарифм неопределён")
                result = math.log10(num1)
            elif operation == "%":
                result = num1 * (num2 / 100)
            elif operation == "amort":
                rate = num2 / 1200
                nper = num1
                result = (rate * 1000000) / (1 - (1 + rate) ** -nper)

            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))

            entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "expression": f"{operation}({num1}"
                + (f", {num2}" if num2 is not None else "")
                + ")",
                "result": str(result),
            }
            self.history.append(entry)
            self.history_listbox.insert(
                tk.END,
                f"{entry['timestamp']}: {entry['expression']} = {entry['result']}",
            )
            self.save_history()

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = CalculatorApp(root)
    root.mainloop()
