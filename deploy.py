# -*- coding: utf-8 -*-
"""
DEPLOY SCRIPT для S.T.A.L.K.E.R. Online
Копирует файлы из репозитория в папку игры и компилирует их.

Использование:
    python deploy.py
"""

import os
import sys
import shutil
import subprocess
import datetime

# === НАСТРОЙКИ ===
# Путь к папке с игрой (куда копируем)
GAME_PATH = r"F:\SO\StalkerOnline"

# Путь к интерпретатору Python 2.7 для компиляции
PYTHON_27_EXE = r"C:\Python27\python.exe"

# Папка для бэкапов (создается внутри GAME_PATH)
BACKUP_FOLDER = "deploy_backup"

# Исключаемые папки (не копируем служебные папки git и т.д.)
EXCLUDE_FOLDERS = ['.git', '.idea', '__pycache__', 'venv', 'mocks']

# === ЛОГИКА ===

def get_script_dir():
    """Возвращает абсолютный путь к директории скрипта (репозиторий)"""
    return os.path.dirname(os.path.abspath(__file__))

def find_python_files(source_root, exclude_folders):
    """Рекурсивно находит все .py файлы, исключая ненужные папки"""
    py_files = []
    for root, dirs, files in os.walk(source_root):
        # Модифицируем dirs inplace, чтобы walk не заходил в исключенные папки
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, source_root)
                py_files.append(rel_path)
    return py_files

def compile_file(file_path):
    """Компилирует файл через py_compile"""
    try:
        # Команда: python -m py_compile <file>
        cmd = [PYTHON_27_EXE, "-m", "py_compile", file_path]
        # Запускаем скрыто, ловим вывод только при ошибке
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            return False, result.stderr
        return True, ""
    except Exception as e:
        return False, str(e)

def main():
    repo_path = get_script_dir()
    
    print("="*60)
    print("S.T.A.L.K.E.R. Online DEPLOY TOOL")
    print("="*60)
    print(f"Репозиторий: {repo_path}")
    print(f"Цель (Игра): {GAME_PATH}")
    print(f"Python 2.7:  {PYTHON_27_EXE}")
    print("="*60)

    # Проверка существования путей
    if not os.path.exists(GAME_PATH):
        print(f"❌ ОШИБКА: Папка игры не найдена: {GAME_PATH}")
        print("Проверьте переменную GAME_PATH в скрипте.")
        input("Нажмите Enter для выхода...")
        return

    if not os.path.exists(PYTHON_27_EXE):
        print(f"❌ ОШИБКА: Python 2.7 не найден: {PYTHON_27_EXE}")
        input("Нажмите Enter для выхода...")
        return

    # Создаем папку бэкапа
    backup_path = os.path.join(GAME_PATH, BACKUP_FOLDER, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    os.makedirs(backup_path, exist_ok=True)
    print(f"📁 Бэкапы сохраняются в: {backup_path}")

    # Поиск файлов
    print("\n🔍 Поиск Python файлов в репозитории...")
    py_files = find_python_files(repo_path, EXCLUDE_FOLDERS)
    print(f"Найдено файлов: {len(py_files)}")

    success_count = 0
    fail_count = 0
    skip_count = 0

    print("\n🚀 Начало копирования и компиляции...\n")

    for rel_file in py_files:
        src_file = os.path.join(repo_path, rel_file)
        dst_file = os.path.join(GAME_PATH, rel_file)
        
        # Создаем директорию назначения, если нет
        dst_dir = os.path.dirname(dst_file)
        if not os.path.exists(dst_dir):
            try:
                os.makedirs(dst_dir)
            except Exception as e:
                print(f"⚠️ Не удалось создать папку {dst_dir}: {e}")
                continue

        # Бэкап существующего файла
        if os.path.exists(dst_file):
            backup_dst = os.path.join(backup_path, rel_file)
            backup_dir = os.path.dirname(backup_dst)
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            shutil.copy2(dst_file, backup_dst)
        
        # Копирование
        try:
            shutil.copy2(src_file, dst_file)
            print(f"📄 Скопировано: {rel_file}")
        except Exception as e:
            print(f"❌ Ошибка копирования {rel_file}: {e}")
            fail_count += 1
            continue

        # Компиляция
        is_ok, error_msg = compile_file(dst_file)
        if is_ok:
            print(f"   ✅ Успешно скомпилировано.")
            success_count += 1
            # Удаляем исходник после успешной компиляции? 
            # Обычно в сталкере оставляют и .py и .pyc, или только .pyc.
            # Оставим как есть, движок сам разберется.
        else:
            print(f"   ❌ ОШИБКА КОМПИЛЯЦИИ: {error_msg.strip()}")
            print(f"   ⚠️ Восстанавливаю старую версию из бэкапа...")
            # Откат
            backup_src = os.path.join(backup_path, rel_file)
            if os.path.exists(backup_src):
                shutil.copy2(backup_src, dst_file)
                print(f"   ↩️ Файл откатчен.")
            fail_count += 1

    print("\n" + "="*60)
    print("ИТОГИ:")
    print(f"✅ Успешно: {success_count}")
    print(f"❌ Ошибки:  {fail_count}")
    print(f"⏭️ Пропущено: {skip_count}")
    print("="*60)
    
    if fail_count > 0:
        print("\n⚠️ ВНИМАНИЕ: Были ошибки компиляции! Игра может не запуститься.")
        print(f"Проверьте лог выше или файлы в {backup_path}")
    else:
        print("\n🎉 Все файлы успешно обновлены и скомпилированы!")
        print("Можно запускать игру.")

    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()
