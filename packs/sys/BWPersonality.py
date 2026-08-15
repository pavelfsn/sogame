# Embedded file name: BWPersonality.py
from collections import namedtuple
import math
import BigWorld
import GUI
import Math
g_compass_text = None
g_compass_ticks = None
g_compass_degrees = None
g_compass_arrow = None
g_coords_gui = None
g_mod_coords_visible = True
g_mod_initialized = False
g_admin_text_gui = None
g_admin_visible = False
from Keys import *
ADMIN_PRESETS = {KEY_NUMPAD1: (u'AK-105', 'wpn_ak105'),
 KEY_NUMPAD2: (u'M4A1', 'wpn_m4a1'),
 KEY_NUMPAD3: (u'Ammo 5.45', 'ammo_545x39'),
 KEY_NUMPAD4: (u'Ammo 5.56', 'ammo_556x45'),
 KEY_NUMPAD5: (u'Medkit', 'medkit_sci'),
 KEY_NUMPAD6: (u'Bandage', 'bandage'),
 KEY_NUMPAD7: (u'Exo Armor', 'armor_exo'),
 KEY_NUMPAD8: (u'Artifact', 'af_fireball'),
 KEY_NUMPAD9: (u'Bolt', 'bolt')}
import os
import hashlib
import re
import traceback
import sys
import inspect
from CallbackHelpers import callback
from bwdebug import *
import ResMgr
import FX
from time import time
from Helpers import PyGUI
from gui_const import CHAR_PICKER, CHAR_MAKER
from gui_jokes import inputBox, msgBox, askUserYesNo
import msgbox_templates
import validators
__import__('__main__').PyGUI = PyGUI
import soGUI
__import__('__main__').soGUI = soGUI
import soGUI.soProgressBars as soProgressBars
from soGUI.soQueueScreen import soQueueScreen
from soGUI.soGUICore import soGUICore
from gui_const import MESSAGEBOX
from utils_bw import get_classname
import sounds
import gui_jokes
stalkerVersion = u'v.0.8.4014'
FX.Events.PlaySound.set_playsound_function(sounds.playSound)
from Localization import lc
from Helpers import Listener
from Helpers.BWCoroutine import *
from Helpers import BWKeyBindings
import Keys
import random
import CameraNode
import Account
import PostProcessing
import Bloom
from Avatar import PlayerAvatar
from Settings import Settings
from Music import Music
from Cache import Cache
from utils_bw import wait
from soGUI.soFriend_BlackList import FriendList
import AccountConst
from Math import Vector3
import json
import codecs
from Config import SpacesConfig
from Config import WeatherConfig
from random import choice

def mod_init_gui():
    """\xd0\x98\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb8\xd0\xb0\xd0\xbb\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f GUI \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xbc\xd0\xbe\xd0\xb4\xd0\xb0 (\xd0\xba\xd0\xbe\xd0\xbc\xd0\xbf\xd0\xb0\xd1\x81 + \xd0\xba\xd0\xbe\xd0\xbe\xd1\x80\xd0\xb4\xd0\xb8\xd0\xbd\xd0\xb0\xd1\x82\xd1\x8b + \xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xba\xd0\xb0)"""
    global g_admin_visible
    global g_mod_initialized
    global g_compass_degrees
    global g_admin_text_gui
    global g_coords_gui
    global g_mod_coords_visible
    global g_compass_text
    if g_mod_initialized:
        return
    try:
        g_coords_gui = GUI.Text('')
        g_coords_gui.font = 'default_medium.font'
        g_coords_gui.colour = (255, 255, 0, 255)
        g_coords_gui.position = (-0.95, 0.9, 1.0)
        g_coords_gui.visible = g_mod_coords_visible
        GUI.addRoot(g_coords_gui)
        g_compass_text = GUI.Text(u'N')
        g_compass_text.font = 'default_large.font'
        g_compass_text.colour = (255, 255, 255, 255)
        g_compass_text.position = (0.0, 0.85, 1.0)
        g_compass_text.horizontalAnchor = 'CENTER'
        g_compass_text.verticalAnchor = 'TOP'
        g_compass_text.visible = True
        GUI.addRoot(g_compass_text)
        g_compass_degrees = GUI.Text(u'0\xb0')
        g_compass_degrees.font = 'default_small.font'
        g_compass_degrees.colour = (200, 200, 200, 255)
        g_compass_degrees.position = (0.0, 0.8, 1.0)
        g_compass_degrees.horizontalAnchor = 'CENTER'
        g_compass_degrees.verticalAnchor = 'TOP'
        g_compass_degrees.visible = True
        GUI.addRoot(g_compass_degrees)
        g_admin_text_gui = GUI.Text(u'')
        g_admin_text_gui.font = 'default_medium.font'
        g_admin_text_gui.colour = (0, 255, 0, 255)
        g_admin_text_gui.position = (0.6, 0.9, 1.0)
        g_admin_text_gui.visible = g_admin_visible
        GUI.addRoot(g_admin_text_gui)
        g_mod_initialized = True
        print '[MOD] GUI initialized successfully!'
    except Exception as e:
        print '[MOD] Error initializing GUI:', e
        traceback.print_exc()


