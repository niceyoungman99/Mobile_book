import os
import json
import re
from datetime import datetime


def load_phonebook(filename):
    """Загружает телефонный справочник из файла."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_phonebook(filename, phonebook):
    """Сохраняет телефонный справочник в файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(phonebook, file, indent=4, ensure_ascii=False)


def format_name(name):
    """Форматирует имя и фамилию с заглавной буквы."""
    return name.strip().capitalize()


def validate_name(name):
    """Проверяет, что имя или фамилия содержат только латиницу, цифры и символ "."."""
    if not re.fullmatch(r'^[A-Z][a-zA-Z0-9\s]*$', format_name(name)):
        raise ValueError("Имя и фамилия должны содержать только латиницу, цифры или символ ")
    return format_name(name)


def validate_phone(phone):
    """Проверяет и форматирует номер телефона."""
    phone = phone.strip()
    phone = re.sub(r"^\+7", "8", phone)
    if re.fullmatch(r"8\d{10}", phone):
        return phone
    raise ValueError("Некорректный номер телефона! Формат: 11 цифр, начиная с 8.")


def validate_date(date):
    """Проверяет корректность введенной даты и её значение относительно текущей даты."""
    try:
        if not date:
            return None
        parsed_date = datetime.strptime(date, "%d.%m.%Y")
        if parsed_date >= datetime.now():
            raise ValueError("Дата должна быть раньше текущей даты.")
        return parsed_date.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Некорректная дата! Формат должен быть ДД.ММ.ГГГГ и дата меньше текущей.")


def calculate_age(birth_date):
    """Вычисляет возраст на основе даты рождения."""
    if not birth_date:
        return "Дата рождения не указана."
    birth_date = datetime.strptime(birth_date, "%d.%m.%Y")
    today = datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return f"{age} лет"


def prompt_correct_name():
    """Предлагает пользователю ввести имя или выйти в главное меню."""
    while True:
        try:
            name = input("Введите имя: ")
            return validate_name(name)
        except ValueError as e:
            print(e)
            while True:
                choice = input("1. Ввести имя заново\n2. Выйти в главное меню\nВаш выбор: ")
                if choice == "1":
                    return prompt_correct_name()
                if choice == "2":
                    return None
                else:
                    print("Некорректный выбор. Попробуйте снова.")


def prompt_correct_lastname():
    """Предлагает пользователю ввести имя или выйти в главное меню."""
    while True:
        try:
            name = input("Введите фамилию: ")
            return validate_name(name)
        except ValueError as e:
            print(e)
            while True:
                choice = input("1. Ввести фамилию заново\n2. Выйти в главное меню\nВаш выбор: ")
                if choice == "1":
                    return prompt_correct_lastname()
                if choice == "2":
                    return None
                else:
                    print("Некорректный выбор. Попробуйте снова.")


def prompt_correct_phone():
    """Предлагает пользователю ввести телефон или выйти в главное меню."""
    while True:
        try:
            phone = input("Введите номер телефона: ")
            return validate_phone(phone)
        except ValueError as e:
            print(e)
            while True:
                choice = input("1. Ввести номер телефона заново\n2. Выйти в главное меню\nВаш выбор: ")
                if choice == "1":
                    return prompt_correct_phone()
                elif choice == "2":
                    return None
                else:
                    print("Некорректный выбор. Попробуйте снова.")


def prompt_correct_date():
    """Предлагает пользователю ввести дату или выйти в главное меню."""
    while True:
        try:
            date = input("Введите дату (ДД.ММ.ГГГГ) или оставьте пустым: ")
            if not date:
                date = "-"
                return date
            return validate_date(date)
        except ValueError as e:
            print(e)
            while True:
                choice = input("1. Ввести дату заново\n2. Выйти в главное меню\nВаш выбор: ")
                if choice == "1":
                    return prompt_correct_date()
                elif choice == "2":
                    return None
                else:
                    print("Некорректный выбор. Попробуйте снова.")


def handle_non_unique(phonebook, unique_key, first_name, last_name):
    """Обрабатывает случай, когда запись не уникальна."""
    while True:
        print("Запись с таким именем и фамилией уже существует. Выберите действие:")
        print("1. Изменить существующую запись")
        print("2. Изменить данные новой записи")
        print("3. Вернуться к выбору команды")
        choice = input("Ваш выбор: ")

        if choice == "1":
            update_all_fields(phonebook, unique_key)
            return False
        elif choice == "2":
            print("Введите новые данные для добавления:")
            new_first_name = prompt_correct_name()
            if new_first_name is None:
                return False
            new_last_name = prompt_correct_lastname()
            if new_last_name is None:
                return False
            new_phone = prompt_correct_phone()
            if new_phone is None:
                return False
            new_birth_date = prompt_correct_date()
            if new_birth_date is None:
                return False

            phonebook[f"{new_first_name} {new_last_name}"] = {
                "Имя": new_first_name,
                "Фамилия": new_last_name,
                "Телефон": new_phone,
                "Дата рождения": new_birth_date
            }
            print("Новая запись успешно добавлена!")
            return False
        elif choice == "3":
            return False
        else:
            print("Некорректный выбор. Попробуйте снова.")


