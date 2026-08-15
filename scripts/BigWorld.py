# -*- coding: utf-8 -*-
"""
ЗАГЛУШКА ДЛЯ МОДУЛЯ BigWorld
Этот файл должен лежать в корне scripts/ и перехватывать импорт BigWorld
Заменяет весь функционал движка на безопасные мок-реализации
"""

import sys
import os

# Добавляем путь к mocks, чтобы работала относительная импортизация
_current_dir = os.path.dirname(__file__)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

# Импортируем нашу мок-реализацию Entity из client.mocks
try:
    from client.mocks import Entity as MockEntity
except ImportError:
    # Если не нашли, пробуем альтернативный путь
    try:
        from mocks import Entity as MockEntity
    except ImportError:
        # Фоллбэк - создаем класс прямо здесь
        class MockEntity:
            def __init__(self):
                self.id = 0
                self.position = [0, 0, 0]
                self.base = type('MockBase', (), {
                    '__getattr__': lambda s, name: lambda *a, **k: None
                })()
            def destroy(self): pass


# Основные константы и функции BigWorld
class BigWorld:
    """Основной класс-заглушка для всего модуля BigWorld"""
    
    Entity = MockEntity
    
    # Имитация пространства игрового мира
    _entities = {}
    _next_id = 1
    
    @staticmethod
    def entity(id):
        """Получить сущность по ID"""
        return BigWorld._entities.get(id, None)
    
    @staticmethod
    def entities():
        """Вернуть все сущности"""
        return BigWorld._entities.values()
    
    @staticmethod
    def createEntity(className, position=(0,0,0), rotation=(0,0,0)):
        """Создать новую сущность"""
        entity = MockEntity()
        entity.id = BigWorld._next_id
        entity.setPosition(position)
        entity.setRotation(rotation)
        BigWorld._entities[BigWorld._next_id] = entity
        BigWorld._next_id += 1
        print "[BigWorld.Mock] Created entity:", className, "ID:", entity.id
        return entity
    
    @staticmethod
    def destroyEntity(entity):
        """Уничтожить сущность"""
        if entity and hasattr(entity, 'id'):
            if entity.id in BigWorld._entities:
                del BigWorld._entities[entity.id]
            if hasattr(entity, 'destroy'):
                entity.destroy()
        print "[BigWorld.Mock] Destroyed entity"
    
    @staticmethod
    def loadTerrain(name):
        """Загрузка территории (заглушка)"""
        print "[BigWorld.Mock] Loading terrain:", name
        return True
    
    @staticmethod
    def addSpaceGeometryMapping(spaceID, geometry):
        """Добавление геометрии (заглушка)"""
        pass
    
    @staticmethod
    def getSpaceID():
        """Получить ID пространства (заглушка)"""
        return 1
    
    @staticmethod
    def getSpaceCamera():
        """Получить камеру (заглушка)"""
        return None
    
    @staticmethod
    def newPlayerAvatar(avatarType, position, direction):
        """Создание аватара игрока (заглушка)"""
        print "[BigWorld.Mock] Creating player avatar:", avatarType
        return BigWorld.createEntity('Avatar', position, direction)
    
    @staticmethod
    def disconnect(reason=''):
        """Отключение от сервера (в офлайне просто лог)"""
        print "[BigWorld.Mock] Disconnect called:", reason
    
    @staticmethod
    def reconnect():
        """Переподключение (заглушка)"""
        pass
    
    @staticmethod
    def isReconnecting():
        """Проверка переподключения"""
        return False
    
    @staticmethod
    def callback(interval, func, *args):
        """Обратный вызов через интервал (упрощенная реализация)"""
        # В реальной игре это должно интегрироваться с игровым циклом
        print "[BigWorld.Mock] Callback registered:", interval, func.__name__
        return None
    
    @staticmethod
    def cancelCallback(callbackID):
        """Отмена обратного вызова"""
        pass
    
    @staticmethod
    def time():
        """Текущее время (имитация)"""
        import time
        return time.time()
    
    @staticmethod
    def frameTime():
        """Время кадра (заглушка)"""
        return 0.033  # ~30 FPS
    
    @staticmethod
    def fps():
        """Количество кадров в секунду (заглушка)"""
        return 30


# Экспортируем основные имена так, как их ожидает оригинальный код
Entity = MockEntity
entity = BigWorld.entity
entities = BigWorld.entities
createEntity = BigWorld.createEntity
destroyEntity = BigWorld.destroyEntity
loadTerrain = BigWorld.loadTerrain
addSpaceGeometryMapping = BigWorld.addSpaceGeometryMapping
getSpaceID = BigWorld.getSpaceID
getSpaceCamera = BigWorld.getSpaceCamera
newPlayerAvatar = BigWorld.newPlayerAvatar
disconnect = BigWorld.disconnect
reconnect = BigWorld.reconnect
isReconnecting = BigWorld.isReconnecting
callback = BigWorld.callback
cancelCallback = BigWorld.cancelCallback
time = BigWorld.time
frameTime = BigWorld.frameTime
fps = BigWorld.fps

# Специальные переменные которые могут использоваться
player = None
camera = None

print "[BigWorld.Mock] Module initialized successfully (OFFLINE MODE)"
