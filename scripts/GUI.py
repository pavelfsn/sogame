# -*- coding: utf-8 -*-
"""
ЗАГЛУШКА ДЛЯ МОДУЛЯ GUI
Отвечает за графический интерфейс пользователя
В офлайн-режиме предоставляет базовую структуру без реальной отрисовки
"""

import sys

class GUI:
    """Заглушка для GUI системы"""
    
    _windows = {}
    _next_id = 1
    
    @staticmethod
    def createWindow(window_type, name='', **kwargs):
        """Создать окно"""
        print "[GUI.Mock] Creating window:", window_type, name
        window_id = GUI._next_id
        GUI._next_id += 1
        
        class MockWindow:
            def __init__(self, wid, wtype, wname):
                self.id = wid
                self.type = wtype
                self.name = wname
                self.visible = True
                self.enabled = True
                self.position = (0, 0)
                self.size = (100, 100)
                self.children = []
                self.text = ''
                self.callback = None
            
            def destroy(self):
                self.visible = False
                print "[GUI.Mock] Window destroyed:", self.name
            
            def setVisible(self, visible):
                self.visible = visible
                print "[GUI.Mock] Window", self.name, "visible:", visible
            
            def isVisible(self):
                return self.visible
            
            def setEnabled(self, enabled):
                self.enabled = enabled
            
            def isEnabled(self):
                return self.enabled
            
            def setPosition(self, x, y):
                self.position = (x, y)
            
            def getPosition(self):
                return self.position
            
            def setSize(self, width, height):
                self.size = (width, height)
            
            def getSize(self):
                return self.size
            
            def setText(self, text):
                self.text = text
            
            def getText(self):
                return self.text
            
            def setCallback(self, callback):
                self.callback = callback
            
            def attachChild(self, child):
                self.children.append(child)
            
            def detachChild(self, child):
                if child in self.children:
                    self.children.remove(child)
            
            def clearChildren(self):
                self.children = []
            
            def findWidget(self, name):
                # Поиск среди детей
                for child in self.children:
                    if hasattr(child, 'name') and child.name == name:
                        return child
                return None
        
        window = MockWindow(window_id, window_type, name)
        GUI._windows[window_id] = window
        return window
    
    @staticmethod
    def destroyWindow(window):
        """Уничтожить окно"""
        if window and hasattr(window, 'id'):
            if window.id in GUI._windows:
                del GUI._windows[window.id]
            if hasattr(window, 'destroy'):
                window.destroy()
        print "[GUI.Mock] Window destroyed"
    
    @staticmethod
    def getWindow(id):
        """Получить окно по ID"""
        return GUI._windows.get(id, None)
    
    @staticmethod
    def getAllWindows():
        """Получить все окна"""
        return GUI._windows.values()
    
    @staticmethod
    def clearAll():
        """Очистить все окна"""
        for window in GUI._windows.values():
            if hasattr(window, 'destroy'):
                window.destroy()
        GUI._windows.clear()
        print "[GUI.Mock] All windows cleared"
    
    @staticmethod
    def loadLayout(xml_path):
        """Загрузить раскладку из XML"""
        print "[GUI.Mock] Loading layout:", xml_path
        return GUI.createWindow('Layout', xml_path)
    
    @staticmethod
    def setActiveWindow(window):
        """Установить активное окно"""
        print "[GUI.Mock] Active window:", getattr(window, 'name', 'Unknown')
    
    @staticmethod
    def getActiveWindow():
        """Получить активное окно"""
        return None
    
    @staticmethod
    def setCursor(cursor_type):
        """Установить курсор"""
        pass
    
    @staticmethod
    def showMessage(title, message, buttons=None):
        """Показать сообщение"""
        print "[GUI.Mock] Message:", title, "-", message
        return True


# Классы для конкретных виджетов
class Button:
    """Класс кнопки"""
    def __init__(self, name=''):
        self.name = name
        self.text = ''
        self.enabled = True
        self.visible = True
        self.callback = None
    
    def setText(self, text):
        self.text = text
    
    def setEnabled(self, enabled):
        self.enabled = enabled
    
    def setCallback(self, callback):
        self.callback = callback


class Label:
    """Класс метки"""
    def __init__(self, name=''):
        self.name = name
        self.text = ''
        self.visible = True
    
    def setText(self, text):
        self.text = text
    
    def getText(self):
        return self.text


class EditBox:
    """Класс поля ввода"""
    def __init__(self, name=''):
        self.name = name
        self.text = ''
        self.max_length = 256
        self.enabled = True
    
    def setText(self, text):
        self.text = text[:self.max_length]
    
    def getText(self):
        return self.text


class ListBox:
    """Класс списка"""
    def __init__(self, name=''):
        self.name = name
        self.items = []
    
    def addItem(self, item):
        self.items.append(item)
    
    def removeItem(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)
    
    def clear(self):
        self.items = []
    
    def getSelectedItem(self):
        return None


class ProgressBar:
    """Класс прогресс-бара"""
    def __init__(self, name=''):
        self.name = name
        self.value = 0.0
        self.min = 0.0
        self.max = 1.0
    
    def setValue(self, value):
        self.value = max(self.min, min(self.max, value))
    
    def getValue(self):
        return self.value


# Экспортируем функции как модуль
createWindow = GUI.createWindow
destroyWindow = GUI.destroyWindow
getWindow = GUI.getWindow
getAllWindows = GUI.getAllWindows
clearAll = GUI.clearAll
loadLayout = GUI.loadLayout
setActiveWindow = GUI.setActiveWindow
getActiveWindow = GUI.getActiveWindow
setCursor = GUI.setCursor
showMessage = GUI.showMessage

print "[GUI.Mock] Module initialized successfully (OFFLINE MODE)"
