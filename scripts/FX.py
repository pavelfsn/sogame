# -*- coding: utf-8 -*-
"""
ЗАГЛУШКА ДЛЯ МОДУЛЯ FX
Отвечает за визуальные эффекты (выстрелы, взрывы, попадания)
В офлайн-режиме просто логирует вызовы без реальной отрисовки
"""

import sys

class FX:
    """Заглушка для системы эффектов"""
    
    _effects = {}
    _next_id = 1
    
    @staticmethod
    def createEffect(effect_type, position, direction=None, **kwargs):
        """Создать эффект"""
        print "[FX.Mock] Creating effect:", effect_type, "at", position
        effect_id = FX._next_id
        FX._next_id += 1
        
        class MockEffect:
            def __init__(self, eid, etype):
                self.id = eid
                self.type = etype
                self.position = position
                self.active = True
            
            def stop(self):
                self.active = False
                print "[FX.Mock] Effect stopped:", self.id
            
            def isPlaying(self):
                return self.active
        
        effect = MockEffect(effect_id, effect_type)
        FX._effects[effect_id] = effect
        return effect
    
    @staticmethod
    def stopEffect(effect):
        """Остановить эффект"""
        if effect and hasattr(effect, 'id'):
            if effect.id in FX._effects:
                del FX._effects[effect.id]
            if hasattr(effect, 'stop'):
                effect.stop()
        print "[FX.Mock] Effect stopped"
    
    @staticmethod
    def playSound(sound_path, position=None, volume=1.0):
        """Воспроизвести звук (заглушка)"""
        print "[FX.Mock] Playing sound:", sound_path, "volume:", volume
        return True
    
    @staticmethod
    def stopSound(sound_id):
        """Остановить звук"""
        print "[FX.Mock] Stopping sound:", sound_id
    
    @staticmethod
    def setVolume(volume):
        """Установить громкость"""
        print "[FX.Mock] Volume set to:", volume
    
    @staticmethod
    def getVolume():
        """Получить громкость"""
        return 1.0


# Классы для конкретных эффектов
class Events:
    """Класс для событий эффектов"""
    
    @staticmethod
    def createEvent(event_name, **kwargs):
        """Создать событие эффекта"""
        print "[FX.Events.Mock] Creating event:", event_name
        return {'name': event_name, 'params': kwargs}
    
    @staticmethod
    def playEvent(event, position):
        """Воспроизвести событие"""
        print "[FX.Events.Mock] Playing event:", event['name'], "at", position


class Sound:
    """Класс для звуковых эффектов"""
    
    @staticmethod
    def play(path, position=None, loop=False):
        """Воспроизвести звук"""
        print "[FX.Sound.Mock] Playing:", path
        return True
    
    @staticmethod
    def stop(sound_id):
        """Остановить звук"""
        print "[FX.Sound.Mock] Stopping:", sound_id


# Экспортируем функции как модуль
createEffect = FX.createEffect
stopEffect = FX.stopEffect
playSound = FX.playSound
stopSound = FX.stopSound
setVolume = FX.setVolume
getVolume = FX.getVolume

print "[FX.Mock] Module initialized successfully (OFFLINE MODE)"
