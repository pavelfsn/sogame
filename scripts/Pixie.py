# -*- coding: utf-8 -*-
"""
ЗАГЛУШКА ДЛЯ МОДУЛЯ Pixie
Отвечает за систему частиц и визуальные эффекты
В офлайн-режиме просто логирует вызовы без реальной отрисовки
"""

import sys

class Pixie:
    """Заглушка для системы частиц Pixie"""
    
    _effects = {}
    _next_id = 1
    
    @staticmethod
    def create(xml_path):
        """Создать эффект частиц"""
        print "[Pixie.Mock] Creating particle effect:", xml_path
        # Возвращаем объект-заглушку
        effect_id = Pixie._next_id
        Pixie._next_id += 1
        
        class MockEffect:
            def __init__(self, eid):
                self.id = eid
                self.position = [0, 0, 0]
                self.active = True
            
            def setPosition(self, pos):
                self.position = list(pos)
            
            def getPosition(self):
                return tuple(self.position)
            
            def setActive(self, active):
                self.active = active
            
            def isActive(self):
                return self.active
            
            def destroy(self):
                self.active = False
                print "[Pixie.Mock] Effect destroyed:", self.id
        
        effect = MockEffect(effect_id)
        Pixie._effects[effect_id] = effect
        return effect
    
    @staticmethod
    def destroy(effect):
        """Уничтожить эффект"""
        if effect and hasattr(effect, 'id'):
            if effect.id in Pixie._effects:
                del Pixie._effects[effect.id]
            if hasattr(effect, 'destroy'):
                effect.destroy()
        print "[Pixie.Mock] Effect destroyed"
    
    @staticmethod
    def getEffect(id):
        """Получить эффект по ID"""
        return Pixie._effects.get(id, None)
    
    @staticmethod
    def getAllEffects():
        """Получить все эффекты"""
        return Pixie._effects.values()
    
    @staticmethod
    def clearAll():
        """Очистить все эффекты"""
        for effect in Pixie._effects.values():
            if hasattr(effect, 'destroy'):
                effect.destroy()
        Pixie._effects.clear()
        print "[Pixie.Mock] All effects cleared"
    
    @staticmethod
    def setGlobalScale(scale):
        """Установить глобальный масштаб эффектов"""
        print "[Pixie.Mock] Global scale set to:", scale
    
    @staticmethod
    def getGlobalScale():
        """Получить глобальный масштаб"""
        return 1.0
    
    @staticmethod
    def setEnabled(enabled):
        """Включить/выключить систему частиц"""
        print "[Pixie.Mock] Particles enabled:", enabled
    
    @staticmethod
    def isEnabled():
        """Проверка включена ли система"""
        return True


# Экспортируем функции как модуль
create = Pixie.create
destroy = Pixie.destroy
getEffect = Pixie.getEffect
getAllEffects = Pixie.getAllEffects
clearAll = Pixie.clearAll
setGlobalScale = Pixie.setGlobalScale
getGlobalScale = Pixie.getGlobalScale
setEnabled = Pixie.setEnabled
isEnabled = Pixie.isEnabled

print "[Pixie.Mock] Module initialized successfully (OFFLINE MODE)"
