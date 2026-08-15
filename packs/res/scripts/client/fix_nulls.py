# -*- coding: utf-8 -*-
with open('BWPersonality.py', 'rb') as f:
    data = f.read()

# Удаляем все нулевые байты
data = data.replace(b'\x00', b'')

with open('BWPersonality_fixed.py', 'wb') as f:
    f.write(data)

print("Файл очищен. Используйте BWPersonality_fixed.py")