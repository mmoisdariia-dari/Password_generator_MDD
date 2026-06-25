import random
import string
import hashlib
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
    Возвращает оценку от 0 до 100, звёзды (1-5) и уровень сложности.
    """
    score = 0
    details = []
    
    # 1. Проверка длины (максимум 65 баллов)
    if len(password) >= 16:
        score += 65
        details.append("Длина отличная (+65)")
    elif len(password) >= 12:
        score += 50
        details.append("Длина хорошая (+50)")
    elif len(password) >= 8:
        score += 25
        details.append("Длина приемлемая (+25)")
    else:
        score += 0
        details.append("Пароль слишком короткий (+0)")
    
    # 2. Разнообразие символов (максимум 35 баллов)
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_special = any(c in "!@#$%^&*()-_=+" for c in password)
    
    # Подсчет типов символов
    char_types = sum([has_lower, has_upper, has_digit, has_special])
    
    if char_types >= 4:
        score += 35
        details.append("Все типы символов (+35)")
    elif char_types == 3:
        score += 25
        details.append("3 типа символов (+25)")
    elif char_types == 2:
        score += 15
        details.append("2 типа символов (+15)")
    elif char_types == 1:
        score += 5
        details.append("1 тип символов (+5)")
    
    # Определение уровня сложности и КОЛИЧЕСТВА звёзд (число от 1 до 5)
    if score >= 90:
        stars_count = 5
        level = "ОЧЕНЬ СЛОЖНЫЙ"
    elif score >= 75:
        stars_count = 4
        level = "СЛОЖНЫЙ"
    elif score >= 60:
        stars_count = 3
        level = "СРЕДНИЙ"
    elif score >= 40:
        stars_count = 2
        level = "СЛАБЫЙ"
    else:
        stars_count = 1
        level = "ОЧЕНЬ СЛАБЫЙ"

    if len(password) < 8:
        stars_count = 1
        level = "ОЧЕНЬ СЛАБЫЙ"

    # Создаём строку со звёздами (заполненные + пустые)
    stars_string = "⭐" * stars_count + "☆" * (5 - stars_count)
    
    return score, level, stars_string, details

# ==================== ШИФРОВАНИЕ ====================

# Секретная соль
SECRET_SALT = "my_secret_salt_8991"

def encrypt_password(password):
    """
    Шифрование пароля с использованием соли и хеширования.
    """
    # Комбинируем пароль с солью
    combined = password + SECRET_SALT
    # Создаём хеш SHA-256
    hashed = hashlib.sha256(combined.encode()).digest()
    # Кодируем в base64 для хранения
    encrypted = base64.b64encode(hashed).decode()
    return encrypted

def decrypt_password(encrypted_password, original_password):
    """
    Проверка пароля (сравнение хешей).
    Возвращает True, если пароль верный.
    """
    # Создаём хеш из введённого пароля
    combined = original_password + SECRET_SALT
    hashed = hashlib.sha256(combined.encode()).digest()
    encrypted = base64.b64encode(hashed).decode()
    # Сравниваем с сохранённым
    return encrypted == encrypted_password

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

# ==================== ИИ-ИНСТРУМЕНТ ====================

# Список популярных (слабых) паролей - "готовые данные"
POPULAR_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123", 
    "monkey", "1234567", "letmein", "trustno1", "dragon",
    "baseball", "iloveyou", "master", "sunshine", "ashley",
    "bailey", "passw0rd", "shadow", "123123", "654321",
    "superman", "qazwsx", "michael", "football", "password1"
]

# Простые паттерны, которые ИИ считает слабыми
WEAK_PATTERNS = [
    "123", "abc", "qwerty", "zxcv", "asdf"
]

def ai_password_check(password):
    """
    ИИ-проверка пароля на основе готовых данных.
    Возвращает рекомендации по улучшению.
    """
    recommendations = []
    password_lower = password.lower()
    
    # Проверка на длину
    if len(password) < 8:
        recommendations.append("⚠️  Пароль слишком короткий (меньше 8 символов)!")
    elif len(password) < 12:
        recommendations.append("⚠️  Рекомендуется увеличить длину до 12+ символов")
    
    # Проверка на популярность
    if password_lower in POPULAR_PASSWORDS:
        recommendations.append("⚠️  Пароль находится в списке популярных!")
    
    # Проверка на простые паттерны
    for pattern in WEAK_PATTERNS:
        if pattern in password_lower:
            recommendations.append(f"⚠️  Содержит простой паттерн '{pattern}'")
            break
    
    # Проверка на последовательности
    if password.isdigit():
        recommendations.append("⚠️  Только цифры — легко подобрать!")
    
    if password.isalpha():
        recommendations.append("⚠️  Только буквы — недостаточно сложно!")
    
    # Проверка на чередование цифр и букв (простой паттерн)
    import re
    if re.match(r'^\d+[a-zA-Z]+$', password) or re.match(r'^[a-zA-Z]+\d+$', password):
        if len(password) < 10:
            recommendations.append("⚠️  Простой паттерн: цифры + буквы (или наоборот)")
    
    # Проверка на повторяющиеся символы
    if len(set(password)) < len(password) / 2:
        recommendations.append("⚠️  Много повторяющихся символов!")
    
    # Проверка на клавиатурные паттерны
    keyboard_patterns = ['qwerty', 'asdf', 'zxcv', 'qazwsx', '1qaz', '2wsx']
    for pattern in keyboard_patterns:
        if pattern in password_lower:
            recommendations.append(f"⚠️  Содержит клавиатурный паттерн '{pattern}'")
            break
    
    # Проверка на отсутствие спецсимволов
    has_special = any(c in "!@#$%^&*()-_=+" for c in password)
    if not has_special and len(password) < 12:
        recommendations.append("⚠️  Нет специальных символов (!@#$%^&*)")
    
    return recommendations

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
    
    while True:
        length_input = input("Длина пароля (по умолчанию 12): ")
        
        # Если просто нажали Enter — берём 12
        if length_input == '':
            length = 12
            break
        
        # Проверяем, что введены только цифры
        if length_input.isdigit():
            length = int(length_input)
            if length < 1:
                print("Длина пароля должна быть хотя бы 1 символ!")
                continue
            else:
                break
        else:
            print("Нужно ввести число. Попробуйте снова.")

    use_uppercase = input("Заглавные буквы? (да/нет, по умолчанию да): ").lower() != 'нет'
    use_digits = input("Цифры? (да/нет, по умолчанию да): ").lower() != 'нет'
    use_special = input("Спецсимволы? (да/нет, по умолчанию да): ").lower() != 'нет'
    
    password = generate_password(length, use_digits, use_special, use_uppercase)
    
    print(f"\n>>> Сгенерированный пароль: {password}")
    
    # Сразу проверяем сложность
    score, level, stars, details = check_password_complexity(password)
    print(f">>> Сложность: {level} {stars} ({score}/100)")
    
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
    
    score, level, stars, details = check_password_complexity(password)
    
    ai_recommendations = ai_password_check(password)
    
    print(f"\n--- РЕЗУЛЬТАТЫ ПРОВЕРКИ ---")
    print(f"Оценка: {score}/100")
    print(f"Уровень: {level} {stars}")
    print("\nДетали:")
    for detail in details:
        print(f"  - {detail}")
    
    if ai_recommendations:
        print("\n💡 ИИ-рекомендации:")
        for rec in ai_recommendations:
            print(f"  {rec}")
    else:
        print("\n✅ ИИ-анализ: пароль хороший!") 

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
    score, level, stars, details = check_password_complexity("StrongPass123!")
    assert score > 50, "Оценка слишком низкая!"
    assert stars.count("⭐") >= 3, "Звёзд должно быть не меньше 3!"
    print(f"✓ Сложность определена: {level} {stars} ({score}/100)")
    
    # Тест 3: Шифрование
    print("\nТест 3: Шифрование/проверка...")
    test_pwd = "TestPassword123"
    encrypted = encrypt_password(test_pwd)
    
    # Проверяем, что правильный пароль проходит проверку
    is_valid = decrypt_password(encrypted, test_pwd)
    assert is_valid == True, "Правильный пароль не прошёл проверку!"
    print("✓ Шифрование работает корректно")
    
    # Проверяем, что неправильный пароль не проходит
    is_invalid = decrypt_password(encrypted, "WrongPassword")
    assert is_invalid == False, "Неправильный пароль прошёл проверку!"
    print("✓ Защита от неправильных паролей работает")
    
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
                    
        elif choice == "4":
            print("\nДо свидания!")
            break
            
        else:
            print("Неверный выбор! Попробуйте снова.")
