# Embedded file name: scripts/client/PlayerAvatar.py
from Avatar import Avatar
from PlayerAvatarForSoClanScreen import PlayerAvatarForSoClanScreen
import BigWorld
import Math
from Math import Vector3
import BWPersonality
from Helpers import Listener as ListenerHelper

class PlayerAvatar(Avatar, PlayerAvatarForSoClanScreen):
    """
    Основной класс игрока в мире игры.
    Наследуется от Avatar (базовая сущность аватара) 
    и PlayerAvatarForSoClanScreen (функционал кланового экрана).
    """
    
    # Статические атрибуты для доступа из других модулей
    CanTurnOnSpotLight = True
    
    def __init__(self):
        Avatar.__init__(self)
        PlayerAvatarForSoClanScreen.__init__(self) if hasattr(PlayerAvatarForSoClanScreen, '__init__') else None
        
        # Инициализация дополнительных атрибутов
        self.selectedBase = None
        self.selectedStaff = None
        self.basesData = []
        self.clanRoster = {}
        self.clanName = ''
        
        # Слушатели событий
        self._listeners = ListenerHelper.Listenable()
        
    def onEnterWorld(self, pre=None):
        """Вызывается при входе аватара в мир"""
        Avatar.onEnterWorld(self, pre)
        # Уведомляем GUI о загрузке аватара игрока
        try:
            if hasattr(BWPersonality, 'GUICore') and BWPersonality.GUICore:
                BWPersonality.GUICore.onPlayerAvatarLoaded()
        except Exception as e:
            print "PlayerAvatar.onEnterWorld: GUI notification error:", e
    
    def onLeaveWorld(self):
        """Вызывается при выходе аватара из мира"""
        try:
            if hasattr(BWPersonality, 'GUICore') and BWPersonality.GUICore:
                BWPersonality.GUICore.onPlayerAvatarUnloaded()
        except Exception as e:
            print "PlayerAvatar.onLeaveWorld: GUI notification error:", e
        Avatar.onLeaveWorld(self) if hasattr(Avatar, 'onLeaveWorld') else None
    
    def handleInput(self, key, isDown):
        """Обработка ввода игрока"""
        return False
    
    def sendMessage(self, message):
        """Отправка сообщения на сервер"""
        if hasattr(self, 'cell') and self.cell:
            self.cell.sendMessage(message)
    
    # Методы для работы с фонариком
    def InitSpotLight(self, force=False):
        """Инициализация фонарика"""
        if not hasattr(self, 'avatarFlashlight'):
            self.setupFlashlight()
        if force or PlayerAvatar.CanTurnOnSpotLight:
            self.onSwitchSpotLight(True)
    
    def onSwitchSpotLight(self, lightState):
        """Переключение состояния фонарика"""
        if PlayerAvatar.CanTurnOnSpotLight:
            Avatar.onSwitchSpotLight(self, lightState)
    
    # Методы для клановой системы (реализация заглушек)
    def getNamedRank(self, name):
        return PlayerAvatarForSoClanScreen.getNamedRank(self, name) if hasattr(PlayerAvatarForSoClanScreen, 'getNamedRank') else None
    
    def getOwnClanRank(self):
        return PlayerAvatarForSoClanScreen.getOwnClanRank(self) if hasattr(PlayerAvatarForSoClanScreen, 'getOwnClanRank') else None
    
    def checkOwnClanRight(self, rightNum):
        return PlayerAvatarForSoClanScreen.checkOwnClanRight(self, rightNum) if hasattr(PlayerAvatarForSoClanScreen, 'checkOwnClanRight') else False
    
    def updateClanRights(self):
        if hasattr(PlayerAvatarForSoClanScreen, 'updateClanRights'):
            PlayerAvatarForSoClanScreen.updateClanRights(self)
    
    def getRightsListForNamedRank(self, name):
        return PlayerAvatarForSoClanScreen.getRightsListForNamedRank(self, name) if hasattr(PlayerAvatarForSoClanScreen, 'getRightsListForNamedRank') else []
    
    # Методы для работы с базой клана
    def findBaseByName(self, name):
        return PlayerAvatarForSoClanScreen.findBaseByName(self, name) if hasattr(PlayerAvatarForSoClanScreen, 'findBaseByName') else None
    
    def onBaseSelected(self, baseName):
        if hasattr(PlayerAvatarForSoClanScreen, 'onBaseSelected'):
            PlayerAvatarForSoClanScreen.onBaseSelected(self, baseName)
    
    def findBaseNPCBySpotName(self, npcSpotName):
        return PlayerAvatarForSoClanScreen.findBaseNPCBySpotName(self, npcSpotName) if hasattr(PlayerAvatarForSoClanScreen, 'findBaseNPCBySpotName') else None
    
    def onBaseNPCSelected(self, npcSpotName):
        if hasattr(PlayerAvatarForSoClanScreen, 'onBaseNPCSelected'):
            PlayerAvatarForSoClanScreen.onBaseNPCSelected(self, npcSpotName)
    
    # Обновления данных клана
    def clanRosterUpdate(self, roster):
        if hasattr(PlayerAvatarForSoClanScreen, 'clanRosterUpdate'):
            PlayerAvatarForSoClanScreen.clanRosterUpdate(self, roster)
    
    def clanMemberRosterUpdate(self, member):
        if hasattr(PlayerAvatarForSoClanScreen, 'clanMemberRosterUpdate'):
            PlayerAvatarForSoClanScreen.clanMemberRosterUpdate(self, member)
    
    def clanRanksUpdate(self, ranks, self_id):
        if hasattr(PlayerAvatarForSoClanScreen, 'clanRanksUpdate'):
            PlayerAvatarForSoClanScreen.clanRanksUpdate(self, ranks, self_id)
    
    def clanBasesUpdate(self, basesData):
        if hasattr(PlayerAvatarForSoClanScreen, 'clanBasesUpdate'):
            PlayerAvatarForSoClanScreen.clanBasesUpdate(self, basesData)
    
    def clanEvent(self, event, data):
        if hasattr(PlayerAvatarForSoClanScreen, 'clanEvent'):
            PlayerAvatarForSoClanScreen.clanEvent(self, event, data)
    
    # Позиция и движение
    def getClientPosition(self):
        """Получение позиции клиента"""
        if hasattr(self, 'position'):
            return self.position
        return Vector3(0, 0, 0)
    
    def isOnGround(self):
        """Проверка, находится ли игрок на земле"""
        if hasattr(self, 'isOnGround'):
            return Avatar.isOnGround(self)
        return True
    
    # Здоровье и состояние
    def isDead(self):
        """Проверка смерти игрока"""
        return getattr(self, 'dead', False)
    
    def setHealth(self, health):
        """Установка здоровья"""
        if hasattr(self, 'health') and health >= 0:
            self.health = health
    
    # Инвентарь и предметы
    def getCurrentItemID(self):
        """Получение ID текущего предмета"""
        return getattr(self, 'ActiveItemID', 0)
    
    def getCurrentItemType(self):
        """Получение типа текущего предмета"""
        return getattr(self, 'ActiveItemType', 0)
    
    # Анимации
    def playAction(self, actionName, loop=False):
        """Воспроизведение анимации"""
        if hasattr(self, 'model') and self.model:
            try:
                if loop:
                    self.model.play(actionName, loop=True)
                else:
                    self.model.play(actionName)
            except Exception as e:
                print "PlayerAvatar.playAction error:", e
    
    def stopCurrentAnimation(self):
        """Остановка текущей анимации"""
        if hasattr(self, 'model') and self.model:
            try:
                self.model.stop()
            except:
                pass
    
    # Камера
    def setCameraMode(self, mode):
        """Установка режима камеры"""
        try:
            if hasattr(BigWorld, 'camera'):
                BigWorld.camera().mode = mode
        except Exception as e:
            print "PlayerAvatar.setCameraMode error:", e
    
    # Сеть и синхронизация
    def broadcastClientEvent(self, eventName, *args):
        """Трансляция клиентского события"""
        try:
            if hasattr(self, 'cell') and self.cell:
                self.cell.broadcastClientEvent(eventName, *args)
        except Exception as e:
            print "PlayerAvatar.broadcastClientEvent error:", e
    
    # Утилиты
    def getName(self):
        """Получение имени игрока"""
        return getattr(self, 'name', 'Unknown')
    
    def getID(self):
        """Получение ID игрока"""
        return getattr(self, 'id', 0)
    
    def isLocalPlayer(self):
        """Проверка, является ли аватар локальным игроком"""
        return True
    
    # Оффлайн-режим (заглушки для стабильности)
    def requestRespawn(self):
        """Запрос возрождения (оффлайн-заглушка)"""
        print "PlayerAvatar: Respawn requested (offline mode)"
        self.setHealth(100)
        self.dead = False
    
    def requestTeleport(self, x, y, z):
        """Запрос телепортации (оффлайн-заглушка)"""
        print "PlayerAvatar: Teleport to (%.2f, %.2f, %.2f) requested (offline mode)" % (x, y, z)
        if hasattr(self, 'position'):
            self.position = Vector3(x, y, z)
    
    def requestItemSpawn(self, itemTypeID):
        """Запрос создания предмета (оффлайн-заглушка)"""
        print "PlayerAvatar: Item spawn requested for type", itemTypeID
        self.spawn_new_item(itemTypeID)
    
    # Обработка урона (оффлайн-режим)
    def takeDamage(self, damage, damageType='physical', attacker=None):
        """Получение урона"""
        if hasattr(self, 'health'):
            self.health = max(0, self.health - damage)
            if self.health <= 0:
                self.dead = True
                print "PlayerAvatar: Player died from", damage, "damage"
        return self.health
    
    # Методы для совместимости
    def cell(self):
        """Возвращает cell объект или None в оффлайне"""
        return getattr(self, '_cell', None)
    
    def base(self):
        """Возвращает base объект или None в оффлайне"""
        return getattr(self, '_base', None)
