def calculator():
    print("Простой калькулятор")
    print("Доступные операции: +, -, *, /")
    
    while True:
        try:
            num1 = float(input("Введите первое число: "))
            op = input("Введите операцию (+, -, *, /) или 'q' для выхода: ")
            if op == 'q':
                print("Выход из калькулятора")
                break
            num2 = float(input("Введите второе число: "))
            
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    print("Ошибка: деление на ноль!")
                    continue
                result = num1 / num2
            else:
                print("Неверная операция!")
                continue
            
            print(f"Результат: {num1} {op} {num2} = {result}")
        except ValueError:
            print("Ошибка: введите корректное число!")

if __name__ == "__main__":
    calculator()
