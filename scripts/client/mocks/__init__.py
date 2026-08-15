# -*- coding: utf-8 -*-
"""
MOCK-МОДУЛЬ ДЛЯ ОТКЛЮЧЕНИЯ СЕРВЕРНОЙ ЛОГИКИ (OFFLINE MODE)
Этот файл перехватывает все обращения к BigWorld.Entity и серверным методам.
Заменяет их на безопасные заглушки, чтобы игра работала локально без крашей.
"""

import sys
import time
import json
import os

# Глобальное хранилище состояния игры (вместо сервера)
GAME_STATE = {
    'player': {
        'name': 'Stalker',
        'level': 1,
        'xp': 0,
        'money': 1000,
        'inventory': [],
        'position': [0, 0, 0],
        'health': 100,
        'energy': 100
    },
    'quests': {},
    'friends': [],
    'clan': None,
    'premium': False,
    'last_save': None
}

# Путь для локального сохранения
SAVE_FILE = os.path.join(os.path.dirname(__file__), 'offline_save.json')

def load_game_state():
    """Загрузка прогресса из локального файла"""
    global GAME_STATE
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                GAME_STATE = json.load(f)
            print "[Mock] Game state loaded from", SAVE_FILE
        except Exception as e:
            print "[Mock] Failed to load save:", e
    return GAME_STATE

def save_game_state():
    """Сохранение прогресса в локальный файл"""
    global GAME_STATE
    GAME_STATE['last_save'] = time.time()
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(GAME_STATE, f, indent=2)
        print "[Mock] Game state saved to", SAVE_FILE
        return True
    except Exception as e:
        print "[Mock] Failed to save:", e
        return False

# Загружаем состояние при импорте
load_game_state()


class MockBaseEntity:
    """
    Заглушка для серверной сущности (self.base)
    Перехватывает все вызовы методов и возвращает безопасные значения
    """
    
    def __getattr__(self, name):
        # Возвращаем функцию-заглушку для любого метода
        def mock_method(*args, **kwargs):
            print "[Mock] Ignored server call: base.%s(%s, %s)" % (name, args, kwargs)
            
            # Специальная обработка важных методов
            if name == 'createNewAvatar':
                # Успешное создание аватара
                return True
            elif name == 'deleteCharacterForDev':
                return True
            elif name == 'restoreCharacter':
                return True
            elif name == 'activatePremiumAccount':
                GAME_STATE['premium'] = True
                return True
            elif name == 'sendMail':
                return True
            elif name == 'acceptQuest':
                quest_id = args[0] if args else kwargs.get('quest_id', 'unknown')
                GAME_STATE['quests'][quest_id] = {'status': 'active', 'progress': 0}
                return True
            elif name == 'completeQuest':
                quest_id = args[0] if args else kwargs.get('quest_id', 'unknown')
                if quest_id in GAME_STATE['quests']:
                    GAME_STATE['quests'][quest_id]['status'] = 'completed'
                return True
            elif name == 'addFriend':
                return True
            elif name == 'removeFriend':
                return True
            elif name == 'inviteToClan':
                return True
            elif name == 'leaveClan':
                GAME_STATE['clan'] = None
                return True
            elif name == 'tradeRequest':
                return False  # Торговля отключена
            elif name == 'pvpRequest':
                return False  # PvP отключен
            
            # По умолчанию возвращаем None или пустой список
            return None
        
        return mock_method


class Entity:
    """
    Заглушка для BigWorld.Entity
    Используется для наследования вместо оригинального класса
    """
    
    def __init__(self):
        self.id = hash(self) & 0xFFFFFFFF  # Имитация ID сущности
        self.position = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.base = MockBaseEntity()  # Серверная часть
        self.cell = None  # Cell-часть (тоже серверная)
        self.isClient = True
        print "[Mock] Entity created:", self.__class__.__name__
    
    def destroy(self):
        print "[Mock] Entity destroyed:", self.__class__.__name__
    
    def setPosition(self, pos):
        self.position = list(pos)
    
    def getPosition(self):
        return tuple(self.position)
    
    def setRotation(self, rot):
        self.rotation = list(rot)
    
    def getRotation(self):
        return tuple(self.rotation)
    
    def isDestroyed(self):
        return False
    
    def addTimer(self, callback, interval):
        # Простая имитация таймера (в реальности нужно интегрировать с игровым циклом)
        print "[Mock] Timer added (not implemented in mock):", interval
        return None
    
    def delTimer(self, timer_id):
        pass


# Функции-помощники для быстрой интеграции
def create_mock_entity(class_name='Entity'):
    """Создает мок-сущность с указанным именем класса"""
    return Entity()


def get_game_state():
    """Возвращает текущее состояние игры"""
    return GAME_STATE


def update_player_data(**kwargs):
    """Обновляет данные игрока"""
    for key, value in kwargs.items():
        if key in GAME_STATE['player']:
            GAME_STATE['player'][key] = value
    save_game_state()


def add_inventory_item(item_id, count=1):
    """Добавляет предмет в инвентарь"""
    GAME_STATE['player']['inventory'].append({'id': item_id, 'count': count})
    save_game_state()


def remove_inventory_item(item_id, count=1):
    """Удаляет предмет из инвентаря"""
    for i, item in enumerate(GAME_STATE['player']['inventory']):
        if item['id'] == item_id:
            if item['count'] <= count:
                GAME_STATE['player']['inventory'].pop(i)
            else:
                item['count'] -= count
            break
    save_game_state()


# Автосохранение каждые 60 секунд (можно вызвать из игрового цикла)
_last_auto_save = time.time()

def auto_save_check():
    """Проверка необходимости автосохранения"""
    global _last_auto_save
    current_time = time.time()
    if current_time - _last_auto_save > 60:
        save_game_state()
        _last_auto_save = current_time


print "[Mock] Offline mode module initialized successfully"
print "[Mock] Save file location:", SAVE_FILE