def add_entry(phonebook):
    """Добавляет новую запись в справочник."""
    while True:
        try:
            first_name = prompt_correct_name()
            if first_name is None:
                return
            last_name = prompt_correct_lastname()
            if last_name is None:
                return
            unique_key = f"{first_name} {last_name}"

            if unique_key in phonebook:
                if not handle_non_unique(phonebook, unique_key, first_name, last_name):
                    return

            phone = prompt_correct_phone()
            if phone is None:
                return
            birth_date = prompt_correct_date()
            if birth_date is None:
                return
            phonebook[unique_key] = {
                "Имя": first_name,
                "Фамилия": last_name,
                "Телефон": phone,
                "Дата рождения": birth_date
            }
            print("Запись добавлена!")
            return
        except ValueError as e:
            print(e)


def display_phonebook(phonebook):
    """Выводит все записи справочника."""
    if not phonebook:
        print("Справочник пуст.")
    else:
        for unique_key, data in phonebook.items():
            print(f"{unique_key}: Телефон: {data['Телефон']}, Дата рождения: {data.get('Дата рождения', 'Не указана')}")


def find_entry(phonebook):
    """Ищет запись в справочнике."""
    print("Введите данные для поиска. Оставьте поле пустым, чтобы пропустить его.")
    first_name = input("Имя: ").strip()
    last_name = input("Фамилия: ").strip()
    phone = input("Телефон: ").strip()
    birth_date = input("Дата рождения (ДД.ММ.ГГГГ): ").strip()

    if not first_name and not last_name and not phone and not birth_date:
        print("Ни один атрибут не ввёден")
        return

    results = {
        key: value for key, value in phonebook.items()
        if (not first_name or value['Имя'].lower() == first_name.lower())
           and (not last_name or value['Фамилия'].lower() == last_name.lower())
           and (not phone or value['Телефон'] == phone)
           and (not birth_date or value.get('Дата рождения') == birth_date)
    }

    if results:
        display_phonebook(results)
    else:
        print("Записей не найдено.")


def delete_entry(phonebook):
    """Удаляет запись по имени и фамилии."""
    try:
        first_name = prompt_correct_name()
        if first_name is None:
            return
        last_name = prompt_correct_lastname()
        if last_name is None:
            return
        unique_key = f"{first_name} {last_name}"

        if unique_key in phonebook:
            confirmation = input(f"Вы уверены, что хотите удалить запись {unique_key}? (да/нет): ").strip().lower()
            if confirmation == "да":
                del phonebook[unique_key]
                print("Запись удалена.")
            else:
                print("Удаление отменено.")
        else:
            print("Запись не найдена.")
    except ValueError as e:
        print(e)


def update_all_fields(phonebook, unique_key=None):
    """Обновляет все поля записи."""
    if not unique_key:
        try:
            first_name = prompt_correct_name()
            if first_name is None:
                return
            last_name = prompt_correct_lastname()
            if last_name is None:
                return
            unique_key = f"{first_name} {last_name}"
        except ValueError as e:
            print(e)
            return

    if unique_key in phonebook:
        entry = phonebook[unique_key]
        print(f"Текущие данные: {entry}")
        try:
            new_first_name = prompt_correct_name()
            if new_first_name is None:
                return
            new_last_name = prompt_correct_lastname()
            if new_last_name is None:
                return
            phone = prompt_correct_phone()
            if phone is None:
                return
            birth_date = prompt_correct_date()
            if birth_date is None:
                return

            del phonebook[unique_key]
            new_key = f"{new_first_name} {new_last_name}"
            phonebook[new_key] = {
                "Имя": new_first_name,
                "Фамилия": new_last_name,
                "Телефон": phone,
                "Дата рождения": birth_date
            }
            print("Запись обновлена!")
        except ValueError as e:
            print(e)
    else:
        print("Запись не найдена.")


def show_age(phonebook):
    """Показывает возраст человека."""
    try:
        first_name = prompt_correct_name()
        if first_name is None:
            return
        last_name = prompt_correct_lastname()
        if last_name is None:
            return
        unique_key = f"{first_name} {last_name}"

        if unique_key in phonebook:
            birth_date = phonebook[unique_key].get("Дата рождения")
            print(calculate_age(birth_date))
        else:
            print("Запись не найдена.")
    except ValueError as e:
        print(e)


def main():
    """Запускает в работу телефонный справочник"""
    filename = "phonebook.json" # файл телефонный справочник
    phonebook = load_phonebook(filename)

    commands = {
        "1": ("Просмотр всех записей", lambda: display_phonebook(phonebook)),
        "2": ("Поиск записи", lambda: find_entry(phonebook)),
        "3": ("Добавление записи", lambda: add_entry(phonebook)),
        "4": ("Удаление записи", lambda: delete_entry(phonebook)),
        "5": ("Изменение записи", lambda: update_all_fields(phonebook)),
        "6": ("Показать возраст", lambda: show_age(phonebook)),
        "7": ("Выйти", exit),
    }

    while True:
        print("\nДоступные команды:")
        for key, (desc, _) in commands.items():
            print(f"{key}. {desc}")
        choice = input("Выберите команду: ")

        if choice in commands:
            commands[choice][1]()
            save_phonebook(filename, phonebook)
        else:
            print("Некорректная команда. Попробуйте снова.")


if __name__ == "__main__":
    main()
