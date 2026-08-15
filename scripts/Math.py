# -*- coding: utf-8 -*-
"""
ЗАГЛУШКА ДЛЯ МОДУЛЯ Math
Отвечает за математические операции и векторы
В офлайн-режиме предоставляет простые реализации векторов и матриц
"""

import math as _math

class Vector2:
    """Простой 2D вектор"""
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __div__(self, scalar):
        if scalar == 0:
            return Vector2(0, 0)
        return Vector2(self.x / scalar, self.y / scalar)
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def length(self):
        return _math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalized(self):
        l = self.length()
        if l == 0:
            return Vector2(0, 0)
        return Vector2(self.x / l, self.y / l)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def __repr__(self):
        return "Vector2(%f, %f)" % (self.x, self.y)


class Vector3:
    """Простой 3D вектор"""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __div__(self, scalar):
        if scalar == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
    
    def length(self):
        return _math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalized(self):
        l = self.length()
        if l == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / l, self.y / l, self.z / l)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def __repr__(self):
        return "Vector3(%f, %f, %f)" % (self.x, self.y, self.z)
    
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


class Vector4:
    """Простой 4D вектор"""
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)
    
    def __repr__(self):
        return "Vector4(%f, %f, %f, %f)" % (self.x, self.y, self.z, self.w)


class Matrix3:
    """Простая 3x3 матрица"""
    def __init__(self):
        self.data = [1, 0, 0, 0, 1, 0, 0, 0, 1]  # Identity
    
    def setRotateYPR(self, yaw, pitch, roll):
        """Установить вращение по Euler углам"""
        # Упрощенная реализация
        pass
    
    def __mul__(self, vector):
        if isinstance(vector, Vector3):
            # Упрощенное умножение
            return Vector3(vector.x, vector.y, vector.z)
        return self


class Matrix4:
    """Простая 4x4 матрица"""
    def __init__(self):
        self.data = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]  # Identity
    
    def setTranslate(self, x, y, z):
        """Установить трансляцию"""
        self.data[12] = x
        self.data[13] = y
        self.data[14] = z
    
    def setRotateYPR(self, yaw, pitch, roll):
        """Установить вращение"""
        pass


def Vector2Tuple(v):
    """Конвертировать в кортеж"""
    if hasattr(v, '__iter__'):
        return tuple(v)
    return (v.x, v.y)


def Vector3Tuple(v):
    """Конвертировать в кортеж"""
    if hasattr(v, '__iter__'):
        return tuple(v)
    return (v.x, v.y, v.z)


def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    """Проверка близости чисел"""
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def sqrt(x):
    return _math.sqrt(x)


def sin(x):
    return _math.sin(x)


def cos(x):
    return _math.cos(x)


def tan(x):
    return _math.tan(x)


def atan2(y, x):
    return _math.atan2(y, x)


def degrees(x):
    return _math.degrees(x)


def radians(x):
    return _math.radians(x)


# Константы
PI = _math.pi
HALF_PI = _math.pi / 2.0
TWO_PI = _math.pi * 2.0
DEG2RAD = _math.pi / 180.0
RAD2DEG = 180.0 / _math.pi

print "[Math.Mock] Module initialized successfully (OFFLINE MODE)"