def mod_destroy_gui():
    """\xd0\xa3\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 GUI \xd0\xbf\xd1\x80\xd0\xb8 \xd0\xbe\xd1\x82\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb8"""
    global g_mod_initialized
    global g_compass_degrees
    global g_admin_text_gui
    global g_coords_gui
    global g_compass_text
    try:
        if g_coords_gui:
            GUI.delRoot(g_coords_gui)
            g_coords_gui = None
        if g_compass_text:
            GUI.delRoot(g_compass_text)
            g_compass_text = None
        if g_compass_degrees:
            GUI.delRoot(g_compass_degrees)
            g_compass_degrees = None
        if g_admin_text_gui:
            GUI.delRoot(g_admin_text_gui)
            g_admin_text_gui = None
        g_mod_initialized = False
        print '[MOD] GUI destroyed'
    except:
        pass

    return


def mod_update():
    """\xd0\x9e\xd1\x81\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbd\xd0\xbe\xd0\xb9 \xd1\x86\xd0\xb8\xd0\xba\xd0\xbb \xd0\xbe\xd0\xb1\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd0\xbc\xd0\xbe\xd0\xb4\xd0\xb0"""
    try:
        if not g_mod_initialized:
            mod_init_gui()
        player = BigWorld.player()
        if player is None or not isinstance(player, PlayerAvatar):
            BigWorld.callback(0.1, mod_update)
            return
        if not hasattr(player, 'position'):
            BigWorld.callback(0.1, mod_update)
            return
        if g_coords_gui and g_mod_coords_visible:
            pos = player.position
            g_coords_gui.text = u'X: %.1f  Y: %.1f  Z: %.1f' % (pos.x, pos.y, pos.z)
        if g_compass_text and hasattr(player, 'yaw'):
            yaw_deg = math.degrees(player.yaw) % 360
            if 337.5 <= yaw_deg or yaw_deg < 22.5:
                direction = u'N'
            elif 22.5 <= yaw_deg < 67.5:
                direction = u'NE'
            elif 67.5 <= yaw_deg < 112.5:
                direction = u'E'
            elif 112.5 <= yaw_deg < 157.5:
                direction = u'SE'
            elif 157.5 <= yaw_deg < 202.5:
                direction = u'S'
            elif 202.5 <= yaw_deg < 247.5:
                direction = u'SW'
            elif 247.5 <= yaw_deg < 292.5:
                direction = u'W'
            else:
                direction = u'NW'
            g_compass_text.text = direction
            if g_compass_degrees:
                g_compass_degrees.text = u'%d\xb0' % int(yaw_deg)
        if g_admin_text_gui and g_admin_visible:
            admin_text = u'=== ADMIN MENU ===\n'
            for key, (name, item_id) in ADMIN_PRESETS.items():
                key_name = Keys.keyToString(key)
                admin_text += u'%s: %s\n' % (key_name, name)

            g_admin_text_gui.text = admin_text
    except Exception as e:
        print '[MOD] Update error:', e

    BigWorld.callback(0.1, mod_update)
    return


def mod_toggle_coords():
    """\xd0\x9f\xd0\xb5\xd1\x80\xd0\xb5\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb8\xd0\xbc\xd0\xbe\xd1\x81\xd1\x82\xd0\xb8 \xd0\xba\xd0\xbe\xd0\xbe\xd1\x80\xd0\xb4\xd0\xb8\xd0\xbd\xd0\xb0\xd1\x82 (F10)"""
    global g_mod_coords_visible
    g_mod_coords_visible = not g_mod_coords_visible
    if g_coords_gui:
        g_coords_gui.visible = g_mod_coords_visible
    print '[MOD] Coordinates:', 'ON' if g_mod_coords_visible else 'OFF'


def mod_toggle_admin():
    """\xd0\x9f\xd0\xb5\xd1\x80\xd0\xb5\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd-\xd0\xbf\xd0\xb0\xd0\xbd\xd0\xb5\xd0\xbb\xd0\xb8 (F6)"""
    global g_admin_visible
    g_admin_visible = not g_admin_visible
    if g_admin_text_gui:
        g_admin_text_gui.visible = g_admin_visible
    print '[MOD] Admin panel:', 'ON' if g_admin_visible else 'OFF'


def mod_give_item(item_id):
    """\xd0\x92\xd1\x8b\xd0\xb4\xd0\xb0\xd1\x82\xd1\x8c \xd0\xbf\xd1\x80\xd0\xb5\xd0\xb4\xd0\xbc\xd0\xb5\xd1\x82 \xd0\xb8\xd0\xb3\xd1\x80\xd0\xbe\xd0\xba\xd1\x83 (\xd0\xb4\xd0\xbb\xd1\x8f \xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xba\xd0\xb8)"""
    try:
        player = BigWorld.player()
        if player and hasattr(player, 'cell'):
            print '[MOD] Item spawn requested:', item_id
    except Exception as e:
        print '[MOD] Error spawning item:', e


global g_compass_arrow ## Warning: Unused globalglobal g_compass_ticks ## Warning: Unused global