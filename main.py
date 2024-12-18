import random
import os

# Функция генерации случайных чисел
def generate_random_numbers(count, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(count)]

# Функция сортировки чисел
def sort_numbers(numbers):
    return sorted(numbers)

# Функция вычисления статистики
def calculate_statistics(numbers):
    average = sum(numbers) / len(numbers)
    minimum = min(numbers)
    maximum = max(numbers)
    return average, minimum, maximum

# Функция вывода таблицы умножения
def print_multiplication_table(size):
    print("Таблица умножения:")
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            print(f"{i * j:4}", end="")
        print()

# Функция записи чисел в файл
def write_numbers_to_file(numbers, filename):
    with open(filename, "w") as file:
        for number in numbers:
            file.write(f"{number}\n")

# Функция чтения чисел из файла
def read_numbers_from_file(filename):
    if not os.path.exists(filename):
        print("Файл не найден.")
        return []
    with open(filename, "r") as file:
        return [int(line.strip()) for line in file]

# Главная функция программы
def main():
    # Генерация случайных чисел
    numbers = generate_random_numbers(20, 1, 100)
    print("Сгенерированные числа:", numbers)

    # Сортировка чисел
    sorted_numbers = sort_numbers(numbers)
    print("Отсортированные числа:", sorted_numbers)

    # Вычисление статистики
    avg, min_val, max_val = calculate_statistics(numbers)
    print(f"Среднее значение: {avg:.2f}, Минимум: {min_val}, Максимум: {max_val}")

    # Вывод таблицы умножения
    print_multiplication_table(5)

    # Запись чисел в файл
    filename = "numbers.txt"
    write_numbers_to_file(sorted_numbers, filename)
    print(f"Числа записаны в файл {filename}.")

    # Чтение чисел из файла
    read_numbers = read_numbers_from_file(filename)
    print("Прочитанные из файла числа:", read_numbers)

# Запуск программы
if __name__ == "__main__":
    main()
