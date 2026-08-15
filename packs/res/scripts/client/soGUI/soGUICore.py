# uncompyle6 version 3.9.3
# Python bytecode version base 2.6 (62161)
# Decompiled from: Python 3.13.0 (tags/v3.13.0:60403a5, Oct  7 2024, 09:38:07) [MSC v.1941 64 bit (AMD64)]
# Embedded file name: scripts/client/soGUI/soGUICore.py
# Compiled at: 2089-08-05 23:12:16
from Localization import lc
import GUI, BigWorld, BWPersonality, os.path as path
from Settings import Settings
import Helpers.PyGUI as PyGUI, soGUI, gui_jokes
from soGUI.soContextMenuComponent import soContextMenuComponent
from soGUI.soToolTipComponent import soToolTipWindow
from soGUI.soToolTipComponent import soToolTipWindow2
from soGUI.soToolTipComponent import soToolTipComponent
from soGUI.soCharacterScreen import soCharacterScreen
from soGUI.soCharacterScreen import soCharacterScreen2
from soGUI.soSkillScreen import soSkillScreen
from soGUI.soSkillScreen import soSkillScreen2
from soGUI.soSkillScreen import soSkillGUI
from soGUI.soPCTradeScreen import soPCTradeScreen, soPCTradeScreen2
from soGUI.soTabletScreen import soTabletScreen
from soGUI.soClanScreen import soClanScreen
from soGUI.soNews import soNews
from soGUI.soClanScreen import soClanScreen2
from soGUI.soHyperLinkComponent import soHyperLinkComponent
from Helpers.PyGUI import PyGUIEvent
from soGUI.soQuickSlotsBar import soQuickSlotsBar
from soGUI.soQuickSlotsBar import soActionBar
import soGUI.selectMapGUI, soGUI.choiceTeam, soGUI.PVPmarker
from soGUI.soWeaponFlash import soWeaponFlash
from soGUI.soQuestLog import soQuestLog
from soGUI.soInteractionMarker import soInteractionMarker
from soGUI.soEditField import soEditField2
from soGUI.soAnomalyMeter import soAnomalyMeter
from soGUI.soLoginScreen import soLoginScreen2
from soGUI.soObjectivesGUI import soObjectivesGUI, soObjectivesGUI2
from soGUI.soTextField import soTextField2, soTextField3
from soGUI.soTextField import soTxtFieldPropsStructure
from soGUI.soItemCache import soItemCacheScreen
from soGUI.soUserFireCache import soUserFireCacheScreen
from soGUI.soWarehouse import soWarehouse
from soGUI.soArtifactQTE import soArtifactQTE
from soGUI.soChatConsole import soChatConsole2
from soGUI.soChatConsole3 import soChatConsole3
from soGUI.soQueueScreen import soQueueScreen
from soGUI.soHealthBar import soHealthBar
from soGUI.soTPCMainMenu import soTPCMainMenu
from soGUI.soCharacterManagmentGUI import soCharacterManagmentGUI
from soGUI.soIncomingDamageGUI import soIncomingDamageGUI
from soGUI.soOptionsGUI import soOptionsGUI, soOptionsGUI2
from soGUI.soOptionsGUI3 import soOptionsGUI3
from soGUI.soCraftGUI import soCraftGUI
from soGUI.soGPSMap import soGPSMap
from soGUI.soHelpGUI import soHelpGUI
from soGUI.soBulletinBoard import soBulletinBoard
from soGUI.soBaseTrader import soBaseTrader
from soGUI.soDialogueBox import soDialogueBox
from soGUI.soDialogueBox import soDlgBoxPropsStructure
from soGUI.soGUILayer import soGUILayer
from soGUI.soInventoryScreen import soInventoryScreen
from soGUI.soInventoryScreen import soInventoryScreen2
from soGUI.soTradeInterface import soTradeInterface
from soGUI.soTradeInterface import soNPCTradeGUI
from soGUI.soTradeInterface import soTradeGUI2
from soGUI.soMiniMap import soMiniMap
from soGUI.soFriend_BlackList import FriendList
from soGUI.DonateBase import DonatebaseGUI, DetailViewStakeGUI, ClanManagerNPCGUI
from soGUI.soTPCQuestLog import soTPCQuestLog
from soGUI.soPartyFrames import soPartyFrames, soPartyFrames2
from soGUI.soSystemMenu import soSystemMenu
from soGUI.soInworldMarkers import soInworldMarkers
from soGUI.soInworldMarkers import soInworldMarker
from soGUI.soTableComponent import soTableComponent as tableComp
from soGUI.soTableComponent import soTableComponent2, soTablePropsStructure, soTableElemPropsStructure
from soGUI.soTableComponent import tablePropsStructure
from soGUI.soProgressBars import soSpaceProgressBar
from soGUI.soProgressBars import soIngameProgressBar
from soGUI.soProgressBars import soDummyProgressBar
import soGUI.soProgressBars as soProgressBars
from soGUI.soDialogueGUI import soDialogueGUI2
from soGUI.soIngameMainMenu import soIngameMainMenu
from soGUI.soVisionModes import soSniperVision
from soGUI.soPvPStats import soPvPStats
from soGUI.soCharEffectsFrame import soCharEffectsGUI
from soGUI.soPPRenderer import soPPRenderer
from soGUI.soCastBar import soCastBar
from soGUI.soPrivateStoreGUI import soPrivateStoreScreen
from soGUI.soHelpGUIs import soTutorialGUI
from soGUI.soDropDownList import soDropDownList2
from soGUI.soPackageSellGUI import soPackageSellScreen
from soGUI.soCrosshairs import soTargettingGUI
from soGUI.soEditField import soEditBox
from soGUI.soMunitionsIndicator import soMunitionsGUI
from soGUI.soButton import soButton
from EffectUtils import EFFECT_TYPE
from soGUI.soMessageBoxGUI import soMessageBox, soMsgBoxMgr
from soGUI.soObjectiveTracker import soObjectiveTrackerGUI
from soGUI.soCharacterMaker import soCharacterMakerGUI
from soGUI.soCharacterPicker import soCharacterPickGUI
from soGUI.EULA import EULAGUI
from soGUI.soGUIBleed import soBleedGUI
from soGUI.soGUIpoison import soGUIpoison
from soGUI.soQuitMenu import soQuitMenu
from Helpers.BWCoroutine import *
from soGUI.data.TTFeed import TTFeeder
from soGUI.data.HintFeed import HintFeeder
from gui_const import MESSAGEBOX, GUI_ID, CHAR_MAKER, REPAIR, EULA
from math import floor, ceil
import _winreg, Helpers.Listener as Listener
from Keys import *
import Helpers.BWKeyBindings as BWKeyBindings
from Helpers.BWKeyBindings import BWKeyBindingAction
import soGUI.soStartSale, soGUI.soStartSubmitOffender, soGUI.PVPScore, Avatar
from Avatar import PlayerAvatar
import soGUI.confirmWindowGUI
MAPLIST = {'spaces/main': (lc('soGPSMap.soGUI.STRING_500_104')), 
   'spaces/so_origins': (lc('soGPSMap.soGUI.STRING_501_113')), 
   'spaces/novaya': (lc('soGPSMap.soGUI.STRING_502_107')), 
   'spaces/tunguska': (lc('soGPSMap.soGUI.STRING_503_111')), 
   'spaces/steppe': (lc('soGPSMap.soGUI.STRING_504_107')), 
   'spaces/steppe_dust': (lc('soGPSMap.soGUI.STRING_steppe_dust')), 
   'spaces/vesuvius': (lc('soGPSMap.soGUI.STRING_505_111')), 
   'spaces/volcano': (lc('soGPSMap.soGUI.STRING_506_107')), 
   'spaces/city_lubech': (lc('soGPSMap.soGUI.STRING_507_117')), 
   'spaces/outlands': (lc('soGPSMap.soGUI.STRING_508_112')), 
   'spaces/fukushima': (lc('soGPSMap.soGUI.minimap_fukushima')), 
   'spaces/outlands_caravan': (lc('soGPSMap.soGUI.minimap_outlands_caravan')), 
   'spaces/pk_prison01': (lc('soGPSMap.soGUI.minimap_pk_prison01')), 
   'spaces/lubech_uderground': (lc('soGPSMap.soGUI.minimap_lubech_underground')), 
   'spaces/outlands_airport': (lc('soGPSMap.soGUI.minimap_outlands_airport')), 
   'spaces/dm_outlands_village': (lc('soGPSMap.soGUI.minimap_dm_outlands_village')), 
   'spaces/dm_rocks': (lc('soGPSMap.soGUI.minimap_dm_rocks')), 
   'spaces/dm_ryabinushka': (lc('soGPSMap.soGUI.minimap_dm_ryabinushka')), 
   'spaces/dm_snowland': (lc('soGPSMap.soGUI.minimap_dm_snowland'))}

class topmostObject(object):

    def __init__(self, layerID=-1, closeOnKey=False, closeOnClick=False):
        self.layerID = layerID
        self.component = None
        self.oldData = {}
        self.closeOnKey = closeOnKey
        self.closeOnClick = closeOnClick
        return

    def restoreContent(self):
        if self.component:
            GUI.delRoot(self.component)
            self.oldData['parent'].script.topmostHiden()
            self.component = None
        return

    def setContent(self, cmp, parent):
        if self.component is not None:
            self.restoreContent()
        self.component = cmp
        self.oldData['parent'] = parent
        self.oldData['z'] = cmp.position.z
        self.component.position.z = 0.0
        GUI.addRoot(self.component)
        return

    def showContent(self):
        self.component.visible = True
        GUI.reSort()
        return

    def hideContent(self):
        self.component.visible = False
        return

    def restoreIfParentHiden(self):
        if self.component is not None:
            parent = self.oldData['parent']
            while parent:
                if parent.visible:
                    parent = parent.parent
                else:
                    self.restoreContent()
                    return True

            if parent not in GUI.roots():
                self.restoreContent()
                return True
        return False


