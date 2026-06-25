import random
import string
import base64
import json
import os

# ==================== ГЕНЕРАТОР ПАРОЛЕЙ ====================

def generate_password(length=12, use_digits=True, use_special=True, use_uppercase=True):
    """
    Генерация случайного пароля с настраиваемыми параметрами.
    """
    # Базовый набор символов - всегда строчные буквы
    characters = string.ascii_lowercase
    
    # Добавление символов в зависимости от параметров
    if use_digits:
        characters += string.digits
    if use_special:
        characters += "!@#$%^&*()-_=+"
    if use_uppercase:
        characters += string.ascii_uppercase
    
    # Генерируем пароль
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# ==================== ПРОВЕРКА ПАРОЛЯ ====================

def check_password_complexity(password):
    """
    Проверка сложности пароля.
    Возвращает оценку от 0 до 100 и уровень сложности.
    """
    score = 0
    details = []
    
    # 1. Проверка длины (максимум 40 баллов)
    if len(password) >= 16:
        score += 40
        details.append("Длина отличная (+40)")
    elif len(password) >= 12:
        score += 30
        details.append("Длина хорошая (+30)")
    elif len(password) >= 8:
        score += 20
        details.append("Длина приемлемая (+20)")
    else:
        details.append("Пароль слишком короткий (+0)")
    
    # 2. Разнообразие символов (максимум 60 баллов)
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_special = any(c in "!@#$%^&*()-_=+" for c in password)
    
    # Подсчет типов символов
    char_types = sum([has_lower, has_upper, has_digit, has_special])
    
    if char_types >= 4:
        score += 60
        details.append("Все типы символов (+60)")
    elif char_types == 3:
        score += 45
        details.append("3 типа символов (+45)")
    elif char_types == 2:
        score += 30
        details.append("2 типа символов (+30)")
    elif char_types == 1:
        score += 15
        details.append("1 тип символов (+15)")
    
    # Определение уровня сложности
    if score >= 80:
        level = "ОЧЕНЬ СЛОЖНЫЙ"
    elif score >= 60:
        level = "СЛОЖНЫЙ"
    elif score >= 40:
        level = "СРЕДНИЙ"
    else:
        level = "СЛАБЫЙ"
    
    return score, level, details

# ==================== ШИФРОВАНИЕ ====================

def encrypt_password(password, key="secret_key_123"):
    """
    Простое шифрование пароля (base64).
    """
    # Комбинируем пароль с ключом
    combined = password + key
    # Кодируем в base64
    encrypted = base64.b64encode(combined.encode()).decode()
    return encrypted

def decrypt_password(encrypted_password, key="secret_key_123"):
    """
    Расшифровка пароля.
    """
    # Декодируем base64
    decoded = base64.b64decode(encrypted_password.encode()).decode()
    # Убираем ключ
    password = decoded.replace(key, "")
    return password

def save_passwords(passwords_list, filename="passwords.json"):
    """
    Сохранение паролей в зашифрованном виде в файл.
    """
    encrypted_data = []
    for pwd in passwords_list:
        encrypted_data.append(encrypt_password(pwd))
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(encrypted_data, f, ensure_ascii=False, indent=2)
    print(f"Пароли сохранены в файл {filename}")

# ==================== ИНТЕРФЕЙС ====================

def main_menu():
    """
    Главное меню программы.
    """
    print("\n" + "="*50)
    print("ГЕНЕРАТОР СЛУЧАЙНЫХ ПАРОЛЕЙ")
    print("="*50)
    print("1. Сгенерировать пароль")
    print("2. Проверить сложность пароля")
    print("3. Сохранить пароли в файл")
    print("4. Выход")
    print("="*50)
    
    choice = input("Выберите пункт (1-4): ")
    return choice

def generate_password_menu():
    """
    Меню генерации пароля.
    """
    print("\n--- НАСТРОЙКИ ГЕНЕРАЦИИ ---")
    
    try:
        length = int(input("Длина пароля (по умолчанию 12): ") or "12")
    except ValueError:
        length = 12
    
    use_uppercase = input("Заглавные буквы? (да/нет, по умолчанию да): ").lower() != 'нет'
    use_digits = input("Цифры? (да/нет, по умолчанию да): ").lower() != 'нет'
    use_special = input("Спецсимволы? (да/нет, по умолчанию да): ").lower() != 'нет'
    
    password = generate_password(length, use_digits, use_special, use_uppercase)
    
    print(f"\n>>> Сгенерированный пароль: {password}")
    
    # Сразу проверяем сложность
    score, level, details = check_password_complexity(password)
    print(f">>> Сложность: {level} ({score}/100)")
    
    return password

def check_password_menu():
    """
    Меню проверки пароля.
    """
    # Создаем строку со всеми русскими буквами
    russian_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    
    while True:
        password = input("\nВведите пароль для проверки: ")
        
        # Проверяем, есть ли русские буквы в пароле
        has_cyrillic = False
        for i in password:
            if i in russian_letters:
                has_cyrillic = True
                break
        
        if has_cyrillic:
            print("Ошибка: пароль содержит кириллицу. Введите пароль только с латинскими символами.")
            continue
        
        break
    
    score, level, details = check_password_complexity(password)
    
    print(f"\n--- РЕЗУЛЬТАТЫ ПРОВЕРКИ ---")
    print(f"Оценка: {score}/100")
    print(f"Уровень: {level}")
    print("\nДетали:")
    for detail in details:
        print(f"  - {detail}")

# ==================== ТЕСТЫ ====================

def run_tests():
    """
    Простые тесты для проверки работы программы.
    """
    print("\n" + "="*50)
    print("ЗАПУСК ТЕСТОВ")
    print("="*50)
    
    # Тест 1: Генерация пароля
    print("\nТест 1: Генерация пароля...")
    pwd = generate_password(12, True, True, True)
    assert len(pwd) == 12, "Длина пароля неверная!"
    print("✓ Пароль сгенерирован правильно")
    
    # Тест 2: Проверка сложности
    print("\nТест 2: Проверка сложности...")
    score, level, details = check_password_complexity("StrongPass123!")
    assert score > 50, "Оценка слишком низкая!"
    print(f"✓ Сложность определена: {level} ({score}/100)")
    
    # Тест 3: Шифрование
    print("\nТест 3: Шифрование/расшифровка...")
    test_pwd = "TestPassword123"
    encrypted = encrypt_password(test_pwd)
    decrypted = decrypt_password(encrypted)
    assert decrypted == test_pwd, "Расшифровка не работает!"
    print("✓ Шифрование работает корректно")
    
    print("\n" + "="*50)
    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("="*50)

# ==================== ОСНОВНАЯ ПРОГРАММА ====================

if __name__ == "__main__":
    # Запускаем тесты при старте
    run_tests()
    
    saved_passwords = []
    
    while True:
        choice = main_menu()
        
        if choice == "1":
            # Генерация пароля
            new_password = generate_password_menu()
            saved_passwords.append(new_password)
            
        elif choice == "2":
            # Проверка пароля
            check_password_menu()
            
        elif choice == "3":
            # Сохранение
            if saved_passwords:
                save_passwords(saved_passwords)
            else:
                print("Нет паролей для сохранения!")
                    
        elif choice == "5":
            print("\nДо свидания!")
            break
            
        else:
            print("Неверный выбор! Попробуйте снова.")