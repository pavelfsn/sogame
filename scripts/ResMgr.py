# -*- coding: utf-8 -*-
"""
ЗАГЛУШКА ДЛЯ МОДУЛЯ ResMgr
Отвечает за загрузку ресурсов (XML, текстуры, конфиги)
В офлайн-режиме возвращает пустые данные или заглушки
"""

import os
import sys

class ResMgr:
    """Заглушка для менеджера ресурсов"""
    
    _data_path = None
    
    @staticmethod
    def setDataPath(path):
        """Установить путь к данным"""
        ResMgr._data_path = path
        print "[ResMgr.Mock] Data path set to:", path
    
    @staticmethod
    def open(filename):
        """Открыть файл ресурса"""
        # Пытаемся найти файл в реальной файловой системе
        if ResMgr._data_path:
            full_path = os.path.join(ResMgr._data_path, filename)
        else:
            full_path = filename
        
        # Нормализуем пути (заменяем слеши)
        full_path = full_path.replace('/', os.sep).replace('\\', os.sep)
        
        if os.path.exists(full_path):
            print "[ResMgr.Mock] Opening file:", full_path
            try:
                return open(full_path, 'rb')
            except Exception as e:
                print "[ResMgr.Mock] Failed to open:", e
                return None
        else:
            print "[ResMgr.Mock] File not found (returning None):", filename
            return None
    
    @staticmethod
    def findFiles(pattern):
        """Найти файлы по шаблону (упрощенно)"""
        print "[ResMgr.Mock] Finding files:", pattern
        # В реальной реализации здесь должен быть glob
        return []
    
    @staticmethod
    def listDirectory(path):
        """Список файлов в директории"""
        if ResMgr._data_path:
            full_path = os.path.join(ResMgr._data_path, path)
        else:
            full_path = path
        
        full_path = full_path.replace('/', os.sep).replace('\\', os.sep)
        
        if os.path.isdir(full_path):
            print "[ResMgr.Mock] Listing directory:", full_path
            return os.listdir(full_path)
        else:
            print "[ResMgr.Mock] Directory not found:", path
            return []
    
    @staticmethod
    def exists(filename):
        """Проверить существование файла"""
        if ResMgr._data_path:
            full_path = os.path.join(ResMgr._data_path, filename)
        else:
            full_path = filename
        
        full_path = full_path.replace('/', os.sep).replace('\\', os.sep)
        exists = os.path.exists(full_path)
        
        if not exists:
            print "[ResMgr.Mock] File does not exist:", filename
        
        return exists
    
    @staticmethod
    def isFile(filename):
        """Проверить является ли файл файлом (а не директорией)"""
        if ResMgr._data_path:
            full_path = os.path.join(ResMgr._data_path, filename)
        else:
            full_path = filename
        
        full_path = full_path.replace('/', os.sep).replace('\\', os.sep)
        return os.path.isfile(full_path)
    
    @staticmethod
    def isDir(filename):
        """Проверить является ли файл директорией"""
        if ResMgr._data_path:
            full_path = os.path.join(ResMgr._data_path, filename)
        else:
            full_path = filename
        
        full_path = full_path.replace('/', os.sep).replace('\\', os.sep)
        return os.path.isdir(full_path)
    
    @staticmethod
    def xmlOpen(filename):
        """Открыть XML файл (возвращает файл или None)"""
        return ResMgr.open(filename)
    
    @staticmethod
    def getSection(filename):
        """Загрузить секцию XML (упрощенно)"""
        print "[ResMgr.Mock] Getting section from:", filename
        # Возвращаем пустой объект-заглушку
        class MockSection:
            def readInt(self, key, default=0): return default
            def readFloat(self, key, default=0.0): return default
            def readString(self, key, default=''): return default
            def readBool(self, key, default=False): return default
            def __getitem__(self, key): return self
            def __contains__(self, key): return False
            def values(): return []
            def keys(): return []
            def items(): return []
        return MockSection()


# Экспортируем функции как модуль
open = ResMgr.open
findFiles = ResMgr.findFiles
listDirectory = ResMgr.listDirectory
exists = ResMgr.exists
isFile = ResMgr.isFile
isDir = ResMgr.isDir
xmlOpen = ResMgr.xmlOpen
getSection = ResMgr.getSection
setDataPath = ResMgr.setDataPath

print "[ResMgr.Mock] Module initialized successfully (OFFLINE MODE)"