class soGUICore(PyGUI.Window, BWKeyBindings.BWActionHandler, Listener.Listenable):
    """
        ╙яЁрты ■∙шщ ъырёё фы  тёхї GUI шуЁ√, фюыцхэ ёє∙хёЄтютрЄ№ т уыюсры№эюь эхщьёяхщёх BWPersonality
        эр тё╕ь яЁюЄ цхэшш ЁрсюЄ√ ъышхэЄр.
        
        ╤ё√ыър эр шэёЄрэё ъырёёр эрїюфшЄё  т gpd (gpd.guiCore)
        """
    DRAGSTART_DIFF = 1
    LAYER_MODE_MENU = 0
    LAYER_MODE_INGAME = 1
    GAMEMODE_LOGIN = 0
    GAMEMODE_INGAME = 1
    KEYBOARD_RU = 0
    KEYBOARD_EN = 1
    TOPMOST_DDL = 0
    TOPMOST_CONTEXT = 1
    TOPMOST_TOOLTIP = 2
    GUI_ID_NONE = 0
    GUI_ID_LOGIN = 1
    GUI_ID_OPTIONS = 2
    GUI_ID_SERVERLIST = 3
    GUI_ID_CHARSELECT = 4
    GUI_ID_CHARCREATE = 5
    GUI_ID_INVENTORY = 6
    GUI_ID_NPCTRADE = 7
    GUI_ID_NPCTRADESUMMARY = 8
    GUI_ID_PCTRADE = 9
    GUI_ID_CHARSCREEN = 10
    GUI_ID_PDAMAIN = 11
    GUI_ID_PDAMAP = 12
    GUI_ID_PDAPEDIA = 13
    GUI_ID_PDARECIPES = 14
    GUI_ID_PDAGUILD = 15
    GUI_ID_PDAQUEST = 16
    GUI_ID_EFFECTSFRAME = 17
    GUI_ID_SKILLS = 18
    GUI_ID_ITEMCACHE = 19
    GUI_ID_PRIVATESTORE = 20
    GUI_ID_TUTORIAL = 21
    GUI_ID_PLAYERMANUAL = 22
    GUI_ID_PACKAGESELL = 23
    GUI_ID_ACTIONBAR = 24
    GUI_ID_PVPSTATS = 25
    GUI_ID_REPSTATS = 26
    GUI_ID_PARTYFRAMES = 27
    GUI_ID_PLAYERFRAME = 28
    GUI_ID_OPTIONS_NEW = 36
    GUI_ID_FRIENDLISTPOPUP = 37
    GUI_ID_BLACKLISTPOPUP = 38

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        Listener.Listenable.__init__(self)
        component.script = self
        self.lastAccID = 0
        self.lastLayerMode = 0
        self.eula_state = False
        self.contextMenu = None
        self.repairMode = False
        self.modalState = False
        self.radioGroups = {}
        self.goldCost = 0
        self.toolTip = None
        self.testVar = 0
        self.genericTimerSecs = 0
        self.timerCheckCoroutine = None
        self.DnDHook = lambda event: False
        self.mouseHook = lambda event: False
        self.keyHook = lambda event: False
        self.mouseDoubleClickSpeed = 500
        self.dlgBoxes = {}
        self.msgBoxes = {}
        self.generalLayer = None
        self.worldLayer = None
        self.menuLayer = None
        self.modalLayer = None
        self.systemLayer = None
        self.mouseCursorHost = None
        self.currentMode = soGUICore.GAMEMODE_LOGIN
        self.msgBoxMgr = None
        self.QuitMenu = None
        self.charScreen = None
        self.playerTrade = None
        self.confirmWindow = None
        self.skillsGUI = None
        self.tabletPC = None
        self.clanGUI = None
        self.questLogGUI = None
        self.weaponFlasher = None
        self.interactionGUI = None
        self.anomalyMeter = None
        self.loginGUI = None
        self.objectivesGUI = None
        self.itemCacheGUI = None
        self.userFireGUI = None
        self.WarehouseGUI = None
        self.startSaleGUI = None
        self.startSubmitOffender = None
        self.artifactQTE = None
        self.chatConsole = None
        self.queueGUI = None
        self.healthBarGUI = None
        self.tabletPCMainMenu = None
        self.characterManager = None
        self.optionsGUI = None
        self.friendList = FriendList(GUI.Window())
        self.DonateBase = DonatebaseGUI(GUI.Window())
        self.DetailViewStakeGUI = DetailViewStakeGUI(GUI.Window())
        self.ClanManagerNPCGUI = ClanManagerNPCGUI(GUI.Window())
        self.QuitMenu = None
        self.craftGUI = None
        self.gpsGUI = None
        self.helpGUI = None
        self.soBulletinBoard = None
        self.soBaseTrader = None
        self.inventoryGUI = None
        self.tradeGUI = None
        self.miniMapGUI = None
        self.partyGUI = None
        self.systemMenu = None
        self.targettingGUI = None
        self.charMaker = None
        self.charPicker = None
        self.GUIpoison = None
        self.quickSlots = None
        self.actionBar = None
        self.selectMap = None
        self.shoiceTeamWindow = None
        self.PVPmarkerGUI = None
        self.incomingDmgGUI = None
        self.inworldMarkersGUI = None
        self.spaceLoaderGUI = None
        self.appLoaderGUI = None
        self.ingameLoaderGUI = None
        self.dummyLoaderGUI = None
        self.dialogueGUI = None
        self.ingameMenuGUI = None
        self.sniperVision = None
        self.pvpStatsGUI = None
        self.effectsFrame = None
        self.ppRenderer = None
        self.castBar = None
        self.privateStoreGUI = None
        self.tutorialGUI = None
        self.soNewsGUI = None
        self.packageGUI = None
        self.pvpScoreBar = None
        self.munitionsGUI = None
        self.objectiveTrackerGUI = None
        self.clanRights = []
        self.EULAgui = None
        # -- NEW индикаторы --
        self.weightLabel = None
        self.fpsLabel = None
        self.showWeight = True      # позже возьмётся из настроек
        self.showFPS = True
        self.fpsTimerID = None
        self._lastFPSTime = 0
        self._fpsFrameCount = 0
        self.setupRoot()
        self.setupLayers()
        self.contextState = False
        self.toolTipState = False
        self.characterReciever = None
        self.mouseAltMode = False
        self.listWantedDataSection = None
        self.inventoryDataSection = None
        self.privateStoreDataSection = None
        self.skillsDataSection = None
        self.clanDataSection = None
        self.tradeDataSection = None
        self.vendorDataSection = None
        self.bulletinBoardDataSection = None
        self.quickSlotsDataSection = None
        self.actionBarDataSection = None
        self.currentWeaponDataSection = None
        self.questLogDataSection = {'quests': [], 'completed': [], 'mode': (soTPCQuestLog.MODE_CURRENT)}
        self.interactionMode = None
        self.objectiveDataSection = None
        self.itemCacheDataSection = None
        self.warehouseDataSection = None
        self.itemCacheDataUserFireSection = None
        self.artifactQTEDataSection = None
        self.chatConsoleDataSection = None
        self.queueDataSection = None
        self.healthDataSection = None
        self.characterManagerDataSection = dict(selection=('', 0), creation=None)
        self.craftDataSection = None
        self.loginDataSection = None
        self.gpsDataSection = None
        self.optionsDataSection = {}
        self.inworldMarkersDataSection = None
        self.charStatsDataSection = None
        self.dialogueDataSection = None
        self.pvpStatsDataSection = None
        self.clanTradeDataSection = None
        self.tutorialDataSection = None
        self.packageSellDataSection = None
        self.crosshairsDataSection = None
        self.munitionsDataSection = None
        self.iconTextures = None
        self.GUItextures = None
        self.toolTipFeeder = TTFeeder()
        self.hintFeeder = HintFeeder()
        self.contextLayer = None
        self.binocularsCmp = None
        self.bulletinBoardShopDataSection = {}
        self.bulletinBoardHunterDataSection = {}
        self.hiddenState = False
        self.hiddenGUIs = []
        self.visibleRoots = []
        self.topMostObjects = {(soGUICore.TOPMOST_DDL): (topmostObject(soGUICore.TOPMOST_DDL, True, True)), 
           (soGUICore.TOPMOST_CONTEXT): (topmostObject(soGUICore.TOPMOST_CONTEXT, False, False)), 
           (soGUICore.TOPMOST_TOOLTIP): (topmostObject(soGUICore.TOPMOST_TOOLTIP, False, False))}
        self.getDoubleClickSpeedFromWin()
        self.store_roomData = None
        self._draggedComponent = None
        self._dragOffset = (0, 0)
        self._fpsBG = None
        self._weightBG = None
        self.hudEditMode = False
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'LEGACY'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.verticalAnchor = 'CENTER'
        cmp.horizontalAnchor = 'CENTER'
        cmp.position = (0.0, 0.0, 10.0)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.focus = True
        cmp.crossFocus = True
        cmp.dragFocus = False
        cmp.moveFocus = False
        GUI.addRoot(cmp)
        return

    def setupLayers(self):
        layer = soGUILayer(GUI.Window())
        cmp = layer.component
        cmp.position.z = 1.0
        GUI.addRoot(cmp)
        self.menuLayer = cmp
        layer = soGUILayer(GUI.Window())
        cmp = layer.component
        cmp.position.z = 0.9
        GUI.addRoot(cmp)
        self.worldLayer = cmp
        layer = soGUILayer(GUI.Window())
        cmp = layer.component
        cmp.position.z = 0.5
        cmp.visible = True
        cmp.dropFocus = False
        GUI.addRoot(cmp)
        self.generalLayer = cmp
        layer = soGUILayer(GUI.Window())
        cmp = layer.component
        cmp.position.z = 0.2
        cmp.visible = False
        cmp.mouseButtonFocus = True
        cmp.focus = True
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.dragFocus = True
        GUI.addRoot(cmp)
        self.modalLayer = cmp
        layer = soGUILayer(GUI.Window())
        cmp = layer.component
        cmp.position.z = 0.0
        cmp.visible = True
        cmp.mouseButtonFocus = False
        cmp.focus = False
        cmp.crossFocus = False
        cmp.moveFocus = False
        cmp.dragFocus = False
        cmp.dropFocus = False
        GUI.addRoot(cmp)
        self.systemLayer = cmp
        GUI.reSort()
        return

    def start(self):
        self.setLayerMode(self.LAYER_MODE_MENU)
        self.tabletPC = soTabletScreen(GUI.Window())
        self.tabletPC.onBound()
        self.tabletPCMainMenu = soTPCMainMenu(GUI.Window())
        self.tabletPCMainMenu.onBound()
        self.tabletPC.addInterface(soTabletScreen.INTERFACE_MAIN, self.tabletPCMainMenu.component)
        self.loginGUI = soLoginScreen2(GUI.Window())
        self.loginGUI.onBound()
        self.loginGUI.show()
        self.showCharacterMaker(False)
        self.showCharacterPicker(False)
        self.showHealthBar(True)
        self.miniMapGUI = soMiniMap(GUI.Window())
        self.miniMapGUI.onBound()
        self.systemMenu = soSystemMenu(GUI.Window())
        self.systemMenu.onBound()
        self.inworldMarkersGUI = soInworldMarkers(GUI.Window())
        self.inworldMarkersGUI.onBound()
        self.effectsFrame = soCharEffectsGUI(GUI.Window())
        self.effectsFrame.onBound()
        self.effectsFrame.show()
        self.showActionBar(True)
        self.ppRenderer = soPPRenderer(GUI.Window())
        self.ppRenderer.onBound()
        self.ppRenderer.show()
        self.targettingGUI = soTargettingGUI(GUI.Window())
        self.targettingGUI.onBound()
        self.targettingGUI.show()
        self.partyGUI = soPartyFrames2(GUI.Window())
        self.partyGUI.onBound()
        self.partyGUI.show()
        self.munitionsGUI = soMunitionsGUI(GUI.Window())
        self.munitionsGUI.onBound()
        self.munitionsGUI.show()
        self.objectiveTrackerGUI = soObjectiveTrackerGUI(GUI.Window())
        self.objectiveTrackerGUI.onBound()
        self.objectiveTrackerGUI.show()
        self.msgBoxMgr = soMsgBoxMgr()
        GUI.setDragDistance(1e-05)
        self.setClanRights([])
        if self.EULAgui is None:
            self.EULAgui = EULAGUI(GUI.Window())
            self.EULAgui.onBound()
        self.eula_state = self.EULAgui.get_eula_state()
        if not self.eula_state:
            self.EULAgui.show()
        self.bleedGUI = soBleedGUI(GUI.Window())
        self.bleedGUI.onBound()
        self.GUIpoison = soGUIpoison(GUI.Window())
        self.GUIpoison.onBound()
        self._createWeightLabel()
        self._createFPSLabel()
        self._startFPSTimer()
        settings = Settings()
        self.showWeight = settings.getSetting('showWeight', True)
        self.showFPS = settings.getSetting('showFPS', True)
        self.setShowWeight(self.showWeight)
        self.setShowFPS(self.showFPS)
        return

    def finalize(self):
        print 'GUICore::finalize'
        self._stopFPSTimer()
        for root in GUI.roots():
            self.clearAllChildren(root)
            root.script = None
            GUI.delRoot(root)

        self.iconTextures = None
        self.charScreen = None
        self.playerTrade = None
        self.skillsGUI = None
        self.tabletPC = None
        self.clanGUI = None
        self.questLogGUI = None
        self.weaponFlasher = None
        self.interactionGUI = None
        self.anomalyMeter = None
        self.loginGUI = None
        self.objectivesGUI = None
        self.itemCacheGUI = None
        self.userFireGUI = None
        self.WarehouseGUI = None
        self.startSaleGUI = None
        self.startSubmitOffender = None
        self.artifactQTE = None
        self.chatConsole = None
        self.queueGUI = None
        self.healthBarGUI = None
        self.tabletPCMainMenu = None
        self.characterManager = None
        self.optionsGUI = None
        self.craftGUI = None
        self.gpsGUI = None
        self.helpGUI = None
        self.soBulletinBoard = None
        self.soBaseTrader = None
        self.inventoryGUI = None
        self.tradeGUI = None
        self.miniMapGUI = None
        self.partyGUI = None
        self.systemMenu = None
        self.targettingGUI = None
        self.quickSlots = None
        self.actionBar = None
        self.selectMap = None
        self.shoiceTeamWindow = None
        self.PVPmarkerGUI = None
        self.incomingDmgGUI = None
        self.inworldMarkersGUI = None
        self.spaceLoaderGUI = None
        self.appLoaderGUI = None
        self.ingameLoaderGUI = None
        self.dummyLoaderGUI = None
        self.dialogueGUI = None
        self.ingameMenuGUI = None
        self.sniperVision = None
        self.pvpStatsGUI = None
        self.effectsFrame = None
        self.ppRenderer = None
        self.castBar = None
        self.privateStoreGUI = None
        self.tutorialGUI = None
        self.soNewsGUI = None
        self.packageGUI = None
        self.pvpScoreBar = None
        self.msgBoxMgr.fini()
        return

    def handleMouseEvent(self, event):
        handled = self.DnDHook(event)
        handled = self.mouseHook(event)
        return handled

    def handleCharEvent(self, char, key, mods):
        if self.characterReciever is not None:
            handled = self.characterReciever.script.handleChar(char, key, mods)
            if handled:
                return True
        return False

    def handleKeyEvent(self, event):
        key = event.key
        char = event.character
        mods = event.modifiers
        down = event.isKeyDown()
        if down and key == KEY_TAB and mods == 0:
            self.hudEditMode = not self.hudEditMode
            if self.hudEditMode:
                # Можно сменить курсор или вывести подсказку, но не обязательно
                pass
            return True
        if self.contextMenu and self.contextMenu.isVisible and not down and key in (KEY_LEFTMOUSE,):
            BigWorld.callback(0.0, self.contextMenu.hide)
        if not self.eula_state:
            return False
        else:
            if down and key == KEY_ESCAPE and self.soNewsGUI and self.soNewsGUI.isVisible:
                self.soNewsGUI.hide()
                return True
            if hasattr(self.generalLayer, 'GUILocker'):
                if self.generalLayer.GUILocker.visible:
                    if self.GUILockerCallback is not None:
                        self.GUILockerCallback(event)
                    return True
            if self.keyHook(event):
                return True
            if self.chatConsole is not None:
                if self.chatConsole.typing:
                    if down:
                        if key == KEY_UPARROW:
                            self.chatConsole.repeatInput(True)
                        elif key == KEY_DOWNARROW:
                            self.chatConsole.repeatInput(False)
            if down and key == KEY_ESCAPE:
                if self.spaceLoaderGUI:
                    if self.spaceLoaderGUI.component.visible:
                        return True
            for topObj in self.topMostObjects:
                if not event.isMouseButton():
                    if self.topMostObjects[topObj].closeOnKey:
                        if down:
                            self.topMostObjects[topObj].restoreContent()

            if self.characterReciever is not None:
                handled = self.characterReciever.script.handleKeyEvent(event)
                if handled:
                    return True
            if self.contextLayer is not None and down:
                self.contextLayer.visible = False
            if down and key == KEY_ESCAPE:
                handled = False
                if self.pvpScoreBar and self.pvpScoreBar.scoreBarVisible():
                    self.pvpScoreBar.setVisibleScore(False)
                    return True
                if self.repairMode:
                    self.showRepairMode(False)
                    return True
                if self.msgBoxMgr is not None:
                    handled = self.msgBoxMgr.onEscapeKey()
                if self.dialogueGUI is not None:
                    if self.dialogueGUI.component.visible:
                        self.showDialogueGUI(False)
                        handled = True
                if self.charScreen is not None:
                    if self.charScreen.component.visible:
                        self.showCharScreen(False)
                        handled = True
                if self.packageGUI is not None:
                    if self.packageGUI.component.visible:
                        self.showPackageSell(False)
                        handled = True
                if self.ingameMenuGUI is not None:
                    if self.ingameMenuGUI.component.visible:
                        self.ingameMenuGUI.resumeGame()
                        handled = True
                if self.skillsGUI is not None:
                    if self.skillsGUI.component.visible:
                        self.showSkillsGUI(False)
                        handled = True
                if self.playerTrade is not None:
                    if self.playerTrade.component.visible:
                        self.showPCTrade(False)
                        handled = True
                if self.artifactQTE is not None:
                    if self.artifactQTE.component.visible:
                        self.showArtifactQTE(False)
                        handled = True
                if self.clanGUI is not None:
                    if self.clanGUI.component.visible:
                        self.showClanGUI(False)
                        handled = True
                if self.itemCacheGUI is not None:
                    if self.itemCacheGUI.component.visible:
                        self.showItemCache(False)
                        handled = True
                if self.userFireGUI is not None:
                    if self.userFireGUI.component.visible:
                        self.showUserFire(False)
                        handled = True
                if self.WarehouseGUI is not None:
                    if self.WarehouseGUI.component.visible:
                        self.showWarehouse(False)
                        handled = True
                if self.startSaleGUI is not None:
                    if self.startSaleGUI.component.visible:
                        self.showStartSale(False)
                        handled = True
                if self.startSubmitOffender is not None:
                    if self.startSubmitOffender.component.visible:
                        self.showSubmitOffender()(False)
                        handled = True
                if self.questLogGUI is not None:
                    if self.questLogGUI.component.visible:
                        self.showQuestLog(False)
                        handled = True
                if self.tabletPC is not None:
                    if self.tabletPC.component.visible:
                        self.showTabletPC(False)
                        handled = True
                if self.optionsGUI is not None:
                    if self.optionsGUI.component.visible:
                        self.showOptions(False)
                        handled = True
                if self.friendList is not None:
                    if self.friendList.component.visible:
                        self.showFriendList(False)
                        handled = True
                if self.DonateBase is not None:
                    if self.DonateBase.component.visible:
                        self.showDonateBase(False)
                        handled = True
                if self.DetailViewStakeGUI is not None:
                    if self.DetailViewStakeGUI.component.visible:
                        self.showDetailViewStakeGUI(False)
                        handled = True
                if self.ClanManagerNPCGUI is not None:
                    if self.ClanManagerNPCGUI.component.visible:
                        self.showClanManagerNPCGUI(False)
                        handled = True
                if self.optionsGUI is not None:
                    if self.optionsGUI.component.visible:
                        self.showTempOptions(False)
                        handled = True
                if self.QuitMenu is not None:
                    if self.QuitMenu.component.visible:
                        self.showQuitMenu(doShow=False)
                        handled = True
                if self.craftGUI is not None:
                    if self.craftGUI.component.visible:
                        self.showCraftGUI(False)
                        handled = True
                if self.inventoryGUI is not None:
                    if self.inventoryGUI.component.visible:
                        self.showInventory(False)
                        handled = True
                if self.privateStoreGUI is not None:
                    if self.privateStoreGUI.component.visible:
                        self.showPrivateStore(False)
                        handled = True
                if self.tradeGUI is not None:
                    if self.tradeGUI.component.visible:
                        self.showTrade(False)
                        handled = True
                if self.soBulletinBoard is not None:
                    if self.soBulletinBoard.component.visible:
                        self.showBulletinBoard(False)
                        handled = True
                if self.soBaseTrader is not None:
                    if self.soBaseTrader.component.visible:
                        self.showBasetrader(False)
                        handled = True
                if self.helpGUI is not None:
                    if self.helpGUI.component.visible:
                        self.showHelpGUI(False)
                        handled = True
                if hasattr(BigWorld.player(), 'playerGUI'):
                    if hasattr(BigWorld.player().playerGUI, 'questGUI'):
                        if BigWorld.player().playerGUI.questGUI.script.dlg:
                            BigWorld.player().playerGUI.questGUI.script.wantClose()
                            handled = True
                if self.clanGUI is not None:
                    if self.clanGUI.component.visible:
                        self.clanGUI.hide()
                        handled = True
                if self.helpGUI is not None:
                    if self.helpGUI.component.visible:
                        self.helpGUI.hide()
                        handled = True
                if self.soBulletinBoard is not None:
                    if self.soBulletinBoard.component.visible:
                        self.soBulletinBoard.hide()
                        handled = True
                if self.gpsGUI is not None:
                    if self.gpsGUI.component.visible:
                        self.gpsGUI.hide()
                        handled = True
                if self.characterManager is not None:
                    if self.characterManager.component.visible:
                        if self.characterManager.currentMode == soGUI.soCharacterManagmentGUI.MODE_CREATE:
                            self.characterManagerEvent(soGUI.soCharacterManagmentGUI.EVENT_CANCELMAKE, None)
                        handled = True
                if self.selectMap is not None:
                    if self.selectMap.script.visible:
                        self.showSelectMap(False)
                        handled = True
                if self.shoiceTeamWindow is not None:
                    if self.shoiceTeamWindow.isVisible():
                        self.showChoiceTeam(False)
                        handled = True
                if handled:
                    return True
                self.setMouseAltState(False)
            if key in (KEY_RETURN, KEY_NUMPADENTER):
                if down:
                    handled = self.msgBoxMgr.onReturnKey()
                    if handled:
                        return True
                if isinstance(BigWorld.player(), PlayerAvatar):
                    if down:
                        if mods & MODIFIER_ALT == MODIFIER_ALT:
                            return False
                        else:
                            self.chatConsole.toggleConsoleInput()
                            return True
            return False

    def gainMouseCursor(self, component):
        self.mouseCursorHost = component
        return

    def loseMouseCursor(self, component):
        if self.mouseCursorHost == component:
            self.mouseCursorHost = None
        return

    def notEnoughMoney(self):
        gui_jokes.askUserOk(lc('BWPersonality.client.notEnoughMoneyTitle'), lc('BWPersonality.client.notEnoughMoneyText'))
        return

    def premiumAlreadyActivated(self):
        gui_jokes.askUserOk(lc('BWPersonality.client.premiumAlreadyActivatedTitle'), lc('BWPersonality.client.premiumAlreadyActivatedText'))
        return

    def TPCGeneralEvent(self, event, data):
        self.listeners.TPCGeneralEvent(event, data)
        return

    def contextMenuEvent(self, iid, id, caption, event):
        self.listeners.contextMenuEvent(iid, id, caption, event)
        if event != soGUI.soContextMenuComponent.EVENT_SHOW:
            self.contextState = False
        return

    def optionsEvent(self, event, data):
        self.listeners.optionsEvent(event, data)
        return

    def ingameMenuEvent(self, event, data):
        self.listeners.ingameMenuEvent(event, data)
        return

    def toolTipEvent(self, id, iid, event):
        if event == soToolTipComponent.EVENT_SHOW:
            self.listeners.toolTipEvent(id, iid, event)
        elif event == soToolTipComponent.EVENT_HIDE:
            self.listeners.toolTipEvent(id, iid, event)
            if self.toolTip is not None:
                self.toolTip.hide()
                self.toolTipState = False
        self.toolTipFeeder.toolTipEvent(id, iid, event)
        return

    def skillEvent(self, event, data):
        self.listeners.skillEvent(event, data)
        return

    def mouseMovementEvent(self, data):
        self.listeners.mouseMovementEvent(data)
        return

    def tradeEvent(self, event, data):
        self.listeners.tradeEvent(event, data)
        return

    def pcTradeEvent(self, event, data):
        self.listeners.pcTradeEvent(event, data)
        return

    def clanMemberActionsRequest(self, caption):
        self.listeners.clanMemberActionsRequest(caption)
        return

    def clanEvent(self, event, data):
        self.listeners.clanEvent(event, data)
        return

    def clanTraderEvent(self, event, data):
        self.listeners.clantTraderEvent(event, data)
        return

    def quickBarEvent(self, event, data):
        self.listeners.quickBarEvent(event, data)
        return

    def actionBarEvent(self, event, data):
        self.listeners.actionBarEvent(event, data)
        return

    def questLogEvent(self, data, event):
        self.listeners.questLogEvent(data, event)
        return

    def reputationEvent(self, event, data):
        self.listeners.reputationEvent(event, data)
        return

    def graphicOptsEvent(self, event, data):
        return

    def soundOptsEvent(self, event, data):
        self.listeners.soundOptsEvent(event, data)
        return

    def controlsOptsEvent(self, event, data):
        return

    def loginEvent(self, event, data):
        self.listeners.loginEvent(event, data)
        return

    def characterManagerEvent(self, event, data):
        self.listeners.characterManagerEvent(event, data)
        return

    def itemCacheEvent(self, event, data):
        self.listeners.itemCacheEvent(event, data)
        return

    def itemCacheUserFireEvent(self, event, data):
        self.listeners.itemCacheUserFireEvent(event, data)
        return

    def itemCacheWarehouseEvent(self, event, data):
        self.listeners.itemCacheWarehouseEvent(event, data)
        return

    def artifactQTEEvent(self, event, data):
        self.listeners.artifactQTEEvent(event, data)
        return

    def chatEvent(self, event, data):
        self.listeners.chatEvent(event, data)
        return

    def hlinkEvent(self, event, data):
        self.listeners.hlinkEvent(event, data)
        return

    def queueEvent(self, event, data):
        self.listeners.queueEvent(event, data)
        return

    def craftEvent(self, event, data):
        self.listeners.craftEvent(event, data)
        return

    def GPSEvent(self, event, data):
        self.listeners.GPSEvent(event, data)
        return

    def dlgBoxEvent(self, event, data):
        self.listeners.dlgBoxEvent(event, data)
        return

    def msgBoxEvent(self, event, data):
        """
                msgBoxEvent(event, data)
                event is an int and may be one of the gui_const.MESSAGEBOX.EVENT_*** constants
                data is a dict
                data will always have 'id' key, which identifies the message box 
                when event == gui_const.MESSAGEBOX.EVENT_BTNPRESS, data has the following additional keys:
                'btn' - button type, can be one of the gui_const.MESSAGEBOX.BTN_*** constants
                'add_controls' - dict with additional controls' ids as keys, and their values as values
                when event == gui_const.MESSAGEBOX.EVENT_ADDCONTROL, data has the following additional keys:
                'add_control_id' - id of the additional control
                'add_control_data' - value of the additional control
                """
        self.listeners.msgBoxEvent(event, data)
        if event == MESSAGEBOX.EVENT_BTNPRESS:
            event = soDialogueBox.EVENT_BTNPRESS
            newData = [data['id'], data['btn']]
            newControlData = []
            controlData = data['add_controls']
            if controlData is not None:
                for ctrl in controlData:
                    newControlData.append([ctrl, controlData[ctrl]])

            newData.append(newControlData)
            self.dlgBoxEvent(event, newData)
        elif event == MESSAGEBOX.EVENT_CLOSE:
            event = soDialogueBox.EVENT_CLOSE
            newData = [data['id'], None, None]
            self.dlgBoxEvent(event, newData)
        elif event == MESSAGEBOX.EVENT_CLOSE_NONUSER:
            event = soDialogueBox.EVENT_CLOSE_NONUSER
            newData = [data['id'], None, None]
            self.dlgBoxEvent(event, newData)
        return

    def eulaEvent(self, event, data):
        self.listeners.eulaEvent(event, data)
        if event == EULA.EVENT_ACCEPT:
            self.on_eula_accpeted()
        elif event == EULA.EVENT_DECLINE:
            self.on_eula_declined()
        return

    def charScreenEvent(self, event, data):
        self.listeners.charScreenEvent(event, data)
        return

    def inventoryEvent(self, event, data):
        self.listeners.inventoryEvent(event, data)
        return

    def charMakerEvent(self, event, data):
        self.listeners.charMakerEvent(event, data)
        return

    def charPickerEvent(self, event, data):
        self.listeners.charPickerEvent(event, data)
        return

    def repairEvent(self, event, data):
        self.listeners.repairEvent(event, data)
        return

    def packageSellEvent(self, event, data):
        self.listeners.packageSellEvent(event, data)
        return

    def privateStoreEvent(self, event, data):
        self.listeners.privateStoreEvent(event, data)
        return

    def partyEvent(self, event, data):
        self.listeners.partyEvent(event, data)
        return

    def playerFrameEvent(self, event, data):
        self.listeners.playerFrameEvent(event, data)
        return

    def loaderGUIEvent(self, event, data):
        self.listeners.loaderGUIEvent(event, data)
        return

    def dialogueEvent(self, event, data):
        self.listeners.dialogueEvent(event, data)
        return

    def castBarEvent(self, event, data):
        self.listeners.castBarEvent(event, data)
        return

    def generalGUIEvent(self, event, data):
        self.listeners.generalGUIEvent(event, data)
        return

    def onWindowsState(self, gui_id, component):
        self.msgBoxMgr.updateParentVisibility()
        return

    def setInventoryData(self, items, weight, money, filterMask=0):
        if self.inventoryGUI is None:
            self.inventoryGUI = soInventoryScreen2(GUI.Window())
            self.inventoryGUI.onBound()
        self.inventoryDataSection = {'items': items, 
           'weight': weight, 
           'money': money, 
           'filters': filterMask}
        self.inventoryGUI.update()

        if self.weightLabel and self.showWeight:
            try:
                curWeight = weight[0]
                maxWeight = weight[1]
                self.weightLabel.text = u"Вес: %.1f / %.1f кг" % (curWeight, maxWeight)
            except:
                pass

    def resetGUI(self):
        if self.objectiveTrackerGUI is not None:
            self.objectiveTrackerGUI._alignToMiniMap()
        return

    def setMunitionsData(self, data):
        self.munitionsDataSection = data
        self.munitionsGUI.update()
        return

    def bindMinimap(self):
        self.miniMapGUI.bindToPlayer()
        return

    def setCrosshairsData(self, data):
        if self.targettingGUI is None:
            self.targettingGUI = soTargettingGUI(GUI.Window())
            self.targettingGUI.onBound()
        self.crosshairsDataSection = data
        self.targettingGUI.update()
        return

    def setCharScreenData(self, data):
        if self.charScreen is None:
            self.charScreen = soCharacterScreen2(GUI.Window())
            self.charScreen.onBound()
        self.characterScreenDataSection = data
        self.charScreen.update()
        return

    def setPackageSellData(self, data):
        if self.packageGUI is None:
            self.packageGUI = soPackageSellScreen(GUI.Window())
            self.packageGUI.onBound()
        self.packageSellDataSection = data
        self.packageGUI.update()
        return

    def setPrivateStoreData(self, data):
        if self.privateStoreGUI is None:
            self.privateStoreGUI = soPrivateStoreScreen(GUI.Window())
            self.privateStoreGUI.onBound()
        self.privateStoreDataSection = data
        self.privateStoreGUI.update()
        return

    def setClanRights(self, rights):
        if self.clanGUI is None:
            self.clanGUI = soClanScreen2(GUI.Window())
            self.clanGUI.onBound()
        self.clanRights = rights
        self.clanGUI.applyRights()
        return

    def setPvPStatsData(self, data):
        if self.pvpStatsGUI is None:
            self.pvpStatsGUI = soPvPStats(GUI.Window())
            self.pvpStatsGUI.onBound()
        self.pvpStatsDataSection = data
        self.pvpStatsGUI.update()
        return

    def setDialogueData(self, data):
        if self.dialogueGUI is None:
            self.dialogueGUI = soDialogueGUI2(GUI.Window())
            self.dialogueGUI.onBound()
        self.dialogueDataSection = data
        self.dialogueGUI.update()
        return

    def setCharStatsData(self, data):
        return
        self.charStatsDataSection = data
        if self.charScreen is not None:
            self.charScreen.applyStats()
        return

    def testInworldMarkers(self):
        from matrix_providers import ShiftProvider

        def updater():
            marks = []
            for i in xrange(30):
                marks.append((u'TestLabel', ShiftProvider(BigWorld.player().matrix, (10 + i * 0.1, 5 + i * 0.1, 10 + i * 0.1)), [soInworldMarker.MARKER_PLAYER], 255))

            self.setInworldMarkersData(marks)
            self.im_test_cb = BigWorld.callback(0.1, updater)
            return

        self.im_test_cb = BigWorld.callback(0.1, updater)
        return

    def setInworldMarkersData(self, data):
        self.inworldMarkersDataSection = data
        self.inworldMarkersGUI.update()
        return

    def spaceChange(self, spaceName):
        self.miniMapGUI.changeMap(spaceName)
        return

    def pcTradeData(self, data):
        print 'warning: GUICore::pcTradeData is now banned, use GUICore::setPCTradeData instead'
        self.tradeDataSection = data
        if self.playerTrade is not None:
            if isinstance(BigWorld.player(), Avatar.PlayerAvatar):
                self.playerTrade.update()
        return

    def setPCTradeData(self, data):
        if self.playerTrade is None:
            self.playerTrade = soPCTradeScreen2(GUI.Window())
            self.playerTrade.onBound()
        self.tradeDataSection = data
        self.playerTrade.update()
        return

    def skillData(self, data):
        self.skillsDataSection = data
        if self.skillsGUI is None:
            self.skillsGUI = soSkillScreen2(GUI.Window())
            self.skillsGUI.onBound()
        self.skillsGUI.update()
        self.systemMenu.refreshPoints()
        return

    def setSkillData(self, data):
        if self.skillsGUI is None:
            self.skillsGUI = soSkillScreen2(GUI.Window())
            self.skillsGUI.onBound()
        self.skillsGUI.update(data)
        self.systemMenu.refreshPoints()
        return

    def testSkillData(self):
        from gui_const import LEVELING
        self.updateBasicSkills()
        self.setSpecData(LEVELING.SPEC_EQUIPMENT, {'modifier': [105, 1], 'spec_name': (lc('soGUICore.soGUI.STRING_1402_80')), 'spec_points': 1600, 'id': 'eq_pistol'})
        return

    def updateBasicSkills(self):
        self.skillsGUI.updateBasicSkills()
        return

    def setSpecData(self, spec_tree, spec):
        self.skillsGUI.setSpec(spec_tree, spec)
        return

    def updateAdvancedSkills(self):
        self.skillsGUI.updatetAdvancedSkills()
        return

    def updateActiveSkills(self):
        self.skillsGUI.updateActiveSkills()
        return

    def setClanTraderData(self, data):
        if self.clanGUI is None:
            self.clanGUI = soClanScreen2(GUI.Window())
            self.clanGUI.onBound()
        self.clanTradeDataSection = data
        self.clanGUI.update()
        return

    def clanData(self, data):
        if self.clanGUI is None:
            self.clanGUI = soClanScreen2(GUI.Window())
            self.clanGUI.onBound()
        self.clanDataSection = data
        self.clanGUI.update()
        return

    def setMembers(self, data):
        if self.clanGUI is None:
            self.clanGUI = soClanScreen2(GUI.Window())
            self.clanGUI.onBound()
        self.clanGUI.setMembers(data)
        return

    def addMembers(self, data):
        if self.clanGUI is None:
            self.clanGUI = soClanScreen2(GUI.Window())
            self.clanGUI.onBound()
        self.clanGUI.addMembers(data)
        return

    def delMembers(self, data):
        if self.clanGUI is None:
            self.clanGUI = soClanScreen2(GUI.Window())
            self.clanGUI.onBound()
        self.clanGUI.delMembers(data)
        return

    def setTutorialData(self, data):
        if self.tutorialGUI is None:
            self.tutorialGUI = soTutorialGUI(GUI.Window())
            self.tutorialGUI.onBound()
        if data == 1:
            data = [[100, 100],
             u'PLACEHOLDER<n>TUTORIAAAAAAAAAAAL TIMEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!']
        self.tutorialDataSection = data
        self.tutorialGUI.update()
        return

    def setSapceNames(self, data):
        self.spaces = {}
        for item in data:
            mappath = item.SpaceName
            if mappath in MAPLIST:
                mapName = MAPLIST[mappath]
            else:
                mapName = mappath.rstrip('spaces/')
            self.spaces[item.SpaceID] = [
             mappath, mapName]

        return

    def getSpaceName(self, spaceID):
        return self.spaces.get(spaceID, (None, None))

    def setCharacterEffect(self, id, data):
        if self.effectsFrame is None:
            self.effectsFrame = soCharEffectsGUI(GUI.Window())
            self.effectsFrame.onBound()
        self.effectsFrame.setEffect(id, data)
        return

    def delCharacterEffect(self, id=None):
        if self.effectsFrame is None:
            self.effectsFrame = soCharEffectsGUI(GUI.Window())
            self.effectsFrame.onBound()
        if id is None or id < 0:
            self.effectsFrame.clearEffects()
        else:
            return self.effectsFrame.delEffect(id)
        return

    def setVisionMode(self, mode=soGUI.soVisionModes.MODE_NORMAL, data=None):
        if mode == soGUI.soVisionModes.MODE_SNIPER:
            if self.sniperVision is None:
                self.sniperVision = soSniperVision(GUI.Window())
                self.sniperVision.onBound()
            self.sniperVision.show()
            self.sniperVision.setScope(data)
        if mode == soGUI.soVisionModes.MODE_NORMAL:
            if self.sniperVision:
                self.sniperVision.hide()
        return

    def setSkillInfo(self, info):
        if self.skillsGUI is not None:
            if isinstance(BigWorld.player(), Avatar.PlayerAvatar):
                self.skillsGUI.setInfo(info)
        return

    def setQuestDescription(self, descr):
        if self.questLogGUI is not None:
            if isinstance(BigWorld.player(), Avatar.PlayerAvatar):
                self.questLogGUI.setDescription(descr)
        return

    def weaponSelect(self, data):
        self.currentWeaponDataSection = data
        if self.weaponFlasher is None:
            self.weaponFlasher = soWeaponFlash(GUI.Window())
            self.weaponFlasher.onBound()
            self.weaponFlasher.show()
        if self.weaponFlasher is not None:
            self.weaponFlasher.update()
        return

    def quickSlotsData(self, data):
        self.quickSlotsDataSection = data
        if self.quickSlots is None:
            self.quickSlots = soQuickSlotsBar(GUI.Window())
            self.quickSlots.onBound()
        if self.quickSlots is not None:
            self.quickSlots.update()
        return

    def setActionBarData(self, data):
        if self.actionBar is None:
            self.actionBar = soActionBar(GUI.Window())
            self.actionBar.onBound()
        self.actionBarDataSection = data
        self.actionBar.update()
        return

    def questLogData(self, data, mode=soTPCQuestLog.MODE_CURRENT):
        self.questLogDataSection['mode'] = mode
        if mode == soTPCQuestLog.MODE_CURRENT:
            self.questLogDataSection['quests'] = data
        elif mode == soTPCQuestLog.MODE_COMPLETED:
            self.questLogDataSection['completed'] = data
        if self.questLogGUI is None:
            self.questLogGUI = soTPCQuestLog(GUI.Window())
            self.questLogGUI.onBound()
        self.questLogGUI.update()
        return

    def setInteractionMode(self, mode):
        if self.interactionGUI is None:
            self.interactionGUI = soInteractionMarker(GUI.Window())
            self.interactionGUI.onBound()
        if self.interactionGUI is not None:
            self.interactionGUI.setInteractionMode(mode)
        return

    def setAnomalyThreat(self, threatLevel):
        return
        if self.anomalyMeter is None:
            self.anomalyMeter = soAnomalyMeter(GUI.Window())
            self.anomalyMeter.onBound()
            self.anomalyMeter.show()
            self.anomalyMeter.setThreatLevel(threatLevel)
        elif self.anomalyMeter.component.visible == False:
            self.anomalyMeter.show()
        self.anomalyMeter.setThreatLevel(threatLevel)
        return

    def setObjectiveData(self, data):
        if self.objectivesGUI is None:
            self.objectivesGUI = soObjectivesGUI2(GUI.Window())
            self.objectivesGUI.onBound()
        self.objectiveDataSection = data
        self.objectivesGUI.update()
        return

    def setItemCacheData(self, data):
        if self.itemCacheGUI is None:
            self.itemCacheGUI = soItemCacheScreen(GUI.Window())
            self.itemCacheGUI.onBound()
        self.itemCacheDataSection = data
        self.itemCacheGUI.update()
        return

    def setWarehouseData(self, data):
        if self.WarehouseGUI is None:
            self.WarehouseGUI = soWarehouse(GUI.Window())
            self.WarehouseGUI.onBound()
        self.warehouseDataSection = data
        self.WarehouseGUI.update()
        return

    def setListWantedDataSection(self, data):
        self.listWantedDataSection = data
        if self.questLogGUI:
            self.questLogGUI.updateWanted()
        return

    def setItemCacheDataUserFire(self, data):
        if self.userFireGUI is None:
            self.userFireGUI = soUserFireCacheScreen(GUI.Window())
            self.userFireGUI.onBound()
        self.itemCacheDataUserFireSection = data
        self.userFireGUI.update()
        return

    def setArtifactQTEData(self, data):
        self.artifactQTEDataSection = data
        self.artifactQTE.update()
        return

    def setChatConsoleData(self, data):
        if self.chatConsole is None:
            self.chatConsole = soChatConsole3(GUI.Window())
            self.chatConsole.onBound()
        self.chatPrint(1, data)
        return
        self.chatConsoleDataSection = data
        self.chatConsole.update()

    def configChatConsole(self, data):
        if self.chatConsole is None:
            self.chatConsole = soChatConsole3(GUI.Window())
            self.chatConsole.onBound()
        self.chatConsole.applyConfig(data)
        return

    def chatPrint(self, mask=1, msg=u'place_holder_Here', timeStamp=u''):
        if self.chatConsole is None:
            self.chatConsole = soChatConsole3(GUI.Window())
            self.chatConsole.onBound()
        self.chatConsole.addMessage(mask, msg, timeStamp)
        return

    def chatClear(self):
        if self.chatConsole is None:
            self.chatConsole = soChatConsole3(GUI.Window())
            self.chatConsole.onBound()
        self.chatConsole.clearConsole()
        return

    def chatPromt(self, txt, replaceTag=False, eraseOld=False, activating=False):
        if self.chatConsole is None:
            self.chatConsole = soChatConsole3(GUI.Window())
            self.chatConsole.onBound()
        self.chatConsole.setPromt(txt, replaceTag, eraseOld, activating)
        return

    def setQueueData(self, data):
        if self.queueGUI is None:
            self.queueGUI = soQueueScreen(GUI.Window())
            self.queueGUI.onBound()
        self.queueDataSection = data
        self.queueGUI.update()
        return

    def setGameMode(self, mode):
        if self.currentMode == mode:
            return
        self.currentMode = mode
        self.msgBoxMgr.onGameModeChange(self.currentMode)
        if mode == self.GAMEMODE_LOGIN:
            self.setLayerMode(self.LAYER_MODE_MENU)
        elif mode == self.GAMEMODE_INGAME:
            self.setLayerMode(self.LAYER_MODE_INGAME)
            self.showHealthBar(True)
        return

    def setHealthData(self, data):
        self.healthDataSection = data
        self.healthBarGUI.update()
        return

    def setCharacterManagerData(self, data, target=soCharacterManagmentGUI.MODE_SELECT):
        if self.characterManager is None:
            self.characterManager = soCharacterManagmentGUI(GUI.Window())
            self.characterManager.onBound()
        if target == soGUI.soCharacterManagmentGUI.MODE_SELECT:
            self.characterManagerDataSection['selection'] = data
        elif target == soGUI.soCharacterManagmentGUI.MODE_CREATE:
            self.characterManagerDataSection['creation'] = data
        self.characterManager.update()
        return

    def setCharMakerDescription(self, first=None, third=None):
        """
                GUICore::setCharMakerDescription(first = None, third = None)
                this method assigns a text to textfields in the character maker GUI
                first goes to 1st screen and third to 3rd one.
                arguments should be None if you don't want to change the current text
                """
        if first is not None:
            self.charMaker.setFirstDescription(first)
        if third is not None:
            self.charMaker.setThirdDescription(third)
        return

    def setCharMakerNickHint(self, txt=u'', type=CHAR_MAKER.HINT_TYPE_NORMAL):
        """
                GUICore::setCharMakerNickHint(txt = u'', type = CHAR_MAKER.HINT_TYPE_NORMAL)
                use this method to set a text of the hint label under the nickname editfield in character maker GUI
                txt is the unicode string to show
                type is used to determine what color should be assigned to label, you can find all possible values in common/gui_const/CHAR_MAKER.py
                """
        self.charMaker.setNicknameHint(txt, type)
        return

    def setCharMakerNickInputValidator(self, valid_callable=None):
        """
                GUICore::setCharMakerNickInputValidator(valid_callable = None)
                this method sets the input validity callback for nickname editfield in character maker GUI
                callback must be None (all input is considered correct) or callable of the following signature:
                callback(newStr, wholeText, offset): return bool
                wheres newStr is the unicode string that is being added, wholeText is the unicode string that is allready present in the editfield and offset is a position where newStr is being added
                callback must return True to allow newStr to be added or False to ignore newStr
                """
        self.charMaker.setNicknameValidator(valid_callable)
        return

    def setCharSummary(self, data=None):
        """
                GUICore::setCharSummary(data = None)
                this method sets the strings for character summary panel (rightmost block of text) for character maker and character picker GUIs
                data must be None or list of the following form:
                [
                ["caption", "value"]
                ...
                ["caption", "value"]
                ]
                """
        self.charPicker.setCharacterSummary(data)
        self.charMaker.setCharacterSummary(data)
        return

    def setSystemData(self, data):
        self.systemDataSection = data
        return

    def setCraftData(self, data):
        if self.craftGUI is None:
            self.craftGUI = soCraftGUI(GUI.Window())
            self.craftGUI.onBound()
        self.craftDataSection = data
        self.craftGUI.update()
        return

    def setLoginData(self, data):
        self.loginDataSection = data
        self.loginGUI.update()
        return

    def setGPSdata(self, data):
        if self.gpsGUI is None:
            self.gpsGUI = soGPSMap(GUI.Window())
            self.gpsGUI.onBound()
        self.gpsDataSection = data
        self.gpsGUI.update()
        return

    def setCastBarData(self, data):
        if self.castBar is None:
            self.castBar = soCastBar(GUI.Window())
            self.castBar.onBound()
        if data[0] == 'RUN':
            self.castBar.runCast(data[1], data[2], data[3])
        elif data[0] == 'SET':
            self.castBar.setCastTime(data[1], data[2])
        elif data[0] == 'INT':
            self.castBar.interruptCast(data[1])
        elif data[0] == 'CNC':
            self.castBar.cancelCast()
        return

    def alterMsgBox(self, id, data, activate=False):
        if not self.dlgBoxes.has_key(id):
            return
        if isinstance(data, dict):
            if data.has_key('msg'):
                self.dlgBoxes[id].setMsg(data['msg'])
            if data.has_key('pict'):
                self.dlgBoxes[id].setPicture(data['pict'])
            if data.has_key('caption'):
                self.dlgBoxes[id].setCaption(data['caption'])
        if activate:
            self.dlgBoxes[id].activate()
        return

    def setTradeData(self, data):
        if self.tradeGUI is None:
            self.tradeGUI = soTradeGUI2(GUI.Window())
            self.tradeGUI.onBound()
        self.vendorDataSection = data
        self.tradeGUI.update()
        return

    def setBulletinBoardData(self, data):
        if self.soBulletinBoard is None:
            self.soBulletinBoard = soGUI.soBulletinBoard.soBulletinBoard(GUI.Window())
            self.soBulletinBoard.onBound()
        self.bulletinBoardDataSection = data
        self.soBulletinBoard.update()
        return

    def setBulletinBoardShopData(self, data):
        if self.soBulletinBoard is None:
            self.soBulletinBoard = soGUI.soBulletinBoard.soBulletinBoard(GUI.Window())
            self.soBulletinBoard.onBound()
        self.bulletinBoardShopDataSection = data
        self.soBulletinBoard.updateShop()
        return

    def setBulletinBoardHunterData(self, data):
        if self.soBulletinBoard is None:
            self.soBulletinBoard = soGUI.soBulletinBoard.soBulletinBoard(GUI.Window())
            self.soBulletinBoard.onBound()
        self.bulletinBoardHunterDataSection = data
        self.soBulletinBoard.updateHunter()
        return

    def setBaseTraderData(self, data):
        if self.DonateBase is None:
            self.DonateBase = DonatebaseGUI(GUI.Window())
            self.DonateBase.onBound()
        self.DonateBase.displayListDonateBase(data)
        return

    def setDeposit(self, value):
        self.DonateBase.setDeposit(value)
        return

    def setDetailViewStakeData(self, data):
        if self.DetailViewStakeGUI is None:
            self.DetailViewStakeGUI = DetailViewStakeGUI(GUI.Window())
            self.DetailViewStakeGUI.onBound()
        self.DetailViewStakeGUI.updateInfo(data)
        return

    def setClanManagerNPCData(self, data):
        if self.ClanManagerNPCGUI is None:
            self.ClanManagerNPCGUI = ClanManagerNPCGUI(GUI.Window())
            self.ClanManagerNPCGUI.onBound()
        self.ClanManagerNPCGUI.update(data)
        return

    def setOptionsData(self, data):
        if self.optionsGUI is None:
            self.optionsGUI = soOptionsGUI3(GUI.Window())
            self.optionsGUI.onBound()
        self.optionsDataSection = data
        self.optionsGUI.update()
        return

    def setPartyData(self, data):
        return
        self.partyDataSection = data
        self.partyGUI.update()

    def setPartyMember(self, id, data):
        self.partyGUI.setMember(id, data)
        return

    def delPartyMember(self, id):
        if id is None:
            self.partyGUI.clearMembers()
            return
        else:
            self.partyGUI.delMember(id)
            return

    def clearPartyMembers(self):
        self.partyGUI.clearMembers()
        return

    def setPartyMemberEffect(self, mmbrID, effID, data):
        self.partyGUI.setMemberEffect(mmbrID, effID, data)
        return

    def delPartyMemberEffect(self, mmbrID, effID):
        if effID is None:
            self.partyGUI.clearMemberEffects(mmbrID)
        return

    def showPartyFramesEffects(self, doShow=True):
        self.partyGUI.showPartyFramesEffects(doShow)
        return

    def addPPEffect(self, ppName):
        return self.ppRenderer.addPP(ppName)

    def delPPEffect(self, ppName):
        return self.ppRenderer.removePP(ppName)

    def clearPPEffects(self):
        self.ppRenderer.removeAll()
        return

    def addSysPPEffect(self, ppName):
        return self.ppRenderer.addSysPP(ppName)

    def delSysPPEffect(self, ppName):
        return self.ppRenderer.removeSysPP(ppName)

    def clearSysPPEffects(self):
        self.ppRenderer.removeAllSys()
        return

    def addObjective(self, id, priority, data):
        return self.objectiveTrackerGUI.addObjective(id, priority, data)

    def setObjective(self, id, data):
        return self.objectiveTrackerGUI.setObjective(id, data)

    def delObjective(self, id):
        return self.objectiveTrackerGUI.delObjective(id)

    def clearObjectives(self):
        self.objectiveTrackerGUI.clearObjectives()
        return

    def setCharPickerCharacter(self, charID, data):
        if self.charPicker is None:
            self.charPicker = soCharacterPickGUI(GUI.Window())
            self.charPicker.onBound()
        self.charPicker.setCharacter(charID, data)
        return

    def delCharPickerCharacter(self, charID):
        if self.charPicker is None:
            self.charPicker = soCharacterPickGUI(GUI.Window())
            self.charPicker.onBound()
        self.charPicker.removeCharacter(charID)
        return

    def setCharPickerCharInfo(self, data):
        """
                soGUICore::setCharPickerCharInfo has the exactly same signature as soGUICore::setCharSummary
                see it's docstrings for reference
                """
        if self.charPicker is None:
            self.charPicker = soCharacterPickGUI(GUI.Window())
            self.charPicker.onBound()
        self.charPicker.setCharacterSummary(data)
        return

    def clearCharPickerCharacters(self):
        if self.charPicker is None:
            self.charPicker = soCharacterPickGUI(GUI.Window())
            self.charPicker.onBound()
        self.charPicker.clearCharacters()
        return

    def prepareInventoryIcons(self, iconTuple):
        try:
            BigWorld.loadResourceListBG(tuple(iconTuple), self.onIconsLoaded)
        except:
            print 'error occured: engine can`t preload 1 recource unit, you must pass at least 2 '

        return

    def onIconsLoaded(self, resourceRefs):
        self.iconTextures = resourceRefs
        return

    def GUILock(self, doLock=True, msg=u'', intercepting_callback=None):
        if not hasattr(self.generalLayer, 'GUILocker'):
            (sW, sH) = BigWorld.screenSize()
            cmp = GUI.Window('soGUI/maps/Colours/white.tga')
            cmp.colour = (0, 0, 0, 127)
            cmp.materialFX = 'BLEND'
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.widthMode = cmp.heightMode = 'CLIP'
            cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
            cmp.width = cmp.height = 2.0
            cmp.position = (0.0, 0.0, 0.0)
            cmp.tiled = True
            cmp.tileHeight = 1
            cmp.tileWidth = 1
            cmp.moveFocus = True
            cmp.crossFocus = True
            cmp.mouseButtonFocus = True
            self.generalLayer.addChild(cmp, 'GUILocker')
            cmp = GUI.Simple('soGUI/maps/loadingScreen/loadingCircle/loadingCircle.texanim')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.height = 41
            cmp.width = 41
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (sW / 2.0, sH / 2.0, 0.2)
            self.generalLayer.GUILocker.addChild(cmp, 'ldrAnim')
            cmp = GUI.Text('')
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'TOP'
            cmp.position = (sW / 2.0, sH / 2.0 + 30, 0.1)
            self.generalLayer.GUILocker.addChild(cmp, 'msg')
        if doLock:
            self.generalLayer.GUILocker.visible = True
        else:
            self.generalLayer.GUILocker.visible = False
        self.generalLayer.GUILocker.msg.text = msg
        self.GUILockerCallback = intercepting_callback
        return

    def showTimer(self, secs, msg=u'', doShow=True):
        if not hasattr(self.worldLayer, 'genericTimer'):
            (sW, sH) = BigWorld.screenSize()
            cmp = GUI.Text('')
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'TOP'
            cmp.position = (sW / 2.0, 10, 0.5)
            self.worldLayer.addChild(cmp, 'genericTimer')
        self.genericTimerSecs = secs
        if doShow:
            self.worldLayer.genericTimer.visible = True
            if self.timerCheckCoroutine is None:
                self.timerCheckCoroutine = self.genericTimerChecker(msg)
                self.timerCheckCoroutine.run()
            else:
                self.timerCheckCoroutine.stop()
                self.timerCheckCoroutine = self.genericTimerChecker(msg)
                self.timerCheckCoroutine.run()
        else:
            self.worldLayer.genericTimer.visible = False
            if self.timerCheckCoroutine is not None:
                self.timerCheckCoroutine.stop()
                self.timerCheckCoroutine = None
        return

    def showConfirmWindow(self, needConfirmIDCount, needConfirmIDUser, msg):
        if self.confirmWindow is None:
            self.confirmWindow = soGUI.confirmWindowGUI.confirmWindowGUI(GUI.Window())
            self.confirmWindow.onBound()
        if needConfirmIDUser:
            self.confirmWindow.show(needConfirmIDCount, needConfirmIDUser, msg)
            self.menuLayer.visible = False
        else:
            self.hideConfirmWindow()
        return

    def hideConfirmWindow(self):
        if self.confirmWindow is not None:
            self.confirmWindow.hide()
        if self.lastLayerMode == self.LAYER_MODE_MENU:
            self.menuLayer.visible = True
        elif self.lastLayerMode == self.LAYER_MODE_INGAME:
            self.menuLayer.visible = False
        return

    def showContextMenu(self, iid, actions):
        self.contextState = True
        if self.toolTipState:
            self.toolTip.hide()
        if self.contextMenu is None:
            self.contextMenu = soContextMenuComponent(GUI.Window(), actions, iid)
        else:
            self.contextMenu.showMenu(actions, iid)
        return

    def showDialogueGUI(self, doShow=True):
        if self.dialogueGUI is None:
            self.dialogueGUI = soDialogueGUI2(GUI.Window())
            self.dialogueGUI.onBound()
        if doShow:
            self.dialogueGUI.show()
        else:
            self.dialogueGUI.hide()
        return

    def showPvPStats(self, doShow=True):
        if self.pvpStatsGUI is None:
            self.pvpStatsGUI = soPvPStats(GUI.Window())
            self.pvpStatsGUI.onBound()
        if doShow:
            self.pvpStatsGUI.show()
        else:
            self.pvpStatsGUI.hide()
        return

    def showToolTip(self, text, icon='', autoWidth=True, style=soToolTipWindow2.STYLE_CURSOR, delay=1.0):
        if self.contextState:
            return
        else:
            self.toolTipState = True
            if self.toolTip is None:
                self.toolTip = soToolTipWindow2(GUI.Window())
            self.toolTip.setStyle(style)
            self.toolTip.setData(text)
            self.toolTip.show(delay)
            return

    def showCharScreen(self, doShow=True):
        if self.charScreen is None:
            self.charScreen = soCharacterScreen2(GUI.Window())
            self.charScreen.onBound()
        if doShow:
            self.charScreen.show()
        else:
            self.charScreen.hide()
        return

    def showSkillsGUI(self, doShow=True):
        if self.skillsGUI is None:
            self.skillsGUI = soSkillScreen2(GUI.Window())
            self.skillsGUI.onBound()
            self.skillsGUI.update()
        self.systemMenu.refreshPoints()
        if doShow:
            self.skillsGUI.show()
        else:
            self.skillsGUI.hide()
        return

    def showPCTrade(self, doShow=True):
        if self.playerTrade is None:
            self.playerTrade = soPCTradeScreen2(GUI.Window())
            self.playerTrade.onBound()
        if doShow:
            self.playerTrade.show()
        else:
            self.playerTrade.hide()
        return

    def showTabletPC(self, doShow=True, interface=soTabletScreen.INTERFACE_MAIN):
        if self.tabletPC is None:
            self.tabletPC = soTabletScreen(GUI.Window())
            self.tabletPC.onBound()
        if doShow:
            self.tabletPC.show()
            self.tabletPC.showInterface(interface)
        else:
            self.tabletPC.hide()
        return

    def showClanGUI(self, doShow=True):
        if self.clanGUI is None:
            self.clanGUI = soClanScreen2(GUI.Window())
            self.clanGUI.onBound()
        if doShow:
            self.clanGUI.show()
        else:
            self.clanGUI.hide()
        return

    def showLoaderGUI(self, guiType=soProgressBars.TYPE_SPACE, distance=300, timeout=100, spaceName='', doShow=True, waitForReset=False):
        if guiType == soProgressBars.TYPE_SPACE:
            if self.spaceLoaderGUI is None:
                self.spaceLoaderGUI = soSpaceProgressBar(GUI.Window())
                self.spaceLoaderGUI.onBound()
            if doShow:
                self.spaceLoaderGUI.setDistance(distance)
                self.spaceLoaderGUI.setTimeout(timeout)
                self.spaceLoaderGUI.setSpaceName(spaceName)
                self.spaceLoaderGUI.setWaitMode(waitForReset)
                self.spaceLoaderGUI.show()
            else:
                self.spaceLoaderGUI.hide()
        elif guiType == soProgressBars.TYPE_INGAME:
            if self.ingameLoaderGUI is None:
                self.ingameLoaderGUI = soIngameProgressBar(GUI.Gobo(''))
                self.ingameLoaderGUI.onBound()
            if doShow:
                self.ingameLoaderGUI.setDistance(distance)
                self.ingameLoaderGUI.setTimeout(timeout)
                self.ingameLoaderGUI.show()
            else:
                self.ingameLoaderGUI.hide()
        elif guiType == soProgressBars.TYPE_DUMMY:
            if self.dummyLoaderGUI is None:
                self.dummyLoaderGUI = soDummyProgressBar(GUI.Window())
                self.dummyLoaderGUI.onBound()
            if doShow:
                self.dummyLoaderGUI.setSpaceName(spaceName)
                self.dummyLoaderGUI.show()
            else:
                self.dummyLoaderGUI.hide()
        return

    def showDamage(self, severity, direction, dmgType):
        """
                severity юЄ 0.0 фю 1.0
                direction юс· тыхэ√ т ъырёёх soIncomingDamageGUI
                """
        if self.incomingDmgGUI is None:
            self.incomingDmgGUI = soIncomingDamageGUI(GUI.Window())
            self.incomingDmgGUI.onBound()
        self.incomingDmgGUI.show(severity, direction, dmgType)
        return

    def testChat(self):
        x = lc('soGUICore.soGUI.STRING_2458_6')
        BigWorld.player().systemChatline(x)
        return

    def testHLink(self):
        hlink = soHyperLinkComponent(GUI.Text('blah blah'))
        cmp = hlink.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0.0, 0.0, 0.0)
        self.generalLayer.addChild(cmp, 'hlink')
        hlink.initVSC('soGUI/visual_styles/hlink_default.xml')
        hlink.setVisualState('normal')
        hlink.setToolTip('hlink_test')
        hlink.onBound()
        return

    def testAnim(self):
        cmp = GUI.Simple('soGUI/maps/loadingScreen/gears/gears.texanim')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.height = 200
        cmp.width = 200
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0.0, 0.0, 0.0)
        self.generalLayer.addChild(cmp, 'animTest')
        return

    def testEdit(self):
        testEdit = soEditBox(GUI.Window(), width=400, height=300)
        cmp = testEdit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.position = (0.0, 0.5, 0.0)
        self.generalLayer.addChild(cmp, 'testEdit')
        testEdit.onBound()
        return testEdit

    def chatStress(self):
        for i in xrange(500):
            self.chatPrint(1, lc('soGUICore.soGUI.STRING_2500_23'))

        return

    def testInvite(self):
        from gui_jokes import askUserYesNoDelayDeafultNo
        dlg = askUserYesNoDelayDeafultNo(u'placeholder', u'2233' + lc('soGUICore.soGUI.STRING_2505_61') + u'zzz2' + lc('soGUICore.soGUI.STRING_2505_150'))
        return

    def testTxtField(self):
        testTxt = soTextField3(GUI.Window(), height=500, textWidth=-1, hScroll=False, vScroll=True, hideScroll=False, borderWidth=0, vOffset=0, hOffset=0, textureless=False, autosize=False, width=400, maxAppends=200)
        cmp = testTxt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.position = (0.0, 0.0, 0.0)
        self.generalLayer.addChild(cmp, 'txtFld')
        testTxt.onBound()
        for i in xrange(150):
            testTxt.addText((u'<color=255000255255>Damge {number}, yeah right, take that !!!!').format(number=i))

        return testTxt

    def testTable2(self):
        memberTable_captionDS = {'font': 'ruRU_calibri_default.font', 
           'color': (255, 255, 255, 0), 
           'hoverColor': (255, 255, 255, 0), 
           'selectColor': (255, 255, 255, 0), 
           'toolTipID': None, 
           'contentColor': (175, 166, 112, 255), 
           'contentColorHover': (175, 166, 112, 255), 
           'contentColorSelect': (175, 166, 112, 255)}
        memberTable_dataDS = {'font': 'ruRU_calibri_default.font', 
           'color': (255, 255, 255, 0), 
           'hoverColor': (255, 255, 255, 0), 
           'selectColor': (28, 28, 28, 255), 
           'toolTipID': None, 
           'contentColor': (175, 166, 112, 255), 
           'contentColorHover': (249, 233, 137, 255), 
           'contentColorSelect': (249, 233, 137, 255)}
        rows = []
        rows.append([(25, 'TOP'), {'name': {'props': (soTableElemPropsStructure(dataStyles=memberTable_captionDS)), 'data': {'text': (lc('GUI.Legacy.CLANMATE_NAME'))}}, 'rank': {'props': (soTableElemPropsStructure(dataStyles=memberTable_captionDS)), 'data': {'text': (lc('GUI.Legacy.CLANMATE_RANK'))}}, 'status': {'props': (soTableElemPropsStructure(dataStyles=memberTable_captionDS)), 'data': {'text': (lc('GUI.Legacy.CLANMAE_STATE'))}}}])
        for i in xrange(1000):
            rowData = [
             (25, 'MIDDLE'), {'name': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': (str(i))}}, 'rank': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': (str(i))}}, 'status': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': (str(i))}}}]
            rows.append(rowData)

        tbl = soTableComponent2(GUI.Window(), soTablePropsStructure(tableHeight=408, tableWidth=786, innerBorderColor=(85,
                                                                                                                       85,
                                                                                                                       85,
                                                                                                                       255)))
        cmp = tbl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (3, 71, 0.0)
        self.menuLayer.addChild(cmp, 'testTable')
        tbl.onBound()
        tbl.addCols([['name', 294], ['rank', 190], ['status', 275]])
        tbl.addRows(rows)
        idx = tbl.getRowIndexByValue({'text': u'500'}, 'name')
        rowData = [
         (25, 'MIDDLE'), {'name': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'test100500'}}, 'rank': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'test100500'}}, 'status': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'test100500'}}}]
        tbl.rewriteRow(idx, rowData)
        tbl.removeRows([idx])
        return

    def testMyFont(self):
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'test.font'
        cmp.colourFormatting = True
        cmp.multiline = True
        cmp.text = lc('soGUICore.soGUI.STRING_2551_13')
        cmp.position = (0.0, 0.5, 0.0)
        self.menuLayer.addChild(cmp, 'testMyFont')
        cmp = GUI.Simple('soGUI/maps/Colours/testFont.bmp')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 1e-06)
        self.menuLayer.addChild(cmp, 'back')
        return

    def testMatFX(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0.0, 0.0, 0.0)
        cmp.width = 300
        cmp.height = 300
        self.menuLayer.addChild(cmp, 'testMFX')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/Colours/white.tga'
        cmp.position = (150, 150, 0.1)
        cmp.width = 100
        cmp.height = 100
        self.menuLayer.testMFX.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 0, 0, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/Colours/white.tga'
        cmp.position = (150, 150, 0.0)
        cmp.width = 90
        cmp.height = 100
        self.menuLayer.testMFX.addChild(cmp)
        return

    def testDDL(self):
        ddl = soDropDownList2(GUI.Window(), VS='soGUI/visual_styles/pdaDDL.xml')
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (0, 0, 0.1)
        self.generalLayer.addChild(cmp, 'ddlTest')
        elems = [
         [
          1, u'PLACEHOLDER'],
         [
          2, u'PLACEHOLDER'],
         [
          3, u'PLACEHOLDER']]
        ddl.addElements(elems)
        ddl.setSelectionByValue(2)
        return

    def testTable(self, testType=0):
        self.memberTable_captionDS = {'font': 'ruRU_calibri_default.font', 
           'color': (255, 255, 255, 0), 
           'hoverColor': (255, 255, 255, 0), 
           'selectColor': (255, 255, 255, 0), 
           'toolTipID': None, 
           'contentColor': (175, 166, 112, 255), 
           'contentColorHover': (175, 166, 112, 255), 
           'contentColorSelect': (175, 166, 112, 255)}
        memberTable_dataDS = {'font': 'ruRU_calibri_default.font', 
           'color': (255, 255, 255, 0), 
           'hoverColor': (255, 255, 255, 0), 
           'selectColor': (28, 28, 28, 255), 
           'toolTipID': None, 
           'contentColor': (175, 166, 112, 255), 
           'contentColorHover': (249, 233, 137, 255), 
           'contentColorSelect': (249, 233, 137, 255)}
        if testType == 0:
            tbl = soTableComponent2(GUI.Window(), soTablePropsStructure(tableHeight=545, tableWidth=480, outerBorderWidth=2, innerBorderColor=(85,
                                                                                                                                               85,
                                                                                                                                               85,
                                                                                                                                               255)))
            cmp = tbl.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.position = (10, 17, 0.0)
            self.menuLayer.addChild(cmp, 'tableTest')
            tbl.onBound()
            tbl.addCols([['col1', 200], ['col2', 300], ['col3', 480]])
            rows = []
            rows.append([(43, 'TOP'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=self.memberTable_captionDS, spanLeft=1, spanDown=1)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=self.memberTable_captionDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(35, 'TOP'), {'col3': {'props': (soTableElemPropsStructure(dataStyles=self.memberTable_captionDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(25, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'findME'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(25, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, dataType=5)), 'data': {'text': u'pushme', 'btnVS': 'soGUI/visual_styles/defaultBtnMedium.xml'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(25, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, spanLeft=1, spanDown=2, rights=['READ', 'EDIT'])), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(85, 'MIDDLE'), {'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(85, 'MIDDLE'), {'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(85, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, spanDown=1, rights=[])), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(85, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, dataType=1)), 'data': {'text': u'', 'boolState': True}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo2'}}}])
            rows.append([(85, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, dataType=1)), 'data': {'text': u'', 'boolState': False}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo3'}}}])
            rows.append([(85, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo4'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(25, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, spanLeft=1)), 'data': {'text': u'PLACEHOLDERo5'}}}])
            rows.append([(25, 'BOTTOM'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, spanLeft=1, spanDown=1)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(25, 'BOTTOM'), {'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(25, 'BOTTOM'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'bottom1'}}}])
            tbl.addRows(rows)
        elif testType == 1:
            tbl = BWPersonality.GUICore.menuLayer.tableTest.script
            tbl.alterElem('col2', 2, soTableElemPropsStructure(dataStyles=memberTable_dataDS), {'text': (lc('soGUICore.soGUI.STRING_2721_97'))})
        elif testType == 2:
            row = [
             (45, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': (lc('soGUICore.soGUI.STRING_2723_122'))}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': (lc('soGUICore.soGUI.STRING_2724_104'))}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': (lc('soGUICore.soGUI.STRING_2725_104'))}}}]
            tbl = BWPersonality.GUICore.menuLayer.tableTest.script
            tbl.rewriteRow(2, row)
        elif testType == 3:
            tbl = BWPersonality.GUICore.menuLayer.tableTest.script
            rows = []
            rows.append([(25, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'findME'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(25, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, dataType=5)), 'data': {'text': u'pushme', 'btnVS': 'soGUI/visual_styles/defaultBtnMedium.xml'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(25, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, spanLeft=1, spanDown=2, rights=['READ', 'EDIT'])), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(85, 'MIDDLE'), {'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(85, 'MIDDLE'), {'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(85, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, spanDown=1, rights=[])), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(85, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, dataType=1)), 'data': {'text': u'', 'boolState': True}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo2'}}}])
            rows.append([(85, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, dataType=1)), 'data': {'text': u'', 'boolState': False}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo3'}}}])
            rows.append([(85, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo4'}}, 'col3': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}}])
            rows.append([(25, 'MIDDLE'), {'col1': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS)), 'data': {'text': u'PLACEHOLDERo1'}}, 'col2': {'props': (soTableElemPropsStructure(dataStyles=memberTable_dataDS, spanLeft=1)), 'data': {'text': u'PLACEHOLDERo5'}}}])
            tbl.addRows(rows)
        elif testType == 4:
            tbl = BWPersonality.GUICore.menuLayer.tableTest.script
        return

    def setBestCursor(self):

        def gui_visible():
            return bool(self.skillsGUI and self.skillsGUI.component.visible or self.packageGUI and self.packageGUI.component.visible or self.privateStoreGUI and self.privateStoreGUI.component.visible or self.ingameMenuGUI and self.ingameMenuGUI.component.visible or self.playerTrade and self.playerTrade.component.visible or self.charScreen and self.charScreen.component.visible or self.clanGUI and self.clanGUI.component.visible or self.questLogGUI and self.questLogGUI.component.visible or self.itemCacheGUI and self.itemCacheGUI.component.visible or self.userFireGUI and self.userFireGUI.component.visible or self.WarehouseGUI and self.WarehouseGUI.component.visible or self.startSaleGUI and self.startSaleGUI.component.visible or self.startSubmitOffender and self.startSubmitOffender.component.visible or self.tabletPC and self.tabletPC.component.visible or self.dialogueGUI and self.dialogueGUI.component.visible or self.optionsGUI and self.optionsGUI.component.visible or self.craftGUI and self.craftGUI.component.visible or self.helpGUI and self.helpGUI.component.visible or self.soBulletinBoard and self.soBulletinBoard.component.visible or self.soBaseTrader and self.soBaseTrader.component.visible or self.tradeGUI and self.tradeGUI.component.visible or self.chatConsole and (self.chatConsole.typing or self.chatConsole.settingsWnd.visible) or self.inventoryGUI and self.inventoryGUI.component.visible or self.gpsGUI and self.gpsGUI.component.visible or self.friendList and self.friendList.component.visible or self.DonateBase and self.DonateBase.component.visible or self.DetailViewStakeGUI and self.DetailViewStakeGUI.component.visible or self.ClanManagerNPCGUI and self.ClanManagerNPCGUI.component.visible or self.DonateBase and self.DonateBase.component.visible or self.selectMap and self.selectMap.script.visible or self.shoiceTeamWindow and self.shoiceTeamWindow.isVisible() or self.pvpScoreBar and self.pvpScoreBar.scoreBarVisible() or self.QuitMenu and self.QuitMenu.component.visible)

        gv = gui_visible()
        mouse_cursor = self.menuLayer.visible or not isinstance(BigWorld.player(), Avatar.PlayerAvatar) or gv or self.mouseAltMode
        if gv and self.mouseAltMode:
            self.mouseAltMode = False
        BWPersonality.game.set_cursor_mouse(mouse_cursor)
        if not mouse_cursor:
            self.objectiveTrackerGUI.mouseFocus(False)
            if self.contextMenu is not None:
                self.contextMenu.hide()
                self.contextState = False
        if self.pvpScoreBar:
            self.pvpScoreBar.onSetBestCursor(mouse_cursor)
        return

    def showComponentInContextLayer(self, component):
        if self.contextLayer is not None:
            self.contextLayer.visible = False
            GUI.delRoot(self.contextLayer)
        component.visible = True
        self.contextLayer = component
        GUI.addRoot(component)
        GUI.reSort()
        return

    def showQuestLog(self, doShow=True):
        if self.questLogGUI is None:
            self.questLogGUI = soTPCQuestLog(GUI.Window())
            self.questLogGUI.onBound()
        if doShow:
            self.questLogGUI.show()
        else:
            self.questLogGUI.hide()
        return

    def showBinoculars(self, doShow=True):
        if self.binocularsCmp is None:
            self.binocularsCmp = GUI.Simple('soGUI/maps/Crosshairs/binokl_1.tga')
            cmp = self.binocularsCmp
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (0.0, 0.0, 0.0)
            cmp.widthMode = cmp.heightMode = 'CLIP'
            cmp.width = 2.0
            cmp.height = 2.0
            cmp.visible = False
        if not doShow and self.binocularsCmp is None:
            return
        else:
            if not doShow and not self.binocularsCmp.visible:
                return
                if doShow and self.binocularsCmp.visible:
                    return
                if doShow:
                    for root in GUI.roots():
                        if root.visible:
                            self.visibleRoots.append(root)
                            root.visible = False

                    self.binocularsCmp.visible = self.hiddenState or True
                    GUI.addRoot(self.binocularsCmp)
            elif self.visibleRoots and not self.hiddenState:
                for root in self.visibleRoots:
                    root.visible = True

                self.visibleRoots = []
                self.binocularsCmp.visible = False
                GUI.delRoot(self.binocularsCmp)
            self.worldLayer.delChild(self.inworldMarkersGUI.component)
            GUI.addRoot(self.inworldMarkersGUI.component)
            GUI.reSort()
            return

    def showLoadingScreen(self, doShow, radius=500):
        loadingGUI = BWPersonality.gpd.loadingGUI
        if doShow:
            BigWorld.worldDrawEnabled(False)
        else:
            BigWorld.worldDrawEnabled(True)

        def loadComplete(complete):
            BigWorld.worldDrawEnabled(res)
            loadingGUI.visible = False
            return

        if doShow:
            loadingGUI.visible = True
        else:
            loadingGUI.visible = False
        loadingGUI.focus = doShow
        loadingGUI.moveFocus = doShow
        loadingGUI.mouseButtonFocus = doShow
        if doShow:
            loadingGUI.script.start(radius, loadComplete)
        else:
            loadingGUI.script.cancel()
        return

    def showItemCache(self, doShow=True, cache_mode=None):
        if self.itemCacheGUI is None:
            self.itemCacheGUI = soItemCacheScreen(GUI.Window())
            self.itemCacheGUI.onBound()
        if doShow:
            self.itemCacheGUI.show(cache_mode)
        else:
            self.itemCacheGUI.hide()
        return

    def showUserFire(self, doShow=True, objId=None):
        if self.userFireGUI is None:
            self.userFireGUI = soUserFireCacheScreen(GUI.Window())
            self.userFireGUI.onBound()
        if doShow:
            self.userFireGUI.show(objId)
        else:
            self.userFireGUI.hide()
        return

    def showWarehouse(self, doShow=True, objId=None):
        if self.WarehouseGUI is None:
            self.WarehouseGUI = soWarehouse(GUI.Window())
            self.WarehouseGUI.onBound()
        if doShow:
            self.WarehouseGUI.show(objId)
        else:
            self.WarehouseGUI.hide()
        return

    def showStartSale(self, doShow=True, item=None, BankName=''):
        if self.startSaleGUI is None:
            self.startSaleGUI = soGUI.soStartSale.soStartSale(GUI.Window())
            self.startSaleGUI.onBound()
        if doShow:
            self.startSaleGUI.show(item, BankName)
        else:
            self.startSaleGUI.hide()
        return

    def showSubmitOffender(self, doShow=True, name=None):
        if self.startSubmitOffender is None:
            self.startSubmitOffender = soGUI.soStartSubmitOffender.soStartSubmitOffender(GUI.Window())
            self.startSubmitOffender.onBound()
        if doShow:
            self.startSubmitOffender.show(name)
        else:
            self.startSubmitOffender.hide()
        return

    def showArtifactQTE(self, doShow=True):
        if self.artifactQTE is None:
            self.artifactQTE = soArtifactQTE(GUI.Window())
            self.artifactQTE.onBound()
        if doShow:
            self.artifactQTE.show()
        else:
            self.artifactQTE.hide()
        return

    def showChatConsole(self, doShow=True):
        if self.chatConsole is None:
            self.chatConsole = soChatConsole3(GUI.Window())
            self.chatConsole.onBound()
        if doShow:
            self.chatConsole.show()
        else:
            self.chatConsole.hide()
        return

    def showQueueBox(self, doShow=True, success=False):
        if self.queueGUI is None:
            self.queueGUI = soQueueScreen(GUI.Window())
            self.queueGUI.onBound()
        if doShow:
            self.menuLayer.loginScreen.script.hide()
            self.queueGUI.show()
        elif not success:
            if hasattr(self.menuLayer, 'loginScreen'):
                self.menuLayer.loginScreen.script.show()
            if hasattr(self.menuLayer, 'characterManager'):
                self.menuLayer.characterManager.script.hide()
            self.queueGUI.hide()
        else:
            self.queueGUI.hide()
        return

    def showCharacterManager(self, doShow=True, mode=soCharacterManagmentGUI.MODE_SELECT):
        if self.characterManager is None:
            self.characterManager = soCharacterManagmentGUI(GUI.Window())
            self.characterManager.onBound()
        if doShow:
            self.menuLayer.loginScreen.script.hide()
            self.characterManager.show(mode)
        else:
            self.menuLayer.loginScreen.script.show()
            self.characterManager.hide()
        return

    def showCharacterMaker(self, doShow=True, stage=CHAR_MAKER.STAGE_2):
        if self.charMaker is None:
            self.charMaker = soCharacterMakerGUI(GUI.Window())
            self.charMaker.onBound()
        if doShow:
            self.menuLayer.loginScreen.script.hide()
            self.charMaker.show(stage)
        else:
            self.menuLayer.loginScreen.script.show()
            self.charMaker.hide()
        return

    def showCharacterPicker(self, doShow=True):
        if self.charPicker is None:
            self.charPicker = soCharacterPickGUI(GUI.Window())
            self.charPicker.onBound()
        if doShow:
            self.menuLayer.loginScreen.script.hide()
            self.charPicker.show()
        else:
            self.menuLayer.loginScreen.script.show()
            self.charPicker.hide()
        return

    def showHealthBar(self, doShow=True):
        if self.healthBarGUI is None:
            self.healthBarGUI = soHealthBar(GUI.Window())
            self.healthBarGUI.onBound()
        if doShow:
            self.healthBarGUI.show()
        else:
            self.healthBarGUI.hide()
        return

    def showOptions(self, doShow=True, callback=None):
        if self.optionsGUI is None:
            self.optionsGUI = soOptionsGUI3(GUI.Window(), callback=callback)
            self.optionsGUI.onBound()
        if doShow:
            self.loginGUI.deactivateEdits()
            self.optionsGUI.show(callback=callback)
        else:
            self.optionsGUI.hide()
        return

    def showFriendList(self, doShow=True):
        if self.friendList is None:
            self.friendList = FriendList(GUI.Window())
            self.friendList.onBound()
        if doShow:
            self.friendList.show()
        else:
            self.friendList.hide()
        return

    def showDonateBase(self, doShow=True):
        if self.DonateBase is None:
            self.DonateBase = DonatebaseGUI(GUI.Window())
            self.DonateBase.onBound()
        if doShow:
            self.DonateBase.show()
        else:
            self.DonateBase.hide()
        return

    def showDetailViewStakeGUI(self, doShow=True):
        if self.DetailViewStakeGUI is None:
            self.DetailViewStakeGUI = DetailViewStakeGUI(GUI.Window())
            self.DetailViewStakeGUI.onBound()
        if doShow:
            self.DetailViewStakeGUI.show()
        else:
            self.DetailViewStakeGUI.hide()
        return

    def showClanManagerNPCGUI(self, doShow=True, npc_id=0):
        if self.ClanManagerNPCGUI is None:
            self.ClanManagerNPCGUI = ClanManagerNPCGUI(GUI.Window())
            self.ClanManagerNPCGUI.onBound()
        if doShow:
            self.ClanManagerNPCGUI.show(npc_id)
        else:
            self.ClanManagerNPCGUI.hide()
        return

    def showQuitMenu(self, callbackYes=None, callbackNo=None, doShow=True):
        if self.QuitMenu is None:
            self.QuitMenu = soQuitMenu(GUI.Window(), callbackOnYesBtnClick=callbackYes, callbackOnNoBtnClick=callbackNo)
            self.QuitMenu.onBound()
        if doShow:
            self.QuitMenu.Show()
        else:
            self.QuitMenu.Hide()
        return

    def showTempOptions(self):
        return

    def showIngameMenu(self, doShow=True):
        if self.ingameMenuGUI is None:
            self.ingameMenuGUI = soIngameMainMenu(GUI.Window())
            self.ingameMenuGUI.onBound()
        if doShow:
            self.setMouseAltState(False)
            self.ingameMenuGUI.show()
        else:
            self.ingameMenuGUI.hide()
        return

    def showPackageSell(self, doShow=True):
        if self.packageGUI is None:
            self.packageGUI = soPackageSellScreen(GUI.Window())
            self.packageGUI.onBound()
        if doShow:
            self.packageGUI.show()
        else:
            self.packageGUI.hide()
        return

    def showCraftGUI(self, doShow=True):
        if self.craftGUI is None:
            self.craftGUI = soCraftGUI(GUI.Window())
            self.craftGUI.onBound()
        if doShow:
            self.craftGUI.show()
        else:
            self.craftGUI.hide()
        return

    def showGPS(self, doShow=True):
        if self.gpsGUI is None:
            self.gpsGUI = soGPSMap(GUI.Window())
            self.gpsGUI.onBound()
        if doShow:
            self.gpsGUI.show()
        else:
            self.gpsGUI.hide()
        return

    def showHelpGUI(self, doShow=True):
        if self.helpGUI is None:
            self.helpGUI = soGUI.soHelpGUI(GUI.Window())
            self.helpGUI.onBound()
        if doShow:
            self.helpGUI.show()
        else:
            self.helpGUI.hide()
        self.setBestCursor()
        return

    def showBulletinBoard(self, doShow=True):
        if self.soBulletinBoard is None:
            self.soBulletinBoard = soGUI.soBulletinBoard.soBulletinBoard(GUI.Window())
            self.soBulletinBoard.onBound()
        if doShow and not self.soBulletinBoard.component.visible:
            self.soBulletinBoard.show()
        else:
            self.soBulletinBoard.hide()
        self.setBestCursor()
        return

    def showBasetrader(self, doShow=True):
        if self.soBaseTrader is None:
            self.soBaseTrader = soGUI.soBaseTrader.soBaseTrader(GUI.Window())
            self.soBaseTrader.onBound()
        if doShow and not self.soBaseTrader.component.visible:
            self.soBaseTrader.show()
        else:
            self.soBaseTrader.hide()
        self.setBestCursor()
        return

    def showMessageBox(self, id='test', props=soDlgBoxPropsStructure(caption=u'placeholder', btnSet=[soDialogueBox.BTN_OK, soDialogueBox.BTN_CANCEL], additions=[('check', u'labelText1', 'id_check'), ('check', u'labelText2', 'id_check2'), ('check', u'labelText3', 'id_check3'),
 ('edit', True, 'edit1', u'PLACEHOLDER',
  (lambda newStr, offset, wholeText: True)), ('radio', u'radio1', 'id_radio1', True), ('radio', u'radio1', 'id_radio2', True)], msg=u'2233' + lc('soGUICore.soGUI.STRING_3090_464') + u'zzz2' + lc('soGUICore.soGUI.STRING_3090_553'))):
        btn_set = []
        for btn in props.btnSet:
            if btn == soDialogueBox.BTN_OK:
                btn_set.append({'type': (MESSAGEBOX.BTN_OK), 'width': (-1)})
            if btn == soDialogueBox.BTN_CANCEL:
                btn_set.append({'type': (MESSAGEBOX.BTN_CANCEL), 'width': (-1)})
            if btn == soDialogueBox.BTN_YES:
                btn_set.append({'type': (MESSAGEBOX.BTN_YES), 'width': (-1)})
            if btn == soDialogueBox.BTN_NO:
                btn_set.append({'type': (MESSAGEBOX.BTN_NO), 'width': (-1)})
            if btn == soDialogueBox.BTN_UNDO:
                btn_set.append({'type': (MESSAGEBOX.BTN_UNDO), 'width': (-1)})
            if btn == soDialogueBox.BTN_APPLY:
                btn_set.append({'type': (MESSAGEBOX.BTN_APPLY), 'width': (-1)})
            if btn == soDialogueBox.BTN_RESET:
                btn_set.append({'type': (MESSAGEBOX.BTN_RESET), 'width': (-1)})

        addControls = []
        addControls.append({'type': (MESSAGEBOX.ADDCONTROL_TEXTFIELD), 'text': (props.msg), 'ID': 'default_txt_field'})
        for addControl in props.additions:
            if addControl[0] == 'check':
                active = False
                if len(addControl) > 3:
                    active = addControl[3]
                ctrl_ = {'type': (MESSAGEBOX.ADDCONTROL_CHECKBOX), 'default': active, 'ID': (addControl[2]), 'caption': (addControl[1])}
                addControls.append(ctrl_)
            if addControl[0] == 'radio':
                active = False
                if len(addControl) > 3:
                    active = addControl[3]
                ctrl_ = {'type': (MESSAGEBOX.ADDCONTROL_RADIO), 'default': active, 'ID': (addControl[2]), 'caption': (addControl[1])}
                addControls.append(ctrl_)
            if addControl[0] == 'edit':
                validator = lambda newStr, wholeText, offset: True
                if len(addControl) > 4:
                    validator = addControl[4]
                default = u''
                if len(addControl) > 3:
                    default = addControl[3]
                ctrl_ = {'type': (MESSAGEBOX.ADDCONTROL_EDIT), 'default': default, 'ID': (addControl[2]), 'input_validator': validator}
                addControls.append(ctrl_)

        msgBox = soMessageBox(GUI.Window(), id=id, isModal=props.modal, x=0.0, y=0.0, width=props.width, caption=props.caption, forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=btn_set, timeout=0, closeBox=props.closeBox, defaultAction=None, addControls=addControls, callback=(lambda event, data: None))
        self.msgBoxMgr.addMsgBox(msgBox)
        return

    def closeMessageBox(self, id):
        self.msgBoxMgr.delMsgBox(id)
        return

    def showMsgBox(self, id, isModal=False, x=0.0, y=0.0, width=350, caption=lc('soGUICore.soGUI.STRING_3153_84'), forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=[{'type': (MESSAGEBOX.BTN_OK), 'width': 80, 'caption': u'ok', 'enabled': True}, {'type': (MESSAGEBOX.BTN_CANCEL), 'width': 80}], timeout=-1, closeBox=True, defaultAction=MESSAGEBOX.BTN_OK, addControls=[{'type': (MESSAGEBOX.ADDCONTROL_TEXTFIELD), 'ID': 'main_txt_field', 'text': (lc('soGUICore.soGUI.STRING_3157_93')), 'hAnchor': (MESSAGEBOX.ANCHOR_CENTER)}, {'type': (MESSAGEBOX.ADDCONTROL_LABEL), 'ID': 'main_label', 'hAnchor': (MESSAGEBOX.ANCHOR_CENTER), 'text': u'label_text_here'}], callback=(lambda event, data: None), isSystem=False):
        msgBox = soMessageBox(GUI.Window(), id, isModal, x, y, width, caption, forcePos, parent_gui_id, bind_to_parent, btn_set, timeout, closeBox, defaultAction, addControls, callback, isSystem)
        self.msgBoxMgr.addMsgBox(msgBox)
        return

    def closeMsgBox(self, id):
        return self.msgBoxMgr.delMsgBox(id)

    def setMsgBoxCtrlData(self, msgBoxID, controlID, data):
        self.msgBoxMgr.setAddControlData(msgBoxID, controlID, data)
        return

    def setMsgBoxBtnData(self, msgBoxID, btn_type, data):
        self.msgBoxMgr.setBtnData(msgBoxID, btn_type, data)
        return

    def showTPCMsgBox(self, id, width=400, height=350, text=u'PLACE_HOLDER', caption=u'PLACEHOLDER', btnSet=['ok', 'cancel', 'yes'], noCloseBox=False, additionalControls=[('check', u'labelText1', 'id_check'), ('check', u'labelText2', 'id_check2'), ('check', u'labelText3', 'id_check3'), ('edit', True, 'edit1')]):
        if self.tabletPC:
            if self.tabletPC.component.visible:
                self.tabletPC.showMsgBox(id, width, height, text, caption, btnSet, noCloseBox, additionalControls)
                return True
        return False

    def showInventory(self, doShow=True):
        if self.inventoryGUI is None:
            self.inventoryGUI = soInventoryScreen2(GUI.Window())
            self.inventoryGUI.onBound()
        if doShow:
            self.inventoryGUI.show()
        else:
            self.inventoryGUI.hide()
        return

    def updatePVPRoomsIDs(self, listIDRooms):
        if self.selectMap:
            self.selectMap.script.updatePVPRoomsIDs(listIDRooms)
        return

    def addServer2SelectMap(self, data, listIDRooms):
        if self.selectMap:
            self.selectMap.script.updateMapInfo(data, listIDRooms)
        return

    def showSelectMap(self, doShow=True):
        if self.selectMap is None:
            self.selectMap = soGUI.selectMapGUI.SelectMapGUI.create()
        if doShow:
            BigWorld.player().base.getAllRooms()
            self.selectMap.script.show()
        else:
            self.selectMap.script.hide()
        self.setBestCursor()
        return

    def showChoiceTeam(self, doShow=True, blackBG=False):
        if doShow:
            if self.shoiceTeamWindow is None:
                self.shoiceTeamWindow = soGUI.choiceTeam.choiceTeamGUI()
            self.shoiceTeamWindow.show(blackBG)
        elif self.shoiceTeamWindow:
            self.shoiceTeamWindow.hide()
        self.setBestCursor()
        return

    def showPVPmarker(self, doShow=True):
        if doShow:
            if self.PVPmarkerGUI is None:
                self.PVPmarkerGUI = soGUI.PVPmarker.PVPmarker()
            self.PVPmarkerGUI.show()
        elif self.PVPmarkerGUI:
            self.PVPmarkerGUI.hide()
        return

    def addPVPmarker(self, userID, matrix):
        if self.PVPmarkerGUI:
            self.PVPmarkerGUI.addMarker(userID, matrix)
        return

    def delPVPmarker(self, userID):
        if self.PVPmarkerGUI:
            self.PVPmarkerGUI.delMarker(userID)
        return

    def clearAllPVPmarkers(self):
        if self.PVPmarkerGUI:
            self.PVPmarkerGUI.clearAll()
        return

    def updateMatrixMarker(self, userID, matrix):
        if self.PVPmarkerGUI:
            self.PVPmarkerGUI.updateMatrixMarker(userID, matrix)
        return

    def showActionBar(self, doShow=True):
        if self.actionBar is None:
            self.actionBar = soActionBar(GUI.Window())
            self.actionBar.onBound()
        if doShow:
            self.actionBar.show()
        else:
            self.actionBar.hide()
        return

    def showNews(self, data):
        if self.soNewsGUI is None:
            self.soNewsGUI = soNews(GUI.Window())
            self.soNewsGUI.onBound()
        if data:
            self.soNewsGUI.show(data)
        else:
            self.soNewsGUI.hide()
        return

    def showTutorial(self, doShow=True):
        if self.tutorialGUI is None:
            self.tutorialGUI = soTutorialGUI(GUI.Window())
            self.tutorialGUI.onBound()
        if doShow:
            self.tutorialGUI.show()
        else:
            self.tutorialGUI.hide()
        return

    def showPrivateStore(self, doShow=True):
        if self.privateStoreGUI is None:
            self.privateStoreGUI = soPrivateStoreScreen(GUI.Window())
            self.privateStoreGUI.onBound()
        if doShow:
            self.privateStoreGUI.show()
        else:
            self.privateStoreGUI.hide()
        return

    def showInworldMarkers(self, doShow=True):
        if doShow:
            self.inworldMarkersGUI.show()
        else:
            self.inworldMarkersGUI.hide()
        return

    def showTrade(self, doShow=True):
        if self.tradeGUI is None:
            self.tradeGUI = soTradeGUI2(GUI.Window())
            self.tradeGUI.onBound()
        if doShow:
            self.tradeGUI.show()
        else:
            self.tradeGUI.hide()
        return

    def showRepairMode(self, doShow=True):
        self.repairMode = doShow
        self.repairEvent(REPAIR.EVENT_STATE, doShow)
        if not doShow:
            GUI.mcursor().shape = 'arrow'
        return

    def showObjectivesGUI(self, doShow=True):
        if self.objectivesGUI is None:
            self.objectivesGUI = soObjectivesGUI2(GUI.Window())
            self.objectivesGUI.onBound()
        if doShow:
            self.objectivesGUI.show()
        else:
            self.objectivesGUI.hide()
        return

    def changeTeamPVP(self, value):
        if self.pvpScoreBar:
            self.pvpScoreBar.changeTeamPVP(value)
        return

    def change_inPVPinstance(self, value):
        if self.ingameMenuGUI:
            self.ingameMenuGUI.change_inPVPinstance(value)
        self.showPVPScoreBar(value)
        self.showChoiceTeam(value, blackBG=True)
        return

    def pvpScoreWinTeam(self, teamID):
        if self.pvpScoreBar:
            self.pvpScoreBar.pvpScoreWinTeam(teamID)
        return

    def pvpScoreWinPlayer(self, playerName):
        if self.pvpScoreBar:
            self.pvpScoreBar.pvpScoreWinPlayer(playerName)
        return

    def pvpScoreStartRound(self):
        if self.pvpScoreBar:
            self.pvpScoreBar.pvpScoreStartRound()
        return

    def setScoreData(self, data):
        self.store_roomData = data
        if self.pvpScoreBar:
            self.pvpScoreBar.setScoreData(data)
        return

    def showPVPScoreBarPlayerList(self, doShow=True):
        if self.pvpScoreBar:
            self.pvpScoreBar.setVisibleScore(doShow)
        return

    def showPVPScoreBar(self, doShow=True):
        if doShow:
            if not self.pvpScoreBar:
                self.pvpScoreBar = soGUI.PVPScore.PVPScore()
            self.pvpScoreBar.show()
            if self.store_roomData:
                self.pvpScoreBar.setScoreData(self.store_roomData)
            self.pvpScoreBar.setVisibleScore(False)
        elif not doShow and self.pvpScoreBar:
            self.pvpScoreBar.hide()
        return

    def show(self):
        self.hiddenState = False
        for gui in self.hiddenGUIs:
            gui.visible = True

        return

    def hide(self):
        self.hiddenState = True
        roots = GUI.roots()
        for root in roots:
            if root.visible:
                self.hiddenGUIs.append(root)
                root.visible = False

        return

    def getCastBarData(self):
        if self.castBar is not None:
            return self.castBar.getState()
        else:
            return
            return

    def isRepairMode(self):
        return self.repairMode

    def getCurrentPPs(self):
        if self.ppRenderer is not None:
            return self.ppRenderer.getCurrentPPs()
        else:
            return []

    def getCurrentSysPPs(self):
        if self.ppRenderer is not None:
            return self.ppRenderer.getCurrentSysPPs()
        else:
            return []

    def getCurrentObjectives(self):
        if self.objectiveTrackerGUI is not None:
            return self.objectiveTrackerGUI.getObjectiveList()
        else:
            return

    def getGUIMap(self, return_id=False):
        map = []
        if self.packageGUI is not None:
            if self.packageGUI.component.visible:
                if not return_id:
                    map.append('packageSell')
                else:
                    map.append(GUI_ID.GUI_ID_PACKAGESELL)
        if self.inworldMarkersGUI is not None:
            if self.inworldMarkersGUI.component.visible:
                if not return_id:
                    map.append('inworldMarkers')
                else:
                    map.append(GUI_ID.GUI_ID_NAMEPLATES)
        if self.privateStoreGUI is not None:
            if self.privateStoreGUI.component.visible:
                if not return_id:
                    map.append('privateStore')
                else:
                    map.append(GUI_ID.GUI_ID_PRIVATESTORE)
        if self.objectivesGUI is not None:
            if self.objectivesGUI.component.visible:
                if not return_id:
                    map.append('objectivesGUI')
                else:
                    map.append(GUI_ID.GUI_ID_BASECAPTURE)
        if self.skillsGUI is not None:
            if self.skillsGUI.component.visible:
                if not return_id:
                    map.append('skillGUI')
                else:
                    map.append(GUI_ID.GUI_ID_SKILLS)
        if self.playerTrade is not None:
            if self.playerTrade.component.visible:
                if not return_id:
                    map.append('playerTradeGUI')
                else:
                    map.append(GUI_ID.GUI_ID_PCTRADE)
        if self.charScreen is not None:
            if self.charScreen.component.visible == True:
                if not return_id:
                    map.append('characterGUI')
                else:
                    map.append(GUI_ID.GUI_ID_CHARSCREEN)
        if self.clanGUI is not None:
            if self.clanGUI.component.visible == True:
                if not return_id:
                    map.append('clanGUI')
                else:
                    map.append(GUI_ID.GUI_ID_PDAGUILD)
        if self.questLogGUI is not None:
            if self.questLogGUI.component.visible == True:
                if not return_id:
                    map.append('questLogGUI')
                else:
                    map.append(GUI_ID.GUI_ID_PDAQUEST)
        if self.itemCacheGUI is not None:
            if self.itemCacheGUI.component.visible:
                if not return_id:
                    map.append('itemCacheGUI')
                else:
                    map.append(GUI_ID.GUI_ID_ITEMCACHE)
        if self.userFireGUI is not None:
            if self.userFireGUI.component.visible:
                map.append('userFireGUI')
        if self.WarehouseGUI is not None:
            if self.WarehouseGUI.component.visible:
                map.append('WarehouseGUI')
        if self.startSaleGUI is not None:
            if self.startSaleGUI.component.visible:
                map.append('startSale')
        if self.startSubmitOffender is not None:
            if self.startSubmitOffender.component.visible:
                map.append('startSubmitOffender_')
        if self.artifactQTE is not None:
            if self.artifactQTE.component.visible:
                if not return_id:
                    map.append('artifactQTEGUI')
                else:
                    map.append(GUI_ID.GUI_ID_MAGNETLOCKQTE)
        if self.tabletPC is not None:
            if self.tabletPC.component.visible:
                if not return_id:
                    map.append('tabletPCGUI')
                else:
                    map.append(GUI_ID.GUI_ID_PDAMAIN)
        if self.optionsGUI is not None:
            if self.optionsGUI.component.visible:
                if not return_id:
                    map.append('optionsGUI')
                else:
                    map.append(GUI_ID.GUI_ID_OPTIONS)
        if self.optionsGUI is not None:
            if self.optionsGUI.component.visible:
                if not return_id:
                    map.append('optionsGUI')
                else:
                    map.append(GUI_ID.GUI_ID_OPTIONS_NEW)
        if self.craftGUI is not None:
            if self.craftGUI.component.visible:
                if not return_id:
                    map.append('craftGUI')
                else:
                    map.append(GUI_ID.GUI_ID_CRAFT)
        if self.tradeGUI is not None:
            if self.tradeGUI.component.visible:
                if not return_id:
                    map.append('vendorGUI')
                else:
                    map.append(GUI_ID.GUI_ID_NPCTRADE)
        if self.dialogueGUI is not None:
            if self.dialogueGUI.component.visible:
                if not return_id:
                    map.append('npcDialogueGUI')
                else:
                    map.append(GUI_ID.GUI_ID_DIALOGUE)
        if self.ingameMenuGUI is not None:
            if self.ingameMenuGUI.component.visible:
                if not return_id:
                    map.append('ingameMenu')
                else:
                    map.append(GUI_ID.GUI_ID_INGAMEMENU)
        if self.actionBar is not None:
            if self.actionBar.component.visible:
                if not return_id:
                    map.append('actionBar')
                else:
                    map.append(GUI_ID.GUI_ID_ACTIONBAR)
        if self.inventoryGUI is not None:
            if self.inventoryGUI.component.visible:
                if not return_id:
                    map.append('inventoryGUI')
                else:
                    map.append(GUI_ID.GUI_ID_INVENTORY)
        return map

    def getCurrentCharMakerAppearance(self):
        retval = None
        if self.charMaker is not None:
            retval = self.charMaker.getCurrentAppearance()
        return retval

    def goModal(self, modalState=True):
        if modalState:
            self.modalState = True
        else:
            self.modalState = False
        self.modalLayer.visible = self.modalState
        return

    def setMouseAltState(self, altState=False, force=False):
        if force:
            self.mouseAltMode = altState
            BWPersonality.game.set_cursor_mouse(self.mouseAltMode)
        else:
            self.mouseAltMode = not self.mouseAltMode
            self.setBestCursor()
        return

    def registerDnDHook(self, func):
        if func is None:
            self.DnDHook = lambda event: False
            return
        else:
            if not callable(func):
                print 'soGUICore::registerDnDHook error: You must pass a callable or None'
            else:
                self.DnDHook = func
            return

    def registerKeyHook(self, func):
        if func is None:
            self.keyHook = lambda event: False
            return
        else:
            if not callable(func):
                print 'soGUICore::registerKeyHook error: You must pass a callable or None'
            else:
                self.keyHook = func
            return

    def getDoubleClickSpeedFromWin(self):
        regHandle = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Control Panel\\Mouse')
        self.mouseDoubleClickSpeed = float(_winreg.QueryValueEx(regHandle, 'DoubleClickSpeed')[0]) * 0.001
        regHandle.Close()
        return

    def killTooltipsAndContextMenus(self):
        return

    def preloadGUIMaps(self):
        return

    def onGUIMapsLoaded(self, refs):
        self.GUItextures = refs
        return

    def addToRadioGroup(self, group, script):
        if not self.radioGroups.has_key(group):
            self.radioGroups[group] = []
        self.radioGroups[group].append(script)
        return

    def delFromRadioGroup(self, group, script):
        if self.radioGroups.has_key(group):
            self.radioGroups[group].remove(script)
        return

    def onRadioBtn(self, group, script):
        if self.radioGroups.has_key(group):
            for rBtn in self.radioGroups[group]:
                if rBtn is not script:
                    rBtn.setInactive()

        return

    def registerCharacterReciever(self, cmp):
        if self.characterReciever is not None:
            self.characterReciever.script.lostCharacterFeed()
            self.characterReciever = cmp
            self.characterReciever.script.getCharacterFeed()
        else:
            self.characterReciever = cmp
            self.characterReciever.script.getCharacterFeed()
        return

    def unregisterCharacterReciever(self, cmp):
        if self.characterReciever == cmp:
            self.characterReciever.script.lostCharacterFeed()
            self.characterReciever = None
        return

    def clearCharacterReciever(self):
        self.characterReciever = None
        return

    def setLayerMode(self, mode):
        self.lastLayerMode = mode
        if self.characterReciever is not None:
            self.unregisterCharacterReciever(self.characterReciever)
        if mode == self.LAYER_MODE_MENU:
            self.menuLayer.visible = True
            self.generalLayer.visible = True
            self.worldLayer.visible = False
        elif mode == self.LAYER_MODE_INGAME:
            self.menuLayer.visible = False
            self.generalLayer.visible = True
            self.worldLayer.visible = True
        return

    def onNewDevice(self):
        (sW, sH) = BigWorld.screenSize()
        if self.healthBarGUI is not None:
            self.healthBarGUI.component.position.x = 3
            self.healthBarGUI.component.position.y = 3
        if hasattr(self.generalLayer, 'GUILocker'):
            self.generalLayer.GUILocker.ldrAnim.position = (
             sW / 2.0, sH / 2.0, 0.2)
            self.generalLayer.GUILocker.msg.position = (sW / 2.0, sH / 2.0 + 30, 0.1)
        if hasattr(self.generalLayer, 'genericTimer'):
            self.generalLayer.genericTimer.position = (
             sW / 2.0, 10, 0.5)
        if self.loginGUI is not None:
            self.loginGUI.doReposition()
        if self.optionsGUI is not None:
            self.optionsGUI.doReposition()
        if self.QuitMenu is not None:
            self.QuitMenu.doReposition()
        if self.soNewsGUI is not None:
            self.soNewsGUI.doReposition()
        if self.helpGUI is not None:
            self.helpGUI.doReposition()
        if self.soBulletinBoard is not None:
            self.soBulletinBoard.doReposition()
        if self.soBaseTrader is not None:
            self.soBaseTrader.doReposition()
        if self.characterManager is not None:
            self.characterManager.doReposition()
        if self.miniMapGUI is not None:
            self.miniMapGUI.doReposition()
        if self.systemMenu is not None:
            self.systemMenu.doReposition()
        if self.ingameMenuGUI is not None:
            self.ingameMenuGUI.doReposition()
        if self.spaceLoaderGUI is not None:
            self.spaceLoaderGUI.doReposition()
        if self.inventoryGUI is not None:
            self.inventoryGUI.doReposition()
        if self.privateStoreGUI is not None:
            self.privateStoreGUI.doReposition()
        if self.effectsFrame is not None:
            self.effectsFrame.doReposition()
        if self.actionBar is not None:
            self.actionBar.doReposition()
        if self.targettingGUI is not None:
            self.targettingGUI.doReposition()
        if self.tradeGUI is not None:
            self.tradeGUI.doReposition()
        if self.munitionsGUI is not None:
            self.munitionsGUI.doReposition()
        if self.chatConsole is not None:
            self.chatConsole.doReposition()
        if self.itemCacheGUI is not None:
            self.itemCacheGUI.doReposition()
        if self.userFireGUI is not None:
            self.userFireGUI.doReposition()
        if self.WarehouseGUI is not None:
            self.WarehouseGUI.doReposition()
        if self.startSaleGUI is not None:
            self.startSaleGUI.doReposition()
        if self.objectiveTrackerGUI is not None:
            self.objectiveTrackerGUI.doReposition()
        if self.bleedGUI is not None:
            self.bleedGUI.doReposition()
        if self.GUIpoison is not None:
            self.GUIpoison.doReposition()
        return

    def updateTopmostObjects(self):
        for topmost in self.topMostObjects:
            self.topMostObjects[topmost].restoreIfParentHiden()

        return

    def showTopmost(self, cmp, parent, layer=TOPMOST_DDL):
        self.topMostObjects[layer].setContent(cmp, parent)
        self.topMostObjects[layer].showContent()
        return

    def hideTopmost(self, cmp, layer=TOPMOST_DDL):
        if self.topMostObjects[layer].component == cmp:
            self.topMostObjects[layer].hideContent()
        return

    def checkAllTopmostComponents(self):
        for topObj in self.topMostObjects:
            self.topMostObjects[topObj].restoreIfParentHiden()

        return

    def toggleCharScreen(self):
        if self.charScreen is None:
            doShow = True
        else:
            doShow = not self.charScreen.component.visible
        self.showCharScreen(doShow)
        self.setBestCursor()
        return

    def toggleSkillGUI(self):
        if self.skillsGUI is None:
            doShow = True
        else:
            doShow = not self.skillsGUI.component.visible
        self.showSkillsGUI(doShow)
        self.setBestCursor()
        return

    def toggleClanGUI(self):
        if self.clanGUI is None:
            doShow = True
        else:
            doShow = not self.clanGUI.component.visible
        self.showClanGUI(doShow)
        self.setBestCursor()
        return

    def toggleQuestLog(self):
        if self.questLogGUI is None:
            doShow = True
        else:
            doShow = not self.questLogGUI.component.visible
        self.showQuestLog(doShow)
        self.setBestCursor()
        return

    def toggleMap(self):
        if self.gpsGUI is None:
            doShow = True
        else:
            doShow = not self.gpsGUI.component.visible
        self.showGPS(doShow)
        self.setBestCursor()
        return

    def toggleInventory(self):
        if self.inventoryGUI is None:
            doShow = True
        else:
            doShow = not self.inventoryGUI.component.visible
            self.showPrivateStore(False)
        self.showInventory(doShow)
        self.setBestCursor()
        return

    def toggleCraft(self):
        if self.craftGUI is None:
            doShow = True
        else:
            doShow = not self.craftGUI.component.visible
        self.showCraftGUI(doShow)
        self.setBestCursor()
        return

    def togglePrivateStore(self):
        if self.privateStoreGUI is None:
            doShow = True
        else:
            doShow = not self.privateStoreGUI.component.visible
        self.showInventory(doShow)
        self.showPrivateStore(doShow)
        self.setBestCursor()
        return

    def on_eula_accpeted(self):
        self.eula_state = True
        Settings().setSetting('eula_accepted', True, True)
        self.EULAgui.hide()
        return

    def on_eula_declined(self):
        self.eula_state = False
        BWPersonality.game.close()
        return

    @PyGUIEvent('hlink', 'onLmb')
    def onLmb(self):
        print 'onLmb'
        return

    @BWMemberCoroutine
    def genericTimerChecker(self, txt):
        while self.genericTimerSecs:
            secs = self.genericTimerSecs
            hours = floor(secs / 3600.0)
            minutes = floor((secs - hours * 3600.0) / 60.0)
            seconds = secs - (hours * 3600.0 + minutes * 60.0)
            outH = str(int(hours)) if hours > 9 else u'0' + str(int(hours))
            outM = str(int(minutes)) if minutes > 9 else u'0' + str(int(minutes))
            outS = str(int(seconds)) if seconds > 9 else u'0' + str(int(seconds))
            timeStr = txt + u' - ' + outH + u':' + outM + u':' + outS
            self.worldLayer.genericTimer.text = timeStr
            yield BWWaitForPeriod(1.0)
            self.genericTimerSecs -= 1

        return

    def createGenericGUICmp(self, cmpType='simple', tiled=False, tileHeight=1, tileWidth=1, width=100, height=100, hPosMode='PIXEL', vPosMode='PIXEL', hAnchor='LEFT', vAnchor='TOP', texture='', wMode='PIXEL', hMode='PIXEL', colour=(
 255, 255, 255, 255), matFX='BLEND'):
        cmp = None
        if cmpType == 'simple':
            cmp = GUI.Simple('')
        elif cmpType == 'window':
            cmp = GUI.Window()
        if cmp is None:
            print 'Failed to create a GUI component, you provided an invalid component type'
            return
        else:
            cmp.horizontalPositionMode = hPosMode
            cmp.verticalPositionMode = vPosMode
            cmp.widthMode = wMode
            cmp.heightMode = hMode
            cmp.horizontalAnchor = hAnchor
            cmp.verticalAnchor = vAnchor
            cmp.width = width
            cmp.height = height
            cmp.tiled = tiled
            cmp.tileHeight = tileHeight
            cmp.tileWidth = tileWidth
            cmp.textureName = texture
            cmp.colour = colour
            cmp.materialFX = matFX
            cmp.pixelSnap = False
            cmp.filterType = 'POINT'
            return cmp

    def setDebugBtn(self, id, text, x, y, w=100, h=21, hAnchor='LEFT', vAnchor='TOP', callBack=(lambda : None)):
        if hAnchor not in ('LEFT', 'CENTER', 'RIGHT'):
            print 'debugBtn can accept only LEFT, CENTER and RIGHT as hAnchor argument'
            return
        else:
            if vAnchor not in ('TOP', 'CENTER', 'BOTTOM'):
                print 'debugBtn can accept only TOP, CENTER and BOTTOM as vAnchor argument'
                return
            cmp = getattr(self.generalLayer, ('debugBtn{0}').format(id), None)
            if cmp:
                cmp.horizontalAnchor = hAnchor
                cmp.verticalAnchor = vAnchor
                cmp.width = w
                cmp.height = h
                cmp.position.x = x
                cmp.position.y = y
                cmp.label.text = text
                cmp.script.onClick = callBack
                return
            btn = soButton(GUI.Window())
            btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
            cmp = btn.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = hAnchor
            cmp.verticalAnchor = vAnchor
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.width = w
            cmp.height = h
            cmp.position.x = x
            cmp.position.y = y
            cmp.label.text = text
            self.generalLayer.addChild(cmp, ('debugBtn{0}').format(id))
            btn.onClick = callBack
            btn.onBound()
            return

    def delDebugBtn(self, id):
        cmp = getattr(self.generalLayer, ('debugBtn{0}').format(id), None)
        if cmp:
            self.generalLayer.delChild(cmp)
        return

    def drawLabel(self, id, text, x, y, hAnchor='LEFT', vAnchor='TOP'):
        if hAnchor not in ('LEFT', 'CENTER', 'RIGHT'):
            print 'drawLabel can accept only LEFT, CENTER and RIGHT as hAnchor argument'
            return
        else:
            if vAnchor not in ('TOP', 'CENTER', 'BOTTOM'):
                print 'drawLabel can accept only TOP, CENTER and BOTTOM as vAnchor argument'
                return
            cmp = getattr(self.generalLayer, ('testLabel{0}').format(id), None)
            if cmp:
                cmp.text = text
                cmp.horizontalAnchor = hAnchor
                cmp.verticalAnchor = vAnchor
                cmp.position.x = x
                cmp.position.y = y
            else:
                cmp = GUI.Text('')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = hAnchor
                cmp.verticalAnchor = vAnchor
                cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.text = text
                cmp.multiline = True
                cmp.position = (x, y, 0.0)
                cmp.multiline = True
                self.generalLayer.addChild(cmp, ('testLabel{0}').format(id))
            return

    def delLabel(self, id):
        cmp = getattr(self.generalLayer, ('testLabel{0}').format(id), None)
        if cmp:
            self.generalLayer.delChild(cmp)
        return
    def handleDragStartEvent(self, comp):
        if not self.hudEditMode:
            return False
        if comp is self._fpsBG or comp is self._weightBG:
            self._draggedComponent = comp
            mx, my = GUI.mcursor().position
            self._dragOffset = (mx - comp.position.x, my - comp.position.y)
            return True
        return False

    def handleDragMoveEvent(self, comp, pos):
        if comp is self._draggedComponent:
            mx, my = GUI.mcursor().position
            newX = mx - self._dragOffset[0]
            newY = my - self._dragOffset[1]
            # ограничение экраном (чтобы не утянуть за пределы)
            sw, sh = BigWorld.screenSize()
            comp.position.x = max(0, min(newX, sw - comp.width))
            comp.position.y = max(0, min(newY, sh - comp.height))
            return True
        return False

    def handleDragStopEvent(self, comp):
        if comp is self._draggedComponent:
            self._draggedComponent = None
            return True
        return False
    
    def _createWeightLabel(self):
        bg = GUI.Window('soGUI/maps/Colours/white.tga')
        bg.colour = (0, 0, 0, 120)
        bg.materialFX = 'BLEND'
        bg.widthMode = bg.heightMode = 'PIXEL'
        bg.width = 220                 # с запасом для "Вес: 999.9 / 999.9 кг"
        bg.height = 22
        bg.horizontalPositionMode = bg.verticalPositionMode = 'PIXEL'
        bg.horizontalAnchor = 'RIGHT'
        bg.verticalAnchor = 'BOTTOM'
        bg.position = (-12, -30, 0.1)
        bg.mouseButtonFocus = True
        bg.moveFocus = True
        bg.crossFocus = True
        bg.script = self
        self.systemLayer.addChild(bg, 'weightBG')
        self._weightBG = bg

        cmp = GUI.Text(u"Вес: --/-- кг")
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (4, 2, 0.0)
        bg.addChild(cmp, 'label')
        self.weightLabel = cmp
        bg.visible = self.showWeight
        cmp.visible = self.showWeight

    def _createFPSLabel(self):
        bg = GUI.Window('soGUI/maps/Colours/white.tga')
        bg.colour = (0, 0, 0, 120)
        bg.materialFX = 'BLEND'
        bg.widthMode = bg.heightMode = 'PIXEL'
        bg.width = 140                 # с запасом для "FPS: 9999"
        bg.height = 22
        bg.horizontalPositionMode = bg.verticalPositionMode = 'PIXEL'
        bg.horizontalAnchor = 'LEFT'
        bg.verticalAnchor = 'TOP'
        bg.position = (8, 8, 0.1)
        # Включаем захват мыши, чтобы получать события
        bg.mouseButtonFocus = True
        bg.moveFocus = True
        bg.crossFocus = True
        bg.script = self               # обработчики будут в soGUICore
        self.systemLayer.addChild(bg, 'fpsBG')
        self._fpsBG = bg

        cmp = GUI.Text(u"FPS: --")
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (12, 3, 0.0)    # небольшой отступ внутри фона
        bg.addChild(cmp, 'label')
        self.fpsLabel = cmp
        bg.visible = self.showFPS
        cmp.visible = self.showFPS

    def _updateFPSCounter(self):
        now = BigWorld.time()
        if not hasattr(self, '_lastFPSTime'):
            self._lastFPSTime = now
            self._fpsFrameCount = 0
        self._fpsFrameCount += 1
        if now - self._lastFPSTime >= 0.5:
            fps = int(round(self._fpsFrameCount / (now - self._lastFPSTime)))
            self.fpsLabel.text = u"FPS: %d" % fps
            self._lastFPSTime = now
            self._fpsFrameCount = 0
        self.fpsTimerID = BigWorld.callback(0.0, self._updateFPSCounter)

    def _startFPSTimer(self):
        if self.fpsTimerID is not None:
            BigWorld.cancelCallback(self.fpsTimerID)
        self._updateFPSCounter()

    def _stopFPSTimer(self):
        if self.fpsTimerID is not None:
            BigWorld.cancelCallback(self.fpsTimerID)
            self.fpsTimerID = None

    def setShowWeight(self, visible):
        self.showWeight = visible
        bg = getattr(self.systemLayer, 'weightBG', None)
        if bg:
            bg.visible = visible

    def setShowFPS(self, visible):
        self.showFPS = visible
        bg = getattr(self.systemLayer, 'fpsBG', None)
        if bg:
            bg.visible = visible
        if visible and self.fpsTimerID is None:
            self._startFPSTimer()
        elif not visible and self.fpsTimerID is not None:
            self._stopFPSTimer()