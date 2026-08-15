# -*- coding: utf-8 -*-
"""
ГЛАВНЫЙ ФАЙЛ НАСТРОЙКИ OFFLINE РЕЖИМА
Этот файл должен импортироваться ПЕРВЫМ перед любыми другими модулями игры.
Он настраивает sys.path и подменяет все движковые модули на mock-версии.

ИНСТРУКЦИЯ ПО ПОДКЛЮЧЕНИЮ:
1. В самом начале главного скрипта запуска (перед всеми импортами) добавить:
   import offline_init
   
2. Или добавить в начало каждого основного файла:
   try:
       import offline_init
   except ImportError:
       pass  # Если запускается в оригинальном движке
"""

import sys
import os

# Получаем директорию текущего скрипта
_script_dir = os.path.dirname(os.path.abspath(__file__))

# Добавляем директорию scripts в начало sys.path чтобы наши mock-модули
# имели приоритет над оригинальными (если они есть в системе)
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

# Добавляем поддиректории для лучшего доступа
_client_dir = os.path.join(_script_dir, 'client')
if _client_dir not in sys.path:
    sys.path.insert(0, _client_dir)

print "=" * 60
print "OFFLINE MODE INITIALIZED"
print "=" * 60
print "Scripts directory:", _script_dir
print "Python path updated with", len([p for p in sys.path if 'scripts' in p or 'client' in p]), "paths"
print "-" * 60

# Проверяем наличие mock-модулей и предупреждаем если их нет
_missing_modules = []

_required_mocks = [
    ('BigWorld', os.path.join(_script_dir, 'BigWorld.py')),
    ('ResMgr', os.path.join(_script_dir, 'ResMgr.py')),
    ('Pixie', os.path.join(_script_dir, 'Pixie.py')),
    ('Math', os.path.join(_script_dir, 'Math.py')),
    ('FX', os.path.join(_script_dir, 'FX.py')),
    ('GUI', os.path.join(_script_dir, 'GUI.py')),
]

for module_name, module_path in _required_mocks:
    if os.path.exists(module_path):
        print "[OK] Mock module found:", module_name
    else:
        print "[WARN] Mock module NOT found:", module_name
        _missing_modules.append(module_name)

if _missing_modules:
    print "-" * 60
    print "WARNING: Some mock modules are missing!"
    print "Missing:", ', '.join(_missing_modules)
    print "The game may crash if it tries to import these modules."
    print "-" * 60

# Предварительно импортируем ключевые модули чтобы убедиться что они работают
try:
    import BigWorld
    print "[OK] BigWorld mock loaded successfully"
except Exception as e:
    print "[ERROR] Failed to load BigWorld mock:", e

try:
    import ResMgr
    print "[OK] ResMgr mock loaded successfully"
except Exception as e:
    print "[ERROR] Failed to load ResMgr mock:", e

try:
    import Pixie
    print "[OK] Pixie mock loaded successfully"
except Exception as e:
    print "[ERROR] Failed to load Pixie mock:", e

try:
    import Math
    print "[OK] Math mock loaded successfully"
except Exception as e:
    print "[ERROR] Failed to load Math mock:", e

try:
    import FX
    print "[OK] FX mock loaded successfully"
except Exception as e:
    print "[ERROR] Failed to load FX mock:", e

try:
    import GUI
    print "[OK] GUI mock loaded successfully"
except Exception as e:
    print "[ERROR] Failed to load GUI mock:", e

# Импортируем систему сохранения из mocks
try:
    from client.mocks import save_game_state, get_game_state, update_player_data
    print "[OK] Save system loaded from client.mocks"
    
    # Сохраняем при выходе (можно вызвать вручную)
    def save_on_exit():
        print "Saving game state on exit..."
        save_game_state()
    
    import atexit
    atexit.register(save_on_exit)
    print "[OK] Auto-save registered"
    
except Exception as e:
    print "[WARN] Save system not available:", e

print "-" * 60
print "Offline initialization complete!"
print "You can now start the game."
print "=" * 60

# Экспортируем полезные функции для использования в других модулях
__all__ = [
    'save_game_state',
    'get_game_state', 
    'update_player_data',
    'BigWorld',
    'ResMgr',
    'Pixie',
    'Math',
    'FX',
    'GUI'
]
