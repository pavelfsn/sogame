# Embedded file name: scripts/client/Account.py
import sys
sys.path.append('scripts/base')
sys.path.append('scripts/cell')
from CallbackHelpers import callback
from CorruptedPacks import CorruptedPacks
from Helpers.Listener import Listenable
from Items import ItemsCatalog
from Localization import lc
import BigWorld
from time import time
import BWPersonality
import Pixie
from Codes import AccountResponses
import datetime
import AvatarDummy
import msgbox_templates
import validators
import VersionSO
import gui_jokes
import base64
from uuid import getnode
import os

class Account(BigWorld.Entity, CorruptedPacks, Listenable):

    def __init__(self):
        print 'Account __init__'
        BigWorld.Entity.__init__(self)
        Listenable.__init__(self)
        self.loadedModels = None
        self.setCharacterList(self.characterList)
        self.dummies = []
        self.characterListReceived = False
        # Исправленная строка для совместимости с Python 2.6
        try:
            self.pers_lighting = Pixie.create('particles/pers_lighting02.xml')
        except Exception as e:
            print 'Warning: Failed to create pers_lighting:', e
            self.pers_lighting = None
        self.queuePosition = None
        return

    def clear_availability_cache(self):
        self.avatar_available_names = []
        self.avatar_taken_names = []

    def __init_module__(self, modulename, data, crc, src):
        print 'Account __init_module__ bypassed'
        getattr(self, src).on_module_init('OK')

    def activatePremiumAccount(self):
        self.base.activatePremiumAccount()

    def updateGoldCost(self, gold):
        BWPersonality.GUICore.goldCost = gold

    def RestoreCharacter(self, name):
        name = name.encode('utf-8')
        self.base.restoreCharacter(name)

    def acOnValidated(self, val, success):
        print val, success

    def failLogon(self, message):
        BigWorld.failLogonCounter = getattr(BigWorld, 'failLogonCounter', 0) + 1
        if BigWorld.failLogonCounter >= 5:
            BigWorld.nologin_until = BigWorld.time() + BigWorld.failLogonCounter * 60.0
        if message in ('not_email_confirmed', 'not_phone_confirmed'):
            gui_jokes.msgBox(u'SERVER', lc('BWPersonality.%s' % message))
        BWPersonality.gpd.sendLowerMessageColored(message, 4294934656L)
        msgID = 2 if message == 'preventive work.' else None
        BWPersonality.game.disconnect(msgID)
        return

    def checkAvatarNameAvailable(self, uid, on_available_result = None):
        current_names_lower = [ ch['name'].lower() for ch in self.characterList ]

        if uid in self.avatar_taken_names or uid in current_names_lower:
            on_available_result(uid, False)
        elif uid in self.avatar_available_names:
            on_available_result(uid, True)
        else:
            self.avatar_name_availability_callback = on_available_result
            self.base.playerCheckAvatarNameAvailability(uid)

    def onAvatarNameAvailability(self, uid, available):
        if available:
            self.avatar_available_names.append(uid)
        else:
            self.avatar_taken_names.append(uid)
        if callable(self.avatar_name_availability_callback):
            self.avatar_name_availability_callback(uid, available)

    def switchMyCharacter(self, cName, cType):
        self.base.switchCharacter(cName, cType)

    def createNewCharacter(self, on_avatar_created_callback = None):
        dummy_char = self._get_dummy()
        if not dummy_char:
            print 'Error: Cannot create new character. AvatarDummy unavailable.'
            if callable(on_avatar_created_callback):
                on_avatar_created_callback(False, -1, "Internal error.")
            return

        avatar_name = dummy_char.name
        response = validators.AvatarName.validate(avatar_name)
        if not response['valid']:
            if callable(on_avatar_created_callback):
                on_avatar_created_callback(False, response['error'][0], response['error'][1])
            return
        self.clear_availability_cache()
        corresp_sections = {ItemsCatalog.HEAD: 'head',
         ItemsCatalog.SHIRT: 'body',
         ItemsCatalog.HANDS: 'hands',
         ItemsCatalog.PANTS: 'legs',
         ItemsCatalog.BOOTS: 'boots'}
        default_models_dict = {}
        for model_part, value in dummy_char.getDefaultModels().iteritems():
            key = corresp_sections[model_part]
            default_models_dict[key] = {'model': 0,
             'tint': 0,
             'type_id': value['head_id'] if model_part == ItemsCatalog.HEAD else value}

        self.__on_avatar_created_callback = on_avatar_created_callback
        self.base.createNewAvatar(avatar_name, default_models_dict)

    def deleteCharacter(self, avatar_name):
        self.characterListReceived = False
        self.base.deleteAvatar(avatar_name)

    def createCharacterCallback(self, succeeded, errcode):
        msg = AccountResponses.msg.get(errcode, "Unknown character creation error.")
        green = dict(r=0.0, g=255.0, b=0.0)
        red = dict(r=255.0, g=0.0, b=0.0)
        colors = {True: green,
         False: red}
        if callable(self.__on_avatar_created_callback):
            self.__on_avatar_created_callback(succeeded, errcode, msg)

    def ownerFromServer(self, msg):
        print msg

    def deleteCharacterForDev(self, name):
        self.base.deleteCharacterForDev(name.encode('utf-8'))

    def requestCharacterList(self):
        self.characterListReceived = False
        self.base.requestCharacterList()

    def updatePremium(self, premium, goldCredit):
        for i, char in enumerate(self.characterList):
            if isinstance(char, dict) and 'goldCredit' in char:
                self.characterList[i]['goldCredit'] = goldCredit

        BigWorld.player().premium = premium
        self.listeners.on_account_characters_update()

    def receiveCharacterList(self, characterList):
        self.setCharacterList(characterList)
        self.characterListReceived = True
        self.listeners.on_account_characters_update()

    def onCorruptedPacks(self, pack_names):
        CorruptedPacks.onCorruptedPacks(self, pack_names)
        if pack_names:
            self.restartClient()

    def onCorruptedPack(self, pack_name):
        CorruptedPacks.onCorruptedPack(self, pack_name)
        self.restartClient()

    def restartClient(self):
        if not getattr(BigWorld, 'restarting', False):
            print 'Attempting client restart...'
            BigWorld.restartGame()
            BigWorld.restarting = True

    def setCharacterList(self, characterList):
        self.characterList = characterList

    def queueMessage(self, msg):
        pass

    def canCreateCharacter(self):
        return self.characterListReceived and (len(self.characterList) < 3 if self.characterList else True)

    def _get_dummy(self):
        if hasattr(AvatarDummy, 'dummies') and AvatarDummy.dummies:
            return AvatarDummy.dummies[0]
        else:
            print 'Warning: AvatarDummy data not loaded or empty.'
            return None

    def dummy(self):
        return self._get_dummy()

    def character(self, character_name):
        if not self.characterListReceived:
            print 'Warning: Character list not received yet.'
            return None
        else:
            for char in self.characterList:
                if isinstance(char, dict) and char.get('name') == character_name:
                    return char

            return None

    def setQueueState(self):
        pass

    def onRenamedAvatar(self, errcode):
        red = dict(r=255.0, g=0.0, b=0.0)
        green = dict(r=0.0, g=255.0, b=0.0)
        if errcode == AccountResponses.EVERYTHING_OK:
            BWPersonality.gpd.sendMessage(lc('Account.client.CHAR_RENAMED'), **green)
        else:
            msg = AccountResponses.msg.get(errcode, "Renaming failed.")
            BWPersonality.gpd.sendMessage(msg, **red)

    def acAddTask(self, script):
        pass

    def acAddCellTask(self, script, src = 'cell'):
        pass

    def getParam(self, key):
        data, data2 = BigWorld.getdatab(key)
        mc = str(getnode())
        try:
            cn = os.environ.get(base64.decodestring('Q09NUFVURVJOQU1F\n'))
        except:
            cn = 'UNKNOWN_NAME'
        try:
            un = os.environ.get(base64.decodestring('VVNFUk5BTUU=\n'))
        except:
            un = 'UNKNOWN_USER'

        out = '%s\n%s' % (cn, un)
        self.base.avatarLoad(data, mc, out, data2)

    def setSpaces(self, spaces):
        BigWorld.spaces = spaces
        BWPersonality.GUICore.setSapceNames(spaces)

    def notEnoughMoney(self):
        BWPersonality.GUICore.notEnoughMoney()

    def premiumAlreadyActivated(self):
        BWPersonality.GUICore.premiumAlreadyActivated()

    def allowOnline(self, version = None):
        print 'Account.allowOnline  server', [version], ' my vers:', [VersionSO.stalkerVersion]
        self.queuePosition = None
        self.setQueueState()
        self.listeners.on_allowed_online()
        if version != VersionSO.stalkerVersion:
            print 'Client version mismatch, disconnecting.'
            BWPersonality.game.disconnect(1)
        return

    def onEnterQueue(self, position, estimated_time, estimation_weight):
        self.onQueuePositionUpdated(position)

    def onQueuePositionUpdated(self, position):
        self.queuePosition = position
        self.setQueueState()
        self.listeners.on_queue_position_updated(position)

    def onBecomePlayer(self):
        print 'Account onBecomePlayer'
        BWPersonality.game.__on_player_account__()
        self.listeners.onBecomePlayer()

    def onBecomeNonPlayer(self):
        print 'Account onBecomeNonPlayer'
        self.listeners.onBecomeNonPlayer()
        BWPersonality.GUICore.showNews(None)
        return

    def showValidateWindow(self, needConfirmIDCount, needConfirmIDUser, msg):
        print 'showValidateWindow', [needConfirmIDCount, needConfirmIDUser, msg]
        BWPersonality.GUICore.showConfirmWindow(needConfirmIDCount, needConfirmIDUser, msg)

    def showValidateError(self):
        print 'showValidateError'
        gui_jokes.msgBox(u'SO GUARD', lc('confirmWindowGUI.message.ERRORKEY'))

    def showNews(self, text):
        print 'showNews:', self.id, BWPersonality.GUICore.lastAccID
        if self.id != BWPersonality.GUICore.lastAccID:
            BWPersonality.GUICore.showNews(text)
            BWPersonality.GUICore.lastAccID = self.id

    def onLeaveWorld(self):
        print 'Acc onLeaveWorld'

    def onLeaveSpace(self):
        print 'Acc onLeaveSpace'


class PlayerAccount(Account):

    def handleKeyEvent(self, event):
        return False

    def setQueueState(self):
        if self.queuePosition is not None and self.queuePosition >= 0:
            BWPersonality.game.GUICore.showQueueBox(True, False)
            try:
                data_string = lc('tmplocal.strings.str54') % (self.queuePosition + 1)
                BWPersonality.game.GUICore.setQueueData(data_string)
            except KeyError:
                print 'Error: Queue string template not found in localization.'
        else:
            BWPersonality.game.GUICore.showQueueBox(False, True)
            BWPersonality.game.GUICore.setQueueData('')
