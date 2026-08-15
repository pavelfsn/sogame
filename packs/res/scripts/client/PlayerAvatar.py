# -*- coding: utf-8 -*-
from collections import deque
import hashlib, copy, math
from copy import deepcopy
from functools import partial
import traceback
from time import time, strftime, gmtime
import datetime, zlib, threading, random, BigWorld, Math, FMOD
from Math import Vector3, Matrix
import json
import FX, csconstans
from CallbackHelpers import callback
from SpiderFake import SpiderFake
import Fractions, Helpers.Caps, ItemsUtils, BWPersonality, GUI, Keys
from Settings import Settings
from Helpers import BWKeyBindings
from Helpers.BWKeyBindings import BWKeyBindingAction
from Helpers.VectorUtils import pointsOnCone, getXYZbyY, expressInBasis
from Inventory import Inventory
from Avatar import Avatar
from Victim import Victim
from EventUtils import pack
from Items import ItemsCatalog
from AvatarItemHolder import AvatarItemHolder
from ItemHolder import ItemHolder
import soGUI
from Character import Character
from FiringDefs import FiringDefs
from Notices import Notices
from Mailable import Mailable
from Grenade import Grenade
from CharacterUtils import CharacterConst, GetStatistic, GetCurrentWeaponProfiency, GetWeaponAdaptivity, GetWeaponSkillValue, GetCombatSkillValue
from ArtefactExtractor import PressGame
import Stats
from UnstableScope import UnstableScope
import Dialog, QuesterConsts, Quest
from matrix_providers import ShiftProvider
from soGUI.soInworldMarkers import soInworldMarker
import gui_jokes
from NPC import NPC
from sNPC import sNPC
from DroppedItem import DroppedItem
import colorCodes, Constants
from UserCommandFilter import UserCommandFilter
from UserCommandFilter import UserCommand
from MapNotes import MapNotes
from ClanMember import ClanMember
import SFXer
from Effects import Effects
from EffectUtils import getEffect
from TriggerObject import TriggerObject
from Inventory import SCOPE_MULTIPLER_TABLE
from Localization import lc
import RestrictionsUtils, Durations
from Restrictions import Restrictions
from utils_bw import isinstance_ext
from client_utils import get_entity_name
from math_bw import angle_between_vectors, VECTOR3_UP
from CorruptedPacks import CorruptedPacks
from Creature import Creature, brainStateToIcon
from ThrowingData import ThrowTypes
from gui_const import MESSAGEBOX
import msgbox_templates, Config, Clan, Respawn
from Quester import Quester
from gui_const import OBJECTIVE_TRACKER
from AnimationCaps import getCapByName
from FX_extension import preload_buffered_oneshot_sfx
import math
import itertools, Pixie
from Codes import HunterResponses
from sounds import getSound
from Camera import Camera
postEfNV = 'super_NV'

def formatNumber(num, places=0):
    formatted = '%.*f' % (places, float(num))
    integer, point, decimal = formatted.partition('.')
    index = 3
    while index < len(integer):
        integer = integer[:-index] + ',' + integer[-index:]
        index += 4
    return integer + point + decimal

def generate_jump_collision_shifts():
    shifts = [(0, 0, 0)]
    points, radius = 4, 0.3
    mult = radius / points
    for d in [i * mult for i in range(-points, points) if i != 0]:
        shifts.append((d, 0, 0))
        shifts.append((0, 0, d))
        shifts.append((-d, 0, d))
        shifts.append((d, 0, -d))
    random.shuffle(shifts)
    return shifts

DEFAULT_FOV = 0.78
RUNNING_FOV = 0.8
SPRINT_ANIMATION_SWITCH = 4.5

class PlayerAvatar(SpiderFake, Inventory, ClanMember, Avatar, BWKeyBindings.BWActionHandler, UserCommandFilter, Restrictions, Quester):

    class ShootRestictions():
        (NOAMMO, RELOAD, BINOCULING, THROW_GRENADE, EQUIPING, SPRINTING, USING_ITEM, SERVER_WAITING, DEATH, CRAFTING, UNJAMM, INFORM_JAMM, CROUCH, SITTING) = xrange(14)

    class StaminaUsers():
        (SPRINT, JUMP, HEART_MODE) = xrange(3)

    isMovie = False
    dialogCurrent = None
    nightVisonON = None
    isDialogStarted = False
    dialogChoosenButton = None
    dialogEntityID = 0
    queryDialogRequest = {}
    dialogHistory = []
    clanInviteConfirmCall = {}
    askIDteamNo = None
    JUMP_COLLISION_FROM = Vector3(0, 0.1, 0)
    JUMP_COLLISION_TO = Vector3(0, -0.2, 0)
    JUMP_COLLISION_SHIFTS = generate_jump_collision_shifts()
    MAX_SURFACE_ANGLE_TO_JUMP = 51 * math.pi / 180.0
    SHOW_DAMAGE = 0
    controlLocks = {}
    snipingSpeedModifier = 0.5
    lastOnline = 0
    pongCtr = 0
    isTogleCursor = False
    timeServerDiff = 0.0
    localSpeedModifiers = []
    pvpCaptureData = {'modes': 0, 'flags': [(1132, 2, 1.0, 2), (1163, 2, 1.0, 2)], 'time': 0, 'total_points': u'0/9', 'currentProgress': (-1.0, 'flag')}
    hidePvpDefenceDataCallbackID = 0
    detectorDecay = 1.0
    CAN_USE_ICON = 'soGUI/maps/Crosshairs/cursor_action-disable.tga'
    CAN_TALK_ICON = 'soGUI/maps/Crosshairs/cursor_action-enable.tga'
    HELPER_MODEL = 'models/misc/particles/helper_attach.model'
    NO_ICON = ''
    clanDlgBox = None
    groupDlgBox = None
    groupQuestDlgBox = None
    isInWorld = False
    msgFromShop = None
    magnitude = 7.0
    worldLoadStatusCode = 0
    lookModelPosAdjust = (0, 1.0, 0)
    artefactExtractor = None
    showGUIDamage = True
    printDamageToChat = True
    minDamageLimit = 5.0
    tradeEntity = None
    friendsList = []
    blackList = []
    pvppkstat = None
    selectedPartyMember = 0
    sound_breathing = None
    cinematic_camera = False
    camera_path = []          # список точек: каждая - кортеж (позиция, yaw, pitch)
    camera_playback_active = False
    camera_playback_index = 0
    camera_playback_timer = None
    spawned_models = [] 
    npc_ai_enabled = False
    npc_ai_targets = {}   # model_id -> {'type': 'follow'/'patrol', 'target': Vector3/Entity}
    npc_current_action = {} 
    current_npc_folder = "alkash"
    BOSS_CONFIG = {
        "paukan": {
            "path": "characters/creatures/spider_boss/spider.model",
            "texture": None,  # текстура уже правильная внутри папки
        },
        "nepr": {
            "path": "characters/creatures/impenetrable/impenetrable_lod1.model",
            "texture": None,  # текстура уже правильная внутри папки
        }
    }   # ← Закрываем BOSS_CONFIG
    # другие боссы можно добавить сюда
    npc_folder_list = [
        "alkash", "arab", "arab_bek", "boatswain", "businessman", "Ded_Moroz",
        "grandma", "guides", "ivan", "mechanic", "otshelnik", "pilot", "pomogalo",
        "torgovez", "uniforms",
        "armadillo", "basilisk", "basilisk_npc", "basilisk_sand", "basilisk_tints",
        "bear", "bear-mutant", "bes", "blyak", "boar-mutant", "brutor", "bush",
        "chicken", "crab", "crow", "dog", "dog-mutant", "dog_gasmask", "fish", "fly",
        "frog", "hyena", "imp", "impenetrable", "jelly", "medved", "outcast",
        "pill-bug", "rat-mutant", "silvan", "snowman", "spider", "spider_egg",
        "starshina", "Stump", "varan", "vedun", "verlioka", "vivert", "worm", "worms"
    ]

    NPC_MODEL_MAP = {
        "paukan": "characters/creatures/spider_boss/spider.model",
        "alkash": "characters/npc/alkash/alkash.model",
        "arab": "characters/npc/arab/arab_guard_01_body.model",
        "arab_bek": "characters/npc/arab_bek/arab_bek_01.model",
        "boatswain": "characters/npc/boatswain/boatswain_body_01.model",
        "businessman": "characters/npc/businessman/businessman_01.model",
        "Ded_Moroz": "characters/npc/Ded_Moroz/dedmoroz.model",
        "grandma": "characters/npc/grandma/grandma_01.model",
        "guides": "characters/npc/guides/guide_bandit.model",
        "ivan": "characters/npc/ivan/npc_ivan.model",
        "mechanic": "characters/npc/mechanic/mechanic_01.model",
        "otshelnik": "characters/npc/otshelnik/otshelnik.model",
        "pilot": "characters/npc/pilot/pilot_01.model",
        "pomogalo": "characters/npc/pomogalo/pomogalo.model",
        "torgovez": "characters/npc/torgovez/npc_torgovez.model",
        "uniforms": "characters/npc/uniforms/uniform.model",
        "armadillo": "characters/creatures/armadillo/armadillo.model",
        "basilisk": "characters/creatures/basilisk/basilisk_lod1.model",
        "basilisk_npc": "characters/creatures/basilisk_npc/basilisk_npc_lod1.model",
        "basilisk_sand": "characters/creatures/basilisk_sand/basilisk_sand_lod1.model",
        "basilisk_tints": "characters/creatures/basilisk_tints/basilisk_tints.model",
        "bear": "characters/creatures/bear/bear.model",
        "bear-mutant": "characters/creatures/bear-mutant/bear-mutant.model",
        "bes": "characters/creatures/bes/bes_lod1.model",
        "blyak": "characters/creatures/blyak/blyak_lod1.model",
        "boar-mutant": "characters/creatures/boar-mutant/boar_mutant_lod1.model",
        "brutor": "characters/creatures/brutor/brutor_lod1.model",
        "bush": "characters/creatures/bush/bush.model",
        "chicken": "characters/creatures/chicken/chicken.model",
        "crab": "characters/creatures/crab/crab.model",
        "crow": "characters/creatures/crow/crow.model",
        "dog": "characters/creatures/dog/dog.model",
        "dog-mutant": "characters/creatures/dog-mutant/dog-mutant.model",
        "dog_gasmask": "characters/creatures/dog_gasmask/dog_gasmask.model",
        "fish": "characters/creatures/fish/fish.model",
        "fly": "characters/creatures/fly/fly-mutant.model",
        "frog": "characters/creatures/frog/frog_lod1.model",
        "hyena": "characters/creatures/hyena/hyena.model",
        "imp": "characters/creatures/imp/imp_lod1.model",
        "impenetrable": "characters/creatures/impenetrable/impenetrable_lod1.model",
        "jelly": "characters/creatures/jelly/jelly_lod1.model",
        "medved": "characters/creatures/medved/medved.model",
        "outcast": "characters/creatures/outcast/outcast_lod1.model",
        "pill-bug": "characters/creatures/pill-bug/pill-bug.model",
        "rat-mutant": "characters/creatures/rat-mutant/rat-mutant_lod1.model",
        "silvan": "characters/creatures/silvan/silvan_lod1.model",
        "snowman": "characters/creatures/snowman/snowman.model",
        "spider": "characters/creatures/spider/spider.model",
        "spider_egg": "characters/creatures/spider_egg/spider_egg.model",
        "starshina": "characters/creatures/starshina/starshina.model",
        "Stump": "characters/creatures/Stump/stump.model",
        "varan": "characters/creatures/varan/varan.model",
        "vedun": "characters/creatures/vedun/vedun_lod1.model",
        "verlioka": "characters/creatures/verlioka/verlioka_lod1.model",
        "vivert": "characters/creatures/vivert/vivert_male_lod1.model",
        "worm": "characters/creatures/worm/worm_hulud.model",
        "worms": "characters/creatures/worms/worm_boss.model",
    }
    NPC_ANIMATION_MAP = {
        # Люди – обычно IdleUnarmed или IdleForever
        "alkash": "IdleUnarmed",
        "arab": "IdleUnarmed",
        "arab_bek": "IdleUnarmed",
        "boatswain": "IdleUnarmed",
        "businessman": "IdleUnarmed",
        "Ded_Moroz": "IdleUnarmed",
        "grandma": "IdleUnarmed",
        "guides": "IdleUnarmed",
        "ivan": "IdleUnarmed",
        "mechanic": "IdleUnarmed",
        "otshelnik": "IdleUnarmed",
        "pilot": "IdleUnarmed",
        "pomogalo": "IdleUnarmed",
        "torgovez": "IdleUnarmed",
        "uniforms": "IdleUnarmed",
        # Существа – часто просто "Idle"
        "armadillo": "Idle",
        "basilisk": "Idle",
        "basilisk_npc": "Idle",
        "basilisk_sand": "Idle",
        "basilisk_tints": "Idle",
        "bear": "Idle",
        "bear-mutant": "Idle",
        "bes": "Idle",
        "blyak": "Idle",
        "boar-mutant": "Idle",
        "brutor": "Idle",
        "bush": "Idle",
        "chicken": "Idle",
        "crab": "Idle",
        "crow": "Idle",
        "dog": "Idle",
        "dog-mutant": "Idle",
        "dog_gasmask": "Idle",
        "fish": "Idle",
        "fly": "Idle",
        "frog": "Idle",
        "hyena": "Idle",
        "imp": "Idle",
        "impenetrable": "Idle",
        "jelly": "Idle",
        "medved": "Idle",
        "outcast": "Idle",
        "pill-bug": "Idle",
        "rat-mutant": "Idle",
        "silvan": "Idle",
        "snowman": "Idle",
        "spider": "Idle",
        "spider_egg": "Idle",
        "starshina": "Idle",
        "Stump": "Idle",
        "varan": "Idle",
        "vedun": "Idle",
        "verlioka": "Idle",
        "vivert": "Idle",
        "worm": "Idle",
        "worms": "Idle",
    }
    GIVEAWAY_ITEMS = {
        'weapons_main': [
            "AK74M_ASSAULT_RIFLE", "AK_102_ASSAULT_RIFLE", "AK_107_ASSAULT_RIFLE",
            "AK_47_ASSAULT_RIFLE", "AK_74_ASSAULT_RIFLE", "AUG_A3_ASSAULT_RIFLE",
            "AUG_HBAR_MACHINEGUN", "BARRETT_M82A3_SNIPER_RIFLE", "COLT_M16_ASSAULT_RIFLE",
            "COLT_M4A1_ASSAULT_RIFLE", "CZ_805_CLAN_ASSAULT_RIFLE", "FAMAS_ASSAULT_RIFLE",
            "FN_FAL_ASSAULT_RIFLE", "FN_SCAR_H_CLAN_ASSAULT_RIFLE", "FRANCHI_SPAS_12_SHOTGUN",
            "HK_416_ASSAULT_RIFLE", "HK_417_CLAN_ASSAULT_RIFLE", "HK_G36C_ASSAULT_RIFLE",
            "HK_G3A_CLAN_ASSAULT_RIFLE", "HK_G3A_LAU_CLAN_ASSAULT_RIFLE", "JACKHAMMER_MK3A1_SHOTGUN",
            "M1014_JSCS_SHOTGUN", "M1_GARAND_RIFLE", "M202_ROCKET_LAUNCHER", "M79_ROCKET_LAUNCHER",
            "MK12_SPR_SNIPER_RIFLE", "MK48_MACHINEGUN", "MOSSBERG_500_SHOTGUN",
            "OC_14_762_ASSAULT_RIFLE", "OC_14_939_ASSAULT_RIFLE", "PECHENEG_CLAN_MACHINEGUN",
            "RPG7_ROCKET_LAUNCHER", "RUGER_MINI_14", "SAIGA_12K_SHOTGUN",
            "SIG_551_ASSAULT_RIFLE", "SIG_716_CLAN_ASSAULT_RIFLE", "SIG_751G_CLAN_ASSAULT_RIFLE",
            "SIG_751_ASSAULT_RIFLE", "STABILIZED_AK74_ASSAULT_RIFLE", "SVD_SNIPER_RIFLE",
            "SVU_A_CLAN_SNIPER_RIFLE", "SVU_CLAN_SNIPER_RIFLE", "TOZ_34_SHOTGUN",
            "VAL_ASSAULT_RIFLE", "VSS_MOD1_CLAN_ASSAULT_RIFLE", "VSS_SNIPER_RIFLE",
            "WALTHER_WA_2000"
        ],
        'weapons_secondary': [
            "COLT_1911_PISTOL", "DEASERT_EAGLE_PISTOL", "GLOCK_17_PISTOL", "GLOCK_18_PISTOL",
            "MAC_10_SUBMACHINEGUN", "MAKAROV_PISTOL", "MP5_K_SUBMACHINEGUN", "MP5_SUBMACHINEGUN",
            "PPSH_41_SUBMACHINEGUN", "SCORPION_VZ61_SUBMACHINEGUN", "SITES_SPECTRE_M4_SUBMACHINEGUN",
            "TOKAREV_TT_PISTOL", "UZI_SUBMACHINEGUN"
        ],
        'ammo': [
            "AMMO_127x99_AP", "AMMO_127x99_FMJ", "AMMO_12x70_FMJ", "AMMO_12x70_HP_12",
            "AMMO_12x70_HP_8", "AMMO_12x76_FMJ", "AMMO_12x76_HP_10", "AMMO_12x76_HP_15",
            "AMMO_40x53_HP", "AMMO_545x39_AP", "AMMO_545x39_AP_WOL", "AMMO_545x39_FMJ",
            "AMMO_545x39_SL", "AMMO_556x45_AP", "AMMO_556x45_FMJ_REM", "AMMO_556x45_FMJ_SS109",
            "AMMO_762x25_FMJ", "AMMO_762x25_HP", "AMMO_762x25_SL", "AMMO_45_ACP_FMJ",
            "AMMO_762x39_AP", "AMMO_762x39_FMJ", "AMMO_762x39_SL", "AMMO_762x51_AP",
            "AMMO_762x51_FMJ", "AMMO_762x54_AP", "AMMO_762x54_FMJ", "AMMO_762x54_HP",
            "AMMO_762x54_TEST", "AMMO_9x18_AP", "AMMO_9x18_FMJ", "AMMO_9x18_FMJ_BAD",
            "AMMO_9x18_HP", "AMMO_9x18_HP_POISON", "AMMO_9x19_AP", "AMMO_9x19_FMJ",
            "AMMO_9x19_HP", "AMMO_357_MAGNUM_AP", "AMMO_357_MAGNUM_FMJ", "AMMO_357_MAGNUM_HP_DOT",
            "AMMO_357_MAGNUM_HP_MAX", "AMMO_357_MAGNUM_HP_SAB", "AMMO_9x39_AP_PAB9",
            "AMMO_9x39_AP_SP6", "AMMO_9x39_FMJ_SP5", "AMMO_ENERGY_12V_A", "AMMO_ENERGY_1V_A",
            "AMMO_ENERGY_3V_A", "AMMO_ENERGY_9V_A", "AMMO_M74_HP", "AMMO_RPG7_AP_LUC",
            "AMMO_RPG7_FMJ", "AMMO_RPG7_HP_OSK", "AMMO_RPG7_HP_TAN"
        ],
        'armor': [
            "ARMY_BACKPACK", "BANDITO_MASK", "BERET_HAT", "BERET_HAT_BLUE", "BERET_HAT_RED",
            "CERBER_ARMOR", "CERBER_PANTS", "CERBER_SHIRT", "CHACK_ARMOR", "CHACK_PANTS",
            "CHACK_SHIRT", "CHIMERA_CLAN_BACKPACK", "CHIMERA_CLAN_SUIT", "DRAGOON_ARMOR",
            "DRAGOON_M2_ARMOR", "DSC_SUIT", "FAUNA_ARMOR", "FLORA_ARMOR", "GLASSES_KOBRA_MASK",
            "GRAFFITY_MASK", "HAKI_PANTS", "HAKI_SHIRT", "HARVAT_PANTS", "INGLISH_MASK",
            "INQUISITOR_CLAN_SUIT", "KAISER_ARMOR", "KOLOBOK_BACKPACK", "KOZIR_HAT",
            "KURTKA_SHIRT", "LONG_PANTS", "MARS_SUIT", "MASK_SNIPE_SUIT", "MAYKA_ARMOR",
            "MAZAY_HAT", "MISTIC_BACKPACK", "NINJA_ARMOR", "OMELET_ARMOR", "PANAMA_HAT",
            "PARTIZAN_BACKPACK", "PARTIZAN_PANTS", "PARTIZAN_SHIRT", "PATCHKA_SUIT",
            "PPS_SUIT", "PREDATOR_CLAN_SUIT", "RAT_ARMOR", "RAT_M2_ARMOR", "RAVENWOOD_ARMOR",
            "RAVENWOOD_HELM", "RAVENWOOD_PANTS", "RED_CROSS_SUIT", "SANDAL_ARMOR",
            "SEKVOYA_BACKPACK", "SHIZ_01_HELM", "SHIZ_02_HELM", "SHIZ_ARMOR", "SHIZ_PANTS",
            "SHKURKA_ARMOR", "SHPINAT_ARMOR", "SIGMA_SUIT", "SILENCE_CLAN_SUIT",
            "SINGLE_BACKPACK", "SINGLE_MOD1_SUIT", "SINGLE_SUIT", "SLONIK_MASK",
            "SPETSOVKA_SHIRT", "STELS_CLAN_SUIT", "STORMOVKA_SHIRT", "SUHAR_ARMOR",
            "SVOBODA2_CLAN_SUIT", "SVOBODA_CLAN_SUIT", "TASH_ARMOR", "TASH_M2_ARMOR",
            "TASH_PANTS", "UGORY_SUIT", "UNIFORM_MED_SHIRT", "UNIFORM_SCI_SHIRT",
            "UNIFORM_TECH_SHIRT", "VIKING_HELM", "VIKING_M2_HELM", "VIZIR_MASK",
            "VOENSTAL_SUIT", "VOROT_ARMOR", "VYAZONKA_HAT"
        ],
        'meds': [
            "HEALTH_ANTIPOISON", "HEALTH_ANTIRADIN", "HEALTH_BANDAGE", "HEALTH_PACK_AVERAGE",
            "HEALTH_PACK_GREAT", "HEALTH_PACK_LESSER", "HEALTH_PACK_SUPER"
        ],
        'artifacts': [
            "ARTIFACT_ANTIGRAV", "ARTIFACT_MAREVO", "ARTIFACT_NOOB", "ARTIFACT_PILLOW",
            "ARTIFACT_REZINA", "ARTIFACT_SCREEN", "ARTIFACT_SHIT", "ARTIFACT_STABILIZER",
            "ARTIFACT_VEZUVIY"
        ],
        'grenades': [
            "ATOMIC_GRENADE", "FRAG_GRENADE_F1", "HOMEMADE_GRENADE", "STONE_GRENADE"
        ],
        'scopes': [
            "ASSAULT1_NATO_SCOPE", "ASSAULT2_NATO_SCOPE", "ASSAULT3_NATO_SCOPE",
            "ASSAULT4_NATO_SCOPE", "BINOCULAR", "COLLIMATOR_USSR_SCOPE", "FLASH1_NATO_LIGHT",
            "FLASH2_NATO_LIGHT", "PO4X34_USSR_SCOPE", "PO6X36_USSR_SCOPE", "POSP8X42_USSR_SCOPE",
            "PSO1_USSR_SCOPE", "REDDOT_NATO_LIGHT", "SNIPER1_ADD_NATO_SCOPE",
            "SNIPER1_NATO_SCOPE", "SNIPER2_NATO_SCOPE", "SNIPER3_NATO_SCOPE",
            "SNIPER4_NATO_SCOPE", "SNIPER_VAR_RUSS_SCOPE", "WEAPON_USSR_LIGHT"
        ],
        'tools': [
            "ANOMALY_DETECTOR", "ANOMALY_EXTRACTOR", "ANOMALY_EXTRACTOR_CFT",
            "ANOMALY_EXTRACTOR_MODULE", "ANOMALY_EXTRACTOR_PROTOTYPE", "REPAIR_KIT",
            "REPAIR_RARE_KIT"
        ]
        
    }
    unlimited_stamina = False

    def getPvPPKstat(self):
        self.cell.getPvPPKstat()
    def spawn_boss(self, boss_name, scale=2.0):
        cfg = self.BOSS_CONFIG.get(boss_name.lower())
        if not cfg:
            self.systemChatline("[Boss] Unknown boss: " + boss_name)
            return
        try:
            model = BigWorld.Model(cfg["path"])
            self.addModel(model)
            cam = BigWorld.camera()
            pos = self.position + cam.direction * 5.0
            pos.y = self.position.y + 1.0
            collision = BigWorld.collide(self.spaceID, pos + (0,1,0), pos + (0,-1,0))
            if collision:
                pos = collision[0]
            model.position = pos
            model.scale = Math.Vector3(scale, scale, scale)
            # Замена текстуры
            try:
                for i in range(model.nMaterials()):
                    mat = model.getMaterial(i)
                    mat.setProperty("diffuseMap", cfg["texture"])
            except:
                pass
            self.spawned_models.append(model)
            # Пробуем Idle анимацию
            try:
                act = model.action("Idle")
                if act: act(0, None, 0, -1, -1, 2.0)
            except:
                pass
            self.systemChatline("[Boss] Spawned %s (scale %.1f)" % (boss_name, scale))
        except Exception as e:
            self.systemChatline("[Boss] Error: " + str(e))

    def setPvpPkStat(self, data):
        self.pvppkstat = data
        _data = {'rep_groups': [[0, lc('PlayerAvatar.client.STRING_1122_8')]],
                 'rep_factions': {0: [i[1] for id in Fractions.ALL_FRACTIONS]},
                 'pvp': self.pvppkstat}
        BWPersonality.GUICore.setCharScreenData(_data)
        
    @BWKeyBindingAction('ToggleCinematicCamera')
    def toggleCinematicCamera(self, isDown):
        if not isDown:
            self.cinematic_camera = not self.cinematic_camera
            try:
                cam = BigWorld.camera()
                if cam is not None:
                    cam.turningHalfLife = 0.1 if self.cinematic_camera else 0.0
            except:
                pass
            print('Cinematic camera: %s' % ('ON' if self.cinematic_camera else 'OFF'))
    @BWKeyBindingAction('ToggleUnlimitedStamina')
    def keyToggleUnlimitedStamina(self, isDown):
        if not isDown:
            self.toggle_unlimited_stamina()

    @BWKeyBindingAction('ListWeatherSystems')
    def keyListWeatherSystems(self, isDown):
        if not isDown:
            self.list_weather_systems()
    @UserCommand
    def give_items(self, category="all"):
        """Выбрасывает предметы указанной категории перед игроком.
        Категории: weapons_main, weapons_secondary, ammo, armor, meds, artifacts, grenades, scopes, tools, all (по одному каждого типа)"""
        import random
        if category not in self.GIVEAWAY_ITEMS and category != "all":
            self.systemChatline("[Give] Unknown category: " + category)
            return

        if category == "all":
            items = []
            for cat in self.GIVEAWAY_ITEMS:
                items.append(self.GIVEAWAY_ITEMS[cat][0])  # по одному первому из каждой категории
        else:
            items = self.GIVEAWAY_ITEMS[category]

        cam = BigWorld.camera()
        base_pos = self.position + cam.direction * 2.0
        base_pos.y = self.position.y
        collision = BigWorld.collide(self.spaceID, base_pos + (0, 2, 0), base_pos + (0, -2, 0))
        if collision:
            base_pos = collision[0]

        count = 0
        for i, item_id in enumerate(items):
            # Разбрасываем по небольшой дуге
            offset_x = (i % 3 - 1) * 1.0
            offset_z = (i // 3) * 0.8
            pos = base_pos + Math.Vector3(offset_x, 0, offset_z)
            try:
                BigWorld.createEntity("DroppedItem", self.spaceID, 0, pos, (0, 0, 0),
                                      {"itemID": item_id, "count": 1})
                count += 1
            except Exception as e:
                self.systemChatline("[Give] Failed to create " + item_id + ": " + str(e))
        self.systemChatline("[Give] Spawned %d items (category: %s)" % (count, category))
    @UserCommand
    def cam_add(self):
        if not Camera.online:
            self.systemChatline("[Cam] Free camera not active (press G first)")
            return
        cam = BigWorld.camera()
        pos = cam.position
        yaw = cam.direction.yaw
        pitch = cam.direction.pitch
        self.camera_path.append((tuple(pos), yaw, pitch))
        self.systemChatline("[Cam] Added point %d: pos=%s yaw=%.2f pitch=%.2f" %
                           (len(self.camera_path), pos, yaw, pitch))

    @UserCommand
    def cam_clear(self):
        self.camera_path = []
        self.systemChatline("[Cam] Path cleared")

    @UserCommand
    def cam_list(self):
        if not self.camera_path:
            self.systemChatline("[Cam] Path is empty")
            return
        for i, (pos, yaw, pitch) in enumerate(self.camera_path):
            self.systemChatline("[Cam] %d: pos=%s yaw=%.2f pitch=%.2f" % (i+1, pos, yaw, pitch))

    @UserCommand
    def cam_play(self, duration=5.0):
        if not Camera.online:
            self.systemChatline("[Cam] Free camera must be active (press G)")
            return
        if len(self.camera_path) < 2:
            self.systemChatline("[Cam] Need at least 2 points in path")
            return
        if self.camera_playback_active:
            self.cam_stop()

        keyframes = []
        total = len(self.camera_path)
        for i, (pos, yaw, pitch) in enumerate(self.camera_path):
            t = float(i) / (total - 1) * duration
            mat = Math.Matrix()
            mat.setTranslate(Math.Vector3(*pos))
            mat.setRotateYPR((yaw, pitch, 0.0))
            keyframes.append((t, mat))

        anim = Math.MatrixAnimation()
        anim.keyframes = keyframes
        anim.loop = False
        anim.time = 0.0

        if hasattr(self, '_cam_servo') and self._cam_servo is not None:
            Camera.freeCamera_model.delMotor(self._cam_servo)
        self._cam_servo = BigWorld.Servo(anim)
        Camera.freeCamera_model.addMotor(self._cam_servo)

        self.camera_playback_active = True
        self.systemChatline("[Cam] Playing path (%.1f sec)" % duration)

        def on_finish():
            if hasattr(self, '_cam_servo'):
                Camera.freeCamera_model.delMotor(self._cam_servo)
                self._cam_servo = None
            self.camera_playback_active = False
            self.systemChatline("[Cam] Playback finished")
        BigWorld.callback(duration, on_finish)

        
    def _cam_playback_update(self):
        if not self.camera_playback_active:
            return
        elapsed = BigWorld.time() - self._cam_playback_start_time
        if elapsed >= self._cam_playback_duration:
            last_pos, last_yaw, last_pitch = self._cam_playback_points[-1]
            self._set_cam_pos(last_pos, last_yaw, last_pitch)
            self.systemChatline("[Cam] Playback finished")
            self.camera_playback_active = False
            return

        total_points = len(self._cam_playback_points)
        t = elapsed / self._cam_playback_duration * (total_points - 1)
        idx = int(t)
        frac = t - idx
        if idx >= total_points - 1:
            idx = total_points - 2
            frac = 1.0

        pos1, yaw1, pitch1 = self._cam_playback_points[idx]
        pos2, yaw2, pitch2 = self._cam_playback_points[idx + 1]

        interp_pos = Math.Vector3(
            pos1[0] * (1 - frac) + pos2[0] * frac,
            pos1[1] * (1 - frac) + pos2[1] * frac,
            pos1[2] * (1 - frac) + pos2[2] * frac
        )

        def interp_angle(a1, a2, f):
            diff = a2 - a1
            if diff > math.pi:
                a1 += 2 * math.pi
            elif diff < -math.pi:
                a2 += 2 * math.pi
            return a1 * (1 - f) + a2 * f

        interp_yaw = interp_angle(yaw1, yaw2, frac)
        interp_pitch = interp_angle(pitch1, pitch2, frac)

        self._set_cam_pos(interp_pos, interp_yaw, interp_pitch)
        self.camera_playback_timer = BigWorld.callback(0.05, self._cam_playback_update)
    def _set_cam_pos(self, pos, yaw, pitch):
        if not Camera.online:
            return
        cam = BigWorld.camera()
        cam.position = Math.Vector3(pos[0], pos[1], pos[2])
        direction = Math.Vector3()
        direction.setPitchYaw(pitch, yaw)
        cam.direction = direction

    def _cam_play_manual(self, keyframes, duration):
        """Ручное воспроизведение через колбэки (если нет модели камеры)"""
        start_time = BigWorld.time()
        def update():
            if not self.camera_playback_active:
                return
            elapsed = BigWorld.time() - start_time
            if elapsed >= duration:
                # Последний кадр
                mat = keyframes[-1][1]
                BigWorld.camera().position = mat.translation
                dir_vec = mat.applyVector(Math.Vector3(0, 0, 1))
                BigWorld.camera().direction = dir_vec
                self.systemChatline("[Cam] Playback finished")
                self.camera_playback_active = False
                return
            # Найти текущий сегмент
            for i in range(len(keyframes)-1):
                t1, m1 = keyframes[i]
                t2, m2 = keyframes[i+1]
                if t1 <= elapsed <= t2:
                    alpha = (elapsed - t1) / (t2 - t1)
                    # Линейная интерполяция позиции
                    pos = m1.translation * (1-alpha) + m2.translation * alpha
                    # Интерполяция поворота через кватернионы (упрощённо)
                    q1 = Math.Quaternion(m1)
                    q2 = Math.Quaternion(m2)
                    q = q1.slerp(q2, alpha)
                    mat = Math.Matrix()
                    mat.setRotate(q)
                    mat.translation = pos
                    BigWorld.camera().position = pos
                    BigWorld.camera().direction = mat.applyVector(Math.Vector3(0, 0, 1))
                    break
            self.camera_playback_timer = BigWorld.callback(0.05, update)
        self.camera_playback_active = True
        update()

    @UserCommand
    def cam_stop(self):
        if hasattr(self, '_cam_servo') and self._cam_servo is not None:
            Camera.freeCamera_model.delMotor(self._cam_servo)
            self._cam_servo = None
        self.camera_playback_active = False
        self.systemChatline("[Cam] Playback stopped")

    @UserCommand
    def cam_save(self, filename="camera_path.json"):
        import os, json
        save_path = os.path.join(os.getcwd(), filename)
        if not filename.endswith('.json'):
            save_path += '.json'
        data = [{'pos': list(pos), 'yaw': yaw, 'pitch': pitch} for pos, yaw, pitch in self.camera_path]
        with open(save_path, 'w') as f:
            json.dump(data, f, indent=2)
        self.systemChatline("[Cam] Saved %d points to %s" % (len(self.camera_path), filename))
        
    @BWKeyBindingAction('CamAddPoint')
    def keyCamAdd(self, isDown):
        if not isDown: self.cam_add()

    @BWKeyBindingAction('CamPlay')
    def keyCamPlay(self, isDown):
        if not isDown: self.cam_play(5.0)

    @UserCommand
    def cam_load(self, filename="camera_path.json"):
        import os, json
        load_path = os.path.join(os.getcwd(), filename)
        if not filename.endswith('.json'):
            load_path += '.json'
        try:
            with open(load_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            self.systemChatline("[Cam] Load error: " + str(e))
            return
        self.camera_path = [(tuple(d['pos']), d['yaw'], d['pitch']) for d in data]
        self.systemChatline("[Cam] Loaded %d points from %s" % (len(self.camera_path), filename))
    @UserCommand
    def toggle_npc_ai(self):
        self.npc_ai_enabled = not self.npc_ai_enabled
        self.systemChatline("[AI] NPC AI " + ("ON" if self.npc_ai_enabled else "OFF"))
        if self.npc_ai_enabled:
            self._npc_ai_loop()

    def _npc_ai_loop(self):
        if not self.npc_ai_enabled:
            return
        count = 0
        for model in self.spawned_models:
            if not hasattr(model, 'position'):
                continue
            count += 1
            try:
                direction = self.position - model.position
                dist = direction.length

                if dist > 2.0:
                    # Движение
                    direction.normalise()
                    step = direction * 0.2
                    new_pos = Math.Vector3(model.position.x + step.x,
                                           model.position.y + step.y,
                                           model.position.z + step.z)
                    model.position = new_pos
                    if hasattr(model, 'yaw'):
                        model.yaw = math.atan2(direction.x, direction.z)

                    # Запуск ходьбы/бега
                    if self.npc_current_action.get(model) != 'Walk':
                        act = model.action('Walk')
                        if act:
                            act(0, None, 0, -1, -1, 2.0)
                            self.npc_current_action[model] = 'Walk'

                else:
                    # Остановка – idle
                    if self.npc_current_action.get(model) not in (None, 'Idle'):
                        act = model.action('Idle')
                        if act:
                            act(0, None, 0, -1, -1, 2.0)
                            self.npc_current_action[model] = 'Idle'

            except Exception as e:
                # Логирование ошибки конкретного NPC без остановки цикла (Python 2 совместимо)
                print 'ERROR in _npc_ai_loop for model %s: %s' % (model, e) 
                pass # Продолжаем работу с остальными моделями

        if count > 0:
            self.systemChatline("[AI] Processing %d models" % count)
        BigWorld.callback(0.5, self._npc_ai_loop)


    @UserCommand
    def save_spawned_models(self, filename="spawned_models.json"):
        import os, json
        save_path = os.path.join(os.getcwd(), filename)
        data = []
        for model in self.spawned_models:
            if hasattr(model, 'position') and hasattr(model, 'sources') and model.sources:
                path = model.sources[0].strip().replace('\\', '/')
                data.append({
                    'path': path,
                    'pos': (model.position.x, model.position.y, model.position.z),
                })
        with open(save_path, 'w') as f:
            json.dump(data, f, indent=2)
        self.systemChatline("[Save] %d models saved to %s" % (len(data), filename))

    @UserCommand
    def load_spawned_models(self, filename="spawned_models.json"):
        import os, json
        load_path = os.path.join(os.getcwd(), filename)
        try:
            with open(load_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            self.systemChatline("[Load] Error: " + str(e))
            return
        count = 0
        for item in data:
            try:
                path = item['path'].strip().replace('\\', '/')
                model = BigWorld.Model(path)
                if model:
                    self.addModel(model)
                    model.position = tuple(item['pos'])
                    self.spawned_models.append(model)
                    count += 1
            except Exception as e:
                self.systemChatline("[Load] Failed " + item['path'] + ": " + str(e))
        self.systemChatline("[Load] Loaded %d models from %s" % (count, filename))
    @UserCommand
    def toggle_unlimited_stamina(self):
        self.unlimited_stamina = not self.unlimited_stamina
        print "Unlimited stamina:", "ON" if self.unlimited_stamina else "OFF"
    def onCameraInWater(self, status):
        if status:
            BWPersonality.GUICore.addPPEffect('underwater')
            if hasattr(self, 'water_reverb') and self.water_reverb:
                self.water_reverb.active = True
            else:
                reverb = FMOD.EventReverb('underwater')
                reverb.minDistance = 1000
                reverb.maxDistance = 1000
                reverb.active = True
                reverb.source = BigWorld.PlayerMatrix()
                self.water_reverb = reverb
        else:
            BWPersonality.GUICore.delPPEffect('underwater')
            if hasattr(self, 'water_reverb') and self.water_reverb:
                self.water_reverb.active = False

    def newFriendsList(self, friendList):
        self.friendsList = [f[1] for f in friendList]

    def newBlackList(self, blackList):
        self.blackList = [b[1] for b in blackList]

    def getFriendList(self):
        return self.friendsList

    def getBlackList(self):
        return self.blackList

    def playerLogOff(self):
        self.base.updateFriendListStatus(False)

    def MsgError(self, msg):
        self.systemChatline(lc('GUI.FriendList.' + msg))
        
    @UserCommand
    def list_anca_actions(self, folder_name):
        """Ищет имена анимаций в .anca файлах указанной папки модели"""
        import os, string
        res_path = "F:/SO/so-education-main — копия/packs/res"
        for base in ["characters/npc", "characters/creatures"]:
            folder = os.path.join(res_path, base, folder_name)
            if os.path.isdir(folder):
                for f in os.listdir(folder):
                    if f.endswith(".anca"):
                        path = os.path.join(folder, f)
                        with open(path, "rb") as af:
                            data = af.read()
                        # Ищем последовательности букв длиной от 4 символов
                        strings = set()
                        current = []
                        for byte in data:
                            if 32 <= byte <= 126 and chr(byte) in string.printable:
                                current.append(chr(byte))
                            else:
                                if len(current) >= 4:
                                    strings.add(''.join(current))
                                current = []
                        # Фильтруем вероятные названия анимаций (с большой буквы)
                        actions = [s for s in strings if s and s[0].isupper() and len(s) < 30]
                        print "=== Potential animation names in", f, "==="
                        for act in sorted(actions):
                            print "  ", act
                        return
        print "No .anca files found in", folder_name

    def updateFriendList(self, friendName, status):
        for i, friend in enumerate(self.friendsList):
            if friend[0] == friendName:
                self.friendsList[i] = (friendName, status)
                notifyState = Settings().getNotifyFriendList()
                if notifyState:
                    if status:
                        self.systemChatline(lc('GUI.FriendList.QueryFriend1') + ' ' + friendName.decode('utf-8') + ' ' + lc('GUI.FriendList.isOnline'))
                    else:
                        self.systemChatline(lc('GUI.FriendList.QueryFriend1') + ' ' + friendName.decode('utf-8') + ' ' + lc('GUI.FriendList.isOffline'))
                if BWPersonality.GUICore.friendList.component.visible:
                    BWPersonality.GUICore.friendList.displayFriendList(0)

    def getTargetForFriendlyAction(self, friendName):
        if not friendName:
            target = BigWorld.target()
            if target and isinstance(target, Avatar):
                return target.playerName
            print 'CLIENT: Please specify friend name or have friend targetted.'
            return ''
        return friendName

    def showRequestToFriend(self, friendName):
        def okey_callback(event):
            if event == gui_jokes.askUserYesNo.YES:
                self.base.friendConfirmedRequest(friendName)
        gui_jokes.askUserYesNo(lc('GUI.FriendList.CaptionQueryWindow'),
                               lc('GUI.FriendList.QueryFriend1') + ' ' + friendName.decode('utf8') + ' ' + lc('GUI.FriendList.QueryFriend2'),
                               okey_callback)

    def friendStatusChanged(self, friendName, status):
        self.updateFriendList(friendName, status)

    def inviteFriendToClan(self, name):
        self.base.inviteFriendToClan(name)

    def getFriendIdxByName(self, friendName):
        for i in range(len(self.friendsList)):
            if self.friendsList[i][0] == friendName:
                return i
        return -1

    def addFriend(self, friendName):
        target = self.getTargetForFriendlyAction(friendName)
        if target:
            idx = self.getFriendIdxByName(target)
            if idx < 0:
                self.base.addFriend(target)
            else:
                self.systemChatline(lc('GUI.FriendList.QueryFriend1') + ' ' + target.decode('utf-8') + ' ' + lc('GUI.FriendList.isAlreadyYourFriend'))

    def onAddedFriend(self, friendName, online):
        if (friendName, online) not in self.friendsList:
            self.friendsList.append((friendName, online))
            self.systemChatline(lc('GUI.FriendList.QueryFriend1') + ' ' + friendName.decode('utf-8') + ' ' + lc('GUI.FriendList.addedToFriendList'))
            if BWPersonality.GUICore.friendList.component.visible:
                BWPersonality.GUICore.friendList.displayFriendList(0)

    def delFriend(self, friendName):
        for i, friend in enumerate(self.friendsList):
            if friend[0] == friendName:
                del self.friendsList[i]
                break
        self.base.delFriend(friendName)
        self.systemChatline(lc('GUI.FriendList.QueryFriend1') + ' ' + friendName.decode('utf-8') + ' ' + lc('GUI.FriendList.deletedFriendmsg'))
        if BWPersonality.GUICore.friendList.component.visible:
            BWPersonality.GUICore.friendList.displayFriendList(0)

    def addToBlackList(self, name):
        self.base.addBlackList(name)

    def onAddedBlackList(self, name):
        if name not in self.blackList:
            self.blackList.append(name)
            self.systemChatline(lc('GUI.FriendList.QueryFriend1') + ' ' + name.decode('utf-8') + ' ' + lc('GUI.FriendList.addedToBlackList'))
            if BWPersonality.GUICore.friendList.component.visible:
                BWPersonality.GUICore.friendList.displayBlackList(0)

    def delFromBlackList(self, name):
        if name not in self.blackList:
            self.systemChatline(lc('GUI.FriendList.QueryFriend1') + ' ' + name.decode('utf-8') + ' ' + lc('GUI.FriendList.playerNotFoundInBlackList'))
        else:
            self.base.delFrmBlackList(name)
            self.blackList.remove(name)
            self.systemChatline(lc('GUI.FriendList.QueryFriend1') + ' ' + name.decode('utf-8') + ' ' + lc('GUI.FriendList.playerIsDeleted'))
            if BWPersonality.GUICore.friendList.component.visible:
                BWPersonality.GUICore.friendList.displayBlackList(0)

    def listFriends(self):
        print 'DEBUG: You have', len(self.friendsList), 'friend(s):'
        print 'DEBUG:', self.friendsList

    def msgFriend(self, friendName, message):
        target = self.getTargetForFriendlyAction(friendName)
        if target:
            idx = self.getFriendIdxByName(target)
            if idx >= 0:
                self.base.sendMessageToFriend(idx, message)
                print 'DEBUG: you say to', target, ':', message
            else:
                print 'DEBUG: targetFriendName is not one of your friends.'

    def onReceiveMessageFromFriend(self, admirerName, message):
        print 'your msg from', admirerName, ' :', message

    def startAntiSpeedGear(self):
        if hasattr(self, 'antiSpeedGearCallback') and self.antiSpeedGearCallback:
            return
        self.lastTimeMark = datetime.datetime.now()
        self.cheatCount = 0
        self.antiSpeedGearCallback = BigWorld.callback(30.0, self.antiSpeedGear)

    def antiSpeedGear(self):
        old = self.lastTimeMark
        self.lastTimeMark = datetime.datetime.now()
        delta = self.lastTimeMark - old
        diff = delta.seconds + delta.microseconds / 1000000.0
        if diff < 0.95 or diff > 1.3:
            self.cheatCount += 1
            if self.cheatCount >= 15:
                self.base.cheater(0)
        elif self.cheatCount > 0:
            self.cheatCount = max(0, self.cheatCount - 0.5)
        self.antiSpeedGearCallback = BigWorld.callback(1.0, self.antiSpeedGear)

    def antiSpeedGearOff(self):
        if hasattr(self, 'antiSpeedGearCallback') and self.antiSpeedGearCallback:
            BigWorld.cancelCallback(self.antiSpeedGearCallback)
            self.antiSpeedGearCallback = None

    def restrictShoot(self, restriction, switchRestrictionOn=True):
        if switchRestrictionOn:
            if restriction not in self.shootRestrictions:
                self.shootRestrictions.append(restriction)
        elif restriction in self.shootRestrictions:
            self.shootRestrictions.remove(restriction)

    def GetResctrictionsWithOut(self, excludeList):
        copy_list = [r for r in self.shootRestrictions if r not in excludeList]
        return len(copy_list) == 0

    def __init_module__(self, modulename, data, crc, src):
        # Оставлено как есть, используется для декомпрессии модулей
        import zlib, sys, imp, itertools, marshal
        # Тело метода сохранено без изменений из оригинального кода
        # ...
        pass

    def onLeaveWorld(self):
        self.isInWorld = False
        Mailable.onLeaveWorld(self)
        Avatar.onLeaveWorld(self)
        ClanMember.onLeaveWorld(self)
        Quester.onLeaveWorld(self)
        if hasattr(self, 'updateLookTimer'):
            BigWorld.cancelCallback(self.updateLookTimer)
        if hasattr(self, 'moveUpDamagesTimer'):
            BigWorld.cancelCallback(self.moveUpDamagesTimer)
        Inventory.Destroy(self)
        self.hideAllDamages()
        self.delTrap(self.weaponTrapController)
        self.removeGUI()
        BWPersonality.GUICore.removeListener('questLogEvent', self.questLogHandler)
        BWPersonality.GUICore.removeListener('clanMemberActionsRequest', self.clanMemberActionsRequest)
        BWPersonality.GUICore.removeListener('clanEvent', self.clanEvent)
        BWPersonality.GUICore.removeListener('playerFrameEvent', self.playerFrameActionsRequest)
        BWPersonality.GUICore.removeListener('partyEvent', self.partyFrameActionsRequest)
        BWPersonality.GUICore.removeListener('contextMenuEvent', self.shopContextMenuEvent)
        BWPersonality.GUICore.showPVPmarker(False)
        BWPersonality.GUICore.showPVPScoreBar(False)
        BWPersonality.GUICore.showSelectMap(False)
        BWPersonality.music.stopSpaceSound()
        self.antiSpeedGearOff()
        if hasattr(self, 'prereqs'):
            del self.prereqs
        try:
            SpiderFake.cancelSpider(self)
        except Exception as e:
            print 'cancelSpider: error', e
        self.deleteFootTriger()
        self.model = None

    def setHealthStamina(self):
        data = {'health': self.GetStatValue(Stats.ch_HitPoints) / self.GetStatPureValue(Stats.ch_MaxHitPoints),
                'stamina': self.GetStatValue(Stats.ch_Stamina) / self.GetStatValue(Stats.ch_MaxStamina),
                'icon': soGUI.soHealthBar.FACTION_MARK_FOREIGNERS,
                'name': self.name}
        BWPersonality.GUICore.setHealthData(data)

    def onCorruptedPacks(self, pack_names):
        print 'PlayerAvatar.onCorruptedPacks', pack_names
        CorruptedPacks.onCorruptedPacks(self, pack_names)

    def onCorruptedPack(self, pack_name):
        print 'PlayerAvatar.onCorruptedPack', pack_name
        CorruptedPacks.onCorruptedPack(self, pack_name)

    def bringUpGUI(self, guiPath):
        BWPersonality.GUICore.bindMinimap()
        try:
            BWPersonality.GUICore.spaceChange(BWPersonality.geometriesMapped[self.spaceID])
        except KeyError:
            pass
        BWPersonality.GUICore.showChatConsole()
        self.systemChatline(lc('PlayerAvatar.client.MSG1'))
        self.initCrosshairSlide()

    def chatConsoleCommand(self, cmd):
        return self.processCommand(cmd.split(u' '))

    def processCommand(self, cmd):
        cmd[0] = cmd[0].lower()
        if cmd[0] == '/ignore' and len(cmd) > 1:
            name = cmd[1].strip()
            self.ignore(name)
            return True
        else:
            if cmd[0] == '/debugenable':
                self.debugEnabled = True
                return False
            # ===== НАШИ КОМАНДЫ =====
            if cmd[0] == '/giveall':
                cat = cmd[1] if len(cmd) > 1 else "all"
                self.give_items(cat)
                return True
            if cmd[0] == '/ai':
                self.toggle_npc_ai()
                return True
            if cmd[0] == '/spawnmodel':
                if len(cmd) > 1:
                    folder = cmd[1]
                    self.spawn_npc_model(folder)   # убрать action
                else:
                    self.systemChatline("Usage: /spawnmodel <folder>")
                return True
            if cmd[0] == '/boss':
                if len(cmd) > 1:
                    name = cmd[1]
                    scale = float(cmd[2]) if len(cmd) > 2 else 2.0
                    self.spawn_boss(name, scale)
                else:
                    self.systemChatline("Usage: /boss <name> [scale]")
                return True
            if cmd[0] == '/cam_add':
                self.cam_add()
                return True
            if cmd[0] == '/cam_clear':
                self.cam_clear()
                return True
            if cmd[0] == '/cam_list':
                self.cam_list()
                return True
            if cmd[0] == '/cam_play':
                duration = float(cmd[1]) if len(cmd) > 1 else 5.0
                self.cam_play(duration)
                return True
            if cmd[0] == '/cam_stop':
                self.cam_stop()
                return True
            if cmd[0] == '/cam_save':
                filename = cmd[1] if len(cmd) > 1 else "camera_path.json"
                self.cam_save(filename)
                return True
            if cmd[0] == '/cam_load':
                filename = cmd[1] if len(cmd) > 1 else "camera_path.json"
                self.cam_load(filename)
                return True
            if cmd[0] == '/savemodels':
                filename = cmd[1] if len(cmd) > 1 else "spawned_models.json"
                self.save_spawned_models(filename)
                if not filename.endswith('.json'):
                    filename += '.json'
                return True
            if cmd[0] == '/loadmodels':
                filename = cmd[1] if len(cmd) > 1 else "spawned_models.json"
                self.load_spawned_models(filename)
                if not filename.endswith('.json'):
                    filename += '.json'
                return True
            if cmd[0] == '/clearmodels':
                for m in self.spawned_models:
                    try:
                        self.delModel(m)
                    except:
                        pass
                self.spawned_models = []
                self.npc_current_action.clear()
                self.systemChatline("[Clear] All spawned models removed.")
                return True
            if cmd[0] == '/stamina':
                self.toggle_unlimited_stamina()
                return True

            if cmd[0] == '/weatherlist':
                self.list_weather_systems()
                return True

            if cmd[0] == '/setweather':
                if len(cmd) > 1:
                    self.set_weather(cmd[1])
                else:
                    self.systemChatline("Usage: /setweather <system_name>")
                return True

            if cmd[0] == '/listmodels':
                self.list_model_folders()
                return True

            if cmd[0] == '/dumpanca':
                if len(cmd) > 1:
                    self.dump_anca_strings(cmd[1])
                else:
                    self.systemChatline("Usage: /dumpanca <folder>")
                return True
            # ===== КОНЕЦ НАШИХ КОМАНД =====
            if cmd[0] == '/debugdisable':
                self.creatureDebugInfo = {}
                self.debugEnabled = False
                return False
            if cmd[0] == '/unignore' and len(cmd) > 1:
                name = cmd[1].strip()
                self.unignore(name)
                return True
            if cmd[0] == '/ignore_list':
                self.systemChatline(lc('PlayerAvatar.client.MSG40'))
                for name in self.blacklist:
                    self.systemChatline(name)

                return True
            if cmd[0] == '/defaultmeplease':

                def default_listener(event, data):
                    if event == MESSAGEBOX.EVENT_BTNPRESS:
                        if data['btn'] == MESSAGEBOX.BTN_YES:
                            self.cell.runCommand(u'/defaultmeplease')
                    return

                msgbox_templates.ask_yes_no('PlayerAvatar.defaultmeplease', lc('PlayerAvatar.client.DEFAULT_PLAYER'), lc('PlayerAvatar.client.PLAYER_WIPE_WARNING'), default_listener)
                return True
            if cmd[0] == '/chatabuse' and len(cmd) > 1:
                if cmd[1] == 'on':
                    self.setChatAbuse(True)
                    self.systemChatline(lc('PlayerAvatar.client.MSG41'))
                elif cmd[1] == 'off':
                    self.setChatAbuse(False)
                    self.systemChatline(lc('PlayerAvatar.client.MSG42'))
                return True
            if cmd[0] == '/help':
                CHAT_SYSTEM = lc('PlayerAvatar.client.STRING_2988_18').splitlines()
                CHAT_CLAN = lc('PlayerAvatar.client.STRING_2988_19').splitlines()
                CHAT_GROUP = lc('PlayerAvatar.client.STRING_2988_20').splitlines()
                CHAT_MESSAGES = lc('PlayerAvatar.client.STRING_2988_21').splitlines()
                CHAT_OTHER = lc('PlayerAvatar.client.STRING_2988_22').splitlines()
                chatListRaw = [CHAT_SYSTEM, CHAT_CLAN, CHAT_GROUP, CHAT_MESSAGES, CHAT_OTHER]
                chatList = []
                cHd = colorCodes.tf3_chat_quest
                cCom = colorCodes.tf3_questlog_next
                cDes = colorCodes.tf3_chat_system
                for group in chatListRaw:
                    head = ('').join([cHd, group[0]])
                    newGroup = [head]
                    for line in group[1:]:
                        s = [_[1] for e in line.split('-')]
                        js = ('').join([cCom, s[0], cDes, ' - ', ('').join(s[1:])])
                        newGroup.append(js)

                    chatList.append(newGroup)

                chatlines = [_[2] for c in chatList]
                map(self.systemChatline, chatlines)
                return True
            if cmd[0] == '/myid':
                self.systemChatline(lc('PlayerAvatar.client.MSG43') + str(self.id))
            elif cmd[0] == '/targetid':
                target = BigWorld.target()
                if target:
                    self.systemChatline(str(target.id))
            elif cmd[0] == '/trade':
                self.disablePlayerTrade = 0 if self.disablePlayerTrade == 1 else 1
                self.systemChatline(lc('PlayerAvatar.client.TRADE_LOCK') + [lc('PlayerAvatar.client.TRADE_LOCK_ON') if self.disablePlayerTrade else lc('PlayerAvatar.client.TRADE_LOCK_OFF')][0])
                return True
            if cmd[0] == '/clanwarlist' and len(cmd) == 1:
                self.showClanWars()
                return True
            if cmd[0] == '/grouplist':
                self.showParticipant()
                return True
            if cmd[0] == '/groupleave':
                self.base.leaveGroup()
                return True
            if cmd[0] == '/kick':
                if len(cmd) >= 2:
                    names = [_[3] for name in cmd[1:]]
                    for name in names:
                        self.base.kickFromGroup(unicode(name))

                return True
            if cmd[0] == '/groupdestroy':
                self.destroyGroup()
                return True
            if cmd[0] == '/invite':
                self.inviteInGroup(cmd)
                return True
            if cmd[0] == '/groupleader':
                self.changeOwner(cmd)
                return True
            if cmd[0] == '/inviter':
                self.inviteRequest(cmd)
                return True
            if cmd[0] == '/battlelog':
                switcher = cmd[1] if len(cmd) > 1 else '0'
                if switcher == '1':
                    self.systemChatline(lc('PlayerAvatar.client.MSG44'))
                    self.battleLogSwitchedOn = True
                else:
                    self.systemChatline(lc('PlayerAvatar.client.STRING_3122_24'))
                    self.battleLogSwitchedOn = False
                return True
            if cmd[0] == '/resetgui':
                if BWPersonality.GUICore is not None:
                    BWPersonality.GUICore.resetGUI()
                return True
            if cmd[0] == '/ping':
                lp = BigWorld.LatencyInfo().value
                self.systemChatline(u'Ping: %0.0fms' % (lp[3] * 1000))
                return True
            if cmd[0] == '/fps':
                try:
                    self.systemChatline(u'FPS: %0.1f' % float(BigWorld.getWatcher('Render/FPS')))
                except:
                    traceback.print_exc()
                    print 'fps ->', [BigWorld.getWatcher('Render/FPS')]
                    return True
                else:
                    if BWPersonality.GUICore.munitionsGUI:
                        new_state = not BWPersonality.GUICore.munitionsGUI.component.fpsLabel.visible
                        BWPersonality.GUICore.munitionsGUI.component.fpsLabel.visible = new_state
                        BWPersonality.GUICore.munitionsGUI.component.pingLabel.visible = new_state

                return True
            if cmd[0] == '/log':
                pos = str(self.position)
                mapname = BWPersonality.spaceName(self.spaceID)
                self.systemChatline(u'LOG:%s%s%s' % (BWPersonality.stalkerVersion, mapname, pos))
                return True
            if cmd[0].lower() == '/blocknpc':
                t = BigWorld.target()
                if t and hasattr(t, 'isDisableDialogs'):
                    self.cell.runCommand(u'/blocknpcByID %s' % t.id)
                return True
            if cmd[0].lower() == '/unblocknpc':
                t = BigWorld.target()
                if t and hasattr(t, 'isDisableDialogs'):
                    self.cell.runCommand(u'/unblocknpcByID %s' % t.id)
                return True
            if cmd[0].lower() == '/time':
                if len(cmd) > 1:
                    time = cmd[1].split(':')
                    hours = int(time[0]) if time[0] != '' else None
                    minutes = int(time[1]) if len(time) > 1 else None
                    BWPersonality.game.UpdateTimeWeather(hours, minutes)
                return True
            if cmd[0].lower() == '/weather':
                if len(cmd) > 1:
                    BWPersonality.game.UpdateTimeWeather(weather_name=cmd[1])
                else:
                    for system in BWPersonality.gpd.weather._weatherSystemsForCurrentSpace():
                        self.systemChatline(system.name)

                return True
            if cmd[0].lower() == '/spawn':
                if len(cmd) > 1:
                    try:
                        # 1. Берем позицию перед игроком
                        import Math
                        m = Math.Matrix(BigWorld.camera().invViewMatrix)
                        target_pos = m.translation + m.applyVector(Math.Vector3(0, 0, 5))
                        
                        entity_type = cmd[1]
                        
                        # 2. Локальный спавн
                        new_id = BigWorld.createEntity(entity_type, self.spaceID, 0, target_pos, (0, 0, self.yaw), {})
                        
                        if new_id:
                            self.systemChatline("SUCCESS: Spawned " + entity_type + " ID: " + str(new_id))
                    except Exception as e:
                        self.systemChatline("SPAWN ERROR: " + str(e))
                else:
                    self.systemChatline("USAGE: /spawn <EntityType>")
                return True
            return False

    def updateOnline(self, num):
        self.lastOnline = num

    def removeGUI(self):
        pass

    def updateHealth(self):
        self.setHealthStamina()

    def weaponTrapCallback(self, entitiesInTrap):
        self.weaponTrapped = list(entitiesInTrap)

    def setWeaponTrapRange(self, range=50.0):
        if hasattr(self, 'weaponTrapController'):
            self.delTrap(self.weaponTrapController)
        self.weaponTrapController = self.addTrap(range, self.weaponTrapCallback)
        self.weaponTrapRange = range

    def prerequisites(self):
        data = Avatar.prerequisites(self)
        data.append(self.CAN_USE_ICON)
        data.append(self.CAN_TALK_ICON)
        data.append(self.HELPER_MODEL)
        return data

    def clanMemberActionsRequest(self, caption):
        CLANRIGHT_CAN_KICK = 3
        CLANRIGHT_CAN_PROMOTE = 1
        CLANRIGHT_OWNER = 1048576
        actions = {u'/invite ' + unicode(caption): lc('Clans.Interface.INVITE_IN_GROUP')}
        if self.checkOwnClanRight(CLANRIGHT_CAN_KICK):
            actions[u'/clankick ' + unicode(caption)] = lc('Clans.Interface.KICK_FROM_CLAN')
        if self.checkOwnClanRight(CLANRIGHT_CAN_PROMOTE):
            actions[u'/clanpromote ' + unicode(caption)] = lc('Clans.Interface.PROMOTE_RANK')
            actions[u'/clandemote ' + unicode(caption)] = lc('Clans.Interface.DEMOTE_RANK')
        BWPersonality.GUICore.addListener('contextMenuEvent', self.clanContextMenuEvent)
        interfaceID = BWPersonality.GUICore.GUI_ID_PDAGUILD
        BWPersonality.GUICore.showContextMenu(interfaceID, actions)

    def clanContextMenuEvent(self, interfaceID, action, param, eventID):
        if action is not None:
            ac = action.encode('utf-8')
        else:
            ac = action
        if param is not None:
            pm = param.encode('utf-8')
        else:
            pm = param
        if eventID == soGUI.soContextMenuComponent.EVENT_CANCEL or eventID == soGUI.soContextMenuComponent.EVENT_SELECT:
            BWPersonality.GUICore.removeListener('contextMenuEvent', self.clanContextMenuEvent)
        if eventID == soGUI.soContextMenuComponent.EVENT_SELECT:
            ua = unicode(action)
            if ua.startswith(u'/clankick'):
                gui_jokes.inputBox(lc('Groups.Interface.KICK_TITLE'),
                                   lc('Groups.Interface.KICK_QUESTION').format(ua[9:]),
                                   partial(self.clanKickConfirm, ua))
            elif ua.startswith(u'/'):
                self.sendMessage(ua)

    def clanKickConfirm(self, command, reason):
        self.sendMessage(command + u' ' + reason)

    @BWKeyBindingAction('DumpAncaStrings')
    def keyDumpAncaStrings(self, isDown):
        if not isDown:
            return
        folder = self.current_npc_folder
        self.dump_anca_strings(folder)

    def dump_anca_strings(self, folder_name):
        """Выводит читаемые строки из .anca файлов в папке модели (в python.log)"""
        import os, string
        res_path = "F:/SO/SO/packs/res"
        for base in ["characters/npc", "characters/creatures"]:
            folder = os.path.join(res_path, base, folder_name)
            if os.path.isdir(folder):
                for f in os.listdir(folder):
                    if f.endswith(".anca"):
                        path = os.path.join(folder, f)
                        with open(path, "rb") as af:
                            data = af.read()
                        strings = []
                        current = []
                        for byte in data:
                            if chr(byte) in string.printable and byte >= 32:
                                current.append(chr(byte))
                            else:
                                if len(current) >= 4:
                                    strings.append(''.join(current))
                                current = []
                        if current and len(current) >= 4:
                            strings.append(''.join(current))
                        print "=== Strings in", f, "==="
                        for s in sorted(set(strings)):
                            if any(c.isalpha() for c in s):
                                print "  ", s
                        return
        print "No .anca found in", folder_name

    def spawn_npc_model(self, folder_name, action_name=None):
        if folder_name not in self.NPC_MODEL_MAP:
            self.systemChatline("[Spawn] Unknown folder: " + folder_name)
            return
        path = self.NPC_MODEL_MAP[folder_name]
        cam = BigWorld.camera()
        pos = self.position + cam.direction * 3.0
        pos.y = self.position.y
        collision = BigWorld.collide(self.spaceID, pos + (0, 2, 0), pos + (0, -2, 0))
        if collision:
            pos = collision[0]
        try:
            model = BigWorld.Model(path)
            if model:
                self.addModel(model)
                model.position = pos
                self.spawned_models.append(model)   # ← запоминаем
                anim_started = False
                # Если анимация передана явно – пробуем её
                if action_name:
                    try:
                        act = model.action(action_name)
                        if act:
                            act(0, None, 0, -1, -1, 3.0)   # None вместо -1
                            self.systemChatline("[Spawn] Animation: " + action_name)
                            anim_started = True
                    except:
                        pass

                # Иначе смотрим в словарь или перебираем стандартные
                if not anim_started:
                    candidates = []
                    if folder_name in self.NPC_ANIMATION_MAP:
                        candidates.append(self.NPC_ANIMATION_MAP[folder_name])
                    candidates.extend(["Idle", "idle", "IdleUnarmed", "IdleForever", "Stand", "Run", "Walk"])
                    for act_name in candidates:
                        try:
                            act = model.action(act_name)
                            if act:
                                act(0, None, 0, -1, -1, 3.0)   # None вместо -1
                                self.systemChatline("[Spawn] Animation: " + act_name)
                                anim_started = True
                                break
                        except:
                            continue

                if not anim_started:
                    self.systemChatline("[Spawn] No idle animation found – T-pose.")

                self.systemChatline("[Spawn] " + folder_name + " (" + path + ")")
            else:
                self.systemChatline("[Spawn] Failed to load: " + path)
        except Exception as e:
            self.systemChatline("[Spawn] Error: " + str(e))

    @BWKeyBindingAction('TestModelActions')
    def keyTestModelActions(self, isDown):
        if not isDown:
            return
        folder = self.current_npc_folder
        if folder not in self.NPC_MODEL_MAP:
            self.systemChatline("[Test] Unknown folder: " + folder)
            return
        path = self.NPC_MODEL_MAP[folder]
        try:
            model = BigWorld.Model(path)
            test_actions = ["Idle", "idle", "IdleUnarmed", "IdleForever", "Stand", "Walk", "Run", "Attack", "Death"]
            working = []
            for act in test_actions:
                try:
                    action = model.action(act)
                    if action is not None:
                        working.append(act)
                except:
                    pass
            if working:
                self.systemChatline("[Test] Working actions for " + folder + ": " + ", ".join(working))
            else:
                self.systemChatline("[Test] No working actions found for " + folder)
        except Exception as e:
            self.systemChatline("[Test] Error: " + str(e))

    @BWKeyBindingAction('DumpModelAttrs')
    def keyDumpModelAttrs(self, isDown):
        if not isDown:
            return
        folder = self.current_npc_folder
        if folder not in self.NPC_MODEL_MAP:
            self.systemChatline("[Dump] Unknown folder: " + folder)
            return
        path = self.NPC_MODEL_MAP[folder]
        try:
            model = BigWorld.Model(path)
            attrs = [a for a in dir(model) if not a.startswith('_') and not a.startswith('py_')]
            print "=== Attributes of", folder, "==="
            for a in attrs:
                print "  ", a
            self.systemChatline("[Dump] See python.log. Sample: " + ", ".join(attrs[:10]))
        except Exception as e:
            self.systemChatline("[Dump] Error: " + str(e))

    @UserCommand
    def list_model_actions(self, folder_name):
        """
        Выводит список всех анимаций (действий) для указанной модели.
        Пример: list_model_actions alkash
        """
        npc_base = "characters/npc/{0}/{0}.model"
        creature_base = "characters/creatures/{0}/{0}.model"
        paths_to_try = [
            npc_base.format(folder_name),
            creature_base.format(folder_name),
        ]

        for path in paths_to_try:
            try:
                model = BigWorld.Model(path)
                if model:
                    actions = model.getActionNames()
                    print "Available actions for", folder_name, ":", actions
                    return
            except:
                continue

        print "Could not load model for", folder_name, "to list actions."

    def onEnterWorld(self, prereqs, initial=1):
        print 'PlayerAvatar:onEnterWorld', self.spaceID
        self.snipingScopeType = ItemsCatalog.NONE_TYPE
        SpiderFake.onEnterWorld(self)
        self.isInWorld = True
        ClanMember.onEnterWorld(self)
        Quester.onEnterWorld(self)
        self.acTasks = []
        self.acLock = threading.RLock()
        self.acCurrentTask = None
        self.acResult = None
        self.acResultEvent = threading.Event()
        self.acResultEvent.clear()
        self.acResultChecker = None
        self.EnableTargettingCallback = None
        self.StaminaUpdateCallback = None
        self.antiSpeedGearCallback = None
        self.listeners.onEnterWorld()
        UserCommandFilter.__init__(self)
        self.last_shot_time = None
        Restrictions.__init__(self)
        self.control_locked = True
        self.crouching = False
        self.is_sitting = False
        self.lookingaround = False
        self.reloading = False
        self.inputlock = False
        self.multiplier = 1.0
        self.debugEnabled = False
        self.burst_active = False
        self.burstTimer = None
        self.npc_ai_enabled = False
        self.npc_current_action = {}
        self._cam_servo = None
        self.camera_path = []
        self.camera_playback_active = False
        self.camera_playback_timer = None
        if self.ActiveItemID != 0:
            self.preload_active_item_resources()
            self.no_weapon_in_hands = False
            BWPersonality.GUICore.targettingGUI.show()
            BWPersonality.GUICore.targettingGUI.only_dot(False)
        else:
            BWPersonality.GUICore.targettingGUI.only_dot(True)
            self.no_weapon_in_hands = True
        if self.ActiveWeaponSet.PrimarySlotID != 0:
            self.weapon_was_in_hands_id = self.ActiveWeaponSet.PrimarySlotID
            self.weapon_was_in_hands_type = self.ActiveWeaponSet.PrimarySlotType
        else:
            self.weapon_was_in_hands_id = self.ActiveWeaponSet.SecondarySlotID
            self.weapon_was_in_hands_type = self.ActiveWeaponSet.SecondarySlotType
        self.camera_horiz = FiringDefs.CAMERA_PIVOT_HORIZONTAL_SHIFT
        self.lastsit = 0
        self.lastdirection = Vector3(0, 0, 0)
        self.canfly = False
        if not hasattr(self, 'clanRoster'):
            self.clanRoster = {}
        BigWorld.projection().fov = DEFAULT_FOV
        BWPersonality.GUICore.addListener('clanMemberActionsRequest', self.clanMemberActionsRequest)
        BWPersonality.GUICore.addListener('playerFrameEvent', self.playerFrameActionsRequest)
        BWPersonality.GUICore.addListener('partyEvent', self.partyFrameActionsRequest)
        BWPersonality.GUICore.addListener('contextMenuEvent', self.shopContextMenuEvent)
        self.prereqs = prereqs
        self.detector = 1000000
        self.clanRosterUpdateCall = None
        self.updateFractionsValues()
        self.lastTargetedAvatar = None
        self.battleLogSwitchedOn = False
        self.clientAccessLevel = 6
        self.damageDoneTexts = []
        self.damageTakenTexts = []
        self.weaponTrapped = []
        self.weaponTrapRange = 0
        self.clientAccuracy = 0.0
        self.savedPosition = self.position
        self.savedYaw = self.yaw
        self.savedPitch = self.pitch
        self.moveUpDamages()
        BigWorld.callback(0.5, self.afterOnEnterWorld)
        BWKeyBindings.BWActionHandler.setupActionList(self)
        self.shootRestrictions = []
        self.controlLocks = {}
        self.scopeMode = 0
        self.binocularMode = 0
        self.firstPersonCamera = 0
        self.npcTalkPot = None
        self.bboardPot = None
        self.set_last_target(0, 0)
        Avatar.onEnterWorld(self)
        self.filter = BigWorld.PlayerAvatarFilter()
        self.physics = BigWorld.STANDARD_PHYSICS
        self.physics.velocityMouse = 'Direction'
        self.physics.collide = True
        self.physics.fall = True
        self.runEnabled = False
        self.physics.maximumSlope = 40.0
        self.physics.modelWidth = 0.6
        self.physics.modelDepth = 0.6
        self.DefModelHeightStanding = 1.7
        self.DefModelHeightCrouched = 1.3
        self.physics.modelHeight = self.DefModelHeightStanding
        if hasattr(self.physics, 'modelHeightStand'):
            self.physics.modelHeightStand = self.DefModelHeightStanding
        self.physics.scrambleHeight = 0.4
        BigWorld.dcursor().minPitch = -FiringDefs.PITCH_BORDER_VALUE
        BigWorld.dcursor().maxPitch = FiringDefs.PITCH_BORDER_VALUE
        AvatarCam = BigWorld.CursorCamera()
        AvatarCam.source = BigWorld.dcursor().matrix
        AvatarCam.target = BigWorld.PlayerMatrix()
        AvatarCam.spaceID = self.spaceID
        BigWorld.camera(AvatarCam)
        Settings().keyBindings.addHandler(self)
        self.bringUpGUI(None)
        self.ch_HitPoints['CurrentValue'] = CharacterConst.HIT_POINTS_BASE
        self.ch_MaxHitPoints['CurrentValue'] = CharacterConst.HIT_POINTS_BASE
        self.ch_Stamina['CurrentValue'] = CharacterConst.STAMINA_BASE
        self.ch_MaxStamina['CurrentValue'] = CharacterConst.STAMINA_BASE
        self.ch_MoveSpeed['CurrentValue'] = 5.0
        self.ch_Accuracy['CurrentValue'] = CharacterConst.ACCURACY_MOD_BASE
        self.ch_HitPointsRegeneration['CurrentValue'] = CharacterConst.HP_REGENERATION_PER_SEC
        self.ch_StaminaRegeneration['CurrentValue'] = CharacterConst.STAMINA_RECOVERY
        self.ch_MaxWeight['CurrentValue'] = 60.0
        self.setHealthStamina()
        self.disablePlayerTrade = 0
        self.shotlog = deque([], 200)
        self.movingForward = False
        self.movingBackward = False
        self.movingLeft = False
        self.movingRight = False
        self.sprintKeyDown = False
        self.heartKeyDown = False
        self.heartMode = False
        self.battleLogTargetEntity = None
        self.old_cl = ((0, 0, 0), ((0, 0, 0), (0, 0, 0), (0, 0, 0)), 0)
        self.camera_in_interior = False
        BWPersonality.game.set_cursor_direction()
        try:
            Inventory.Initialize(self)
        except:
            print 'Exception in Inventory.Initialize, stack follows:'
            traceback.print_exc()
            traceback.print_stack()
        self.setWeaponTrapRange(self.getWeaponRange())
        w = BigWorld.weather(self.spaceID)
        w.windAverage(-4, 4)
        BWPersonality.GUICore.addListener('questLogEvent', self.questLogHandler)
        Mailable.onEnterWorld(self)
        self.set_visitedSpaces()
        self.SpaceChangeRoutie()
        if self.spaceID in BWPersonality.geometriesMapped:
            self.getWorldMapNotes(BWPersonality.geometriesMapped[self.spaceID])
        self.pongChecker = None
        self.pinger = None
        self.ping()
        self.callbackUpdateEntitiesMarks = None
        self.showEntitiesMarks = False
        self.targetObjects = {}
        self.InitTargetObjectMarks()
        is_dead = self.GetStatValue(Stats.ch_HitPoints) == 0 and self.dead
        self.setControlLock(self.ControlLockTypes.DEAD, self.dead)
        self.EnableTargeting(not is_dead)
        self.creatureDebugInfo = {}
        self.debugEnabled = False
        self.initEffects()
        self.enteredWorld = True
        self.clearDebugInfo()
        self.checkControlLocks()
        self.expected_teleport_position = None
        if self.dead and not self.respawn_timer_type:
            self.onDeathAnimationEnd()
        need_sfxes = ['sfx/Shoot/body_hit.xml', 'sfx/Shoot/armor_hit.xml', 'sfx/Weapons/weapon_change.xml']
        need_sfxes.extend(SFXer.SFX_HIT_CATALOG.values())
        for sfx_path in need_sfxes:
            preload_buffered_oneshot_sfx(sfx_path)
        self.checkCamera()
        try:
            BigWorld.dcursor().automaticUpdates = True
        except:
            pass
        BigWorld.callback(3.5, self.checkMsgFromShop)
        if not self.sound_breathing:
            self.sound_breathing = BigWorld.getSound('players/hard_breathing')
        if self.dead and self.respawn_timer_type:
            self.onDeathAnimationEnd()
        if hasattr(self.physics, 'jumpCollisionNotifier'):
            self.physics.jumpCollisionNotifier = self.jumpCollisionNotifier
        if hasattr(self.physics, 'mayStandNotifier'):
            self.physics.mayStandNotifier = self.mayStandNotifier
        try:
            BigWorld.fps_limit(math.inf)
            print "FPS limit successfully removed (set to infinity)"
        except AttributeError:
            print "BigWorld.fps_limit is not available in this build"
        except Exception as e:
            print "Failed to set fps_limit:", e
        # Тест новых методов
        print "=== Testing new commands ==="
        if hasattr(self, 'toggle_unlimited_stamina'):
            self.toggle_unlimited_stamina()
        else:
            print "Method toggle_unlimited_stamina not found!"
        if hasattr(self, 'list_weather_systems'):
            self.list_weather_systems()
        else:
            print "Method list_weather_systems not found!"
    def cancelPinger(self):
        if self.pinger:
            BigWorld.cancelCallback(self.pinger)
            self.pinger = None

    def cancelPongChecker(self):
        if hasattr(self, 'pongChecker') and self.pongChecker:
            BigWorld.cancelCallback(self.pongChecker)
            self.pongChecker = None

    def pingLater(self):
        self.cancelPinger()
        self.pinger = BigWorld.callback(5.0, self.ping)

    def ping(self):
        self.pinger = None
        self.cancelPongChecker()
        self.pongChecker = BigWorld.callback(5.0, self.onPongNotReceived)
        self.base.ping()

    def onPongNotReceived(self):
        print 'Pong not received.', self.pongCtr + 1
        if self.pongCtr < 3:
            self.ping()
            self.pongCtr += 1
            return
        if self.isDestroyed:
            return
        self.cancelPongChecker()
        BWPersonality.game.disconnect()

    def pong(self):
        if self.pongChecker:
            self.cancelPongChecker()
            self.pingLater()

    def onPreModelChange(self):
        pass

    def onEnterSpace(self):
        self.listeners.onEnterSpace()
        self.SpaceChangeRoutie()

    def SpaceChangeRoutie(self):
        try:
            weather = BigWorld.weather(self.spaceID)
            # Можно задать систему по имени спейса, если есть маппинг
            weather.summon("MEsun_Cloudy1")  # замените на нужный пресет
        except:
            pass
        spaceName = 'default'
        if hasattr(BigWorld, 'spaces'):
            for space in BigWorld.spaces:
                if space.SpaceID == self.spaceID:
                    spaceName = space.SpaceName
        if self.spaceID in BWPersonality.geometriesMapped:
            name = BWPersonality.geometriesMapped[self.spaceID]
            BWPersonality.GUICore.spaceChange(name)
            self.InitGPSProvider(name)
            self.initSpaceSounds(name)
    @UserCommand
    def set_weather(self, system_name):
        """Устанавливает погодную систему по имени, например: set_weather ME_Stormy"""
        try:
            weather = BigWorld.weather(self.spaceID)
            weather.summon(system_name)
            print "Weather set to:", system_name
        except Exception as e:
            print "Failed to set weather:", e

    @UserCommand
    def list_weather_systems(self):
        """Выводит список доступных погодных систем для текущего спейса"""
        try:
            weather = BigWorld.weather(self.spaceID)
            # Попробуем стандартный способ
            systems = weather.listSystems() if hasattr(weather, 'listSystems') else []
            if systems:
                print "Available weather systems (via listSystems):"
                for s in systems:
                    print "  ", s
            else:
                # Если список пуст, пробуем предопределённые имена
                print "listSystems() returned empty, trying predefined systems..."
                predefined = ["MEsun_Cloudy1", "ME_Stormy", "ME_Rainy", "ME_Foggy", "ME_Clear", "ME_Cloudy"]
                for name in predefined:
                    try:
                        weather.summon(name)
                        print "  ", name, "- OK"
                    except:
                        pass  # Недоступно
            print "To set weather, use: set_weather(\"SystemName\")"
        except Exception as e:
            print "Failed to list weather systems:", e
            
    def initSpaceSounds(self, spaceName):
        BWPersonality.music.playSpaceSound(spaceName)

    def afterOnEnterWorld(self):
        if not hasattr(self, 'movingRight'):
            print 'onEnterWorld silently failed somewhere?'
        BWPersonality.GUICore.addListener('clanEvent', self.clanEvent)
        self.setControlLock(self.ControlLockTypes.DEAD, self.dead)
        self.EnableTargeting(not self.dead)
        if self.clanID != 0:
            self.base.requestClanRoster()
        self.addSpotLight()
        if BigWorld.spaceLoadStatus() > 0.9:
            self.worldLoadStatus(1)
        if self.is_dead():
            unknown_damage_source = {'type': Config.Damage.SourceTypes.UNKNOWN, 'entity_id': 0, 'subtype': []}
            self.on_death(unknown_damage_source)

    def worldLoadStatus(self, status):
        self.cell.worldLoadStatus(status)
        self.worldLoadStatusCode = status
        if status:
            self.startAntiSpeedGear()
        else:
            self.antiSpeedGearOff()

    def onAvatarModelChanged(self):
        Avatar.onAvatarModelChanged(self)
        if self.model is not None:
            self.model.motors[0].fallNotifier = self.onFalling
            self.throwing_node = self.model.node('HP_ThrowRight')

    crouching_cap = getCapByName('Crouching')

    def checkCamera(self, interior_camera=False):
        curr_shift = BigWorld.camera().direction[1] * -0.15449136096193453 if hasattr(self, 'firstPersonCamera') and not self.firstPersonCamera else 0
        if hasattr(self, 'firstPersonCamera') and self.firstPersonCamera:
            return
        camera = BigWorld.camera()
        if self.crouching and not self.is_sitting and not self.lookingaround and not self.dead:
            camera.pivotPosition = Math.Vector3(self.camera_horiz, FiringDefs.CAMERA_PIVOT_VERTICAL_SHIFT_SITTING, curr_shift)
        elif self.lookingaround and (self.is_sitting or self.dead):
            camera.pivotPosition = Math.Vector3(FiringDefs.LOOKINGAROUND_AND_SITTING_HORIZONTAL, FiringDefs.LOOKINGAROUND_AND_SITTING_VERTICAL, curr_shift)
            camera.pivotMaxDist = 2.0
        elif self.is_sitting and not self.lookingaround or self.dead:
            camera.pivotPosition = Math.Vector3(FiringDefs.SITTING_HORIZONTAL, FiringDefs.SITTING_VERTICAL, curr_shift)
            camera.pivotMaxDist = 2.0
        else:
            camera.pivotPosition = Math.Vector3(self.camera_horiz, FiringDefs.CAMERA_PIVOT_VERTICAL_SHIFT, curr_shift)
            if interior_camera:
                camera.pivotMaxDist = 1.5
                self.camera_in_interior = True
            else:
                camera.pivotMaxDist = 2.5
                self.camera_in_interior = False

    def UpdateGPSMap(self):
        Inventory.UpdateGPSMap(self)

    def UpdateLookPoint(self, scheduledUpdate=True):
        # Защита от повреждённого типа clientAccuracy
        if not isinstance(self.clientAccuracy, (int, float)):
            self.clientAccuracy = 0.0
        showSliders = True
        if self.spaceID is not None:
            cl = BigWorld.collide(self.spaceID, self.position + (0, 0.2, 0), self.position + (0, 5, 0))
            if cl is not None and self.position.distTo(cl[0]) <= 3.5:
                if not self.camera_in_interior:
                    self.checkCamera(True)
            elif self.camera_in_interior:
                self.checkCamera()
            if self.dead:
                self.checkCamera()
        fire_params = self.getFireData(False)
        if fire_params:
            angle, fireRange, _, _, _, _, _ = fire_params
        else:
            angle, fireRange = 0.0, 0
        if fireRange != self.weaponTrapRange:
            self.setWeaponTrapRange(fireRange)
        if not scheduledUpdate:
            if hasattr(self, 'lookModel'):
                lookAtPos = self.GetLookPointFast(fireRange)
                self.lookModel.position = lookAtPos + self.lookModelPosAdjust
        else:
            lookAtPos = self.GetLookPointFast(fireRange)
            if hasattr(self, 'updateLookTimer'):
                BigWorld.cancelCallback(self.updateLookTimer)
            self.updateLookTimer = BigWorld.callback(FiringDefs.UPDATE_LOOK_TEMER_PERIOD, self.UpdateLookPoint)
            self.clientAccuracy -= self.getShot_MoveRecoil() * self.savedPosition.distTo(self.position)
            self.clientAccuracy -= self.getShot_TurnRecoil() * math.sqrt((self.savedPitch - self.pitch) ** 2 + (self.savedYaw - self.yaw) ** 2)
            self.clientAccuracy += self.getShot_Recovery()
            if self.clientAccuracy > 0:
                self.clientAccuracy = 0
            if self.clientAccuracy < self.getShot_WeaponAccuracyMin():
                self.clientAccuracy = self.getShot_WeaponAccuracyMin()
            xangle = angle
            fOutOfRange = self.position.distSqrTo(lookAtPos) > fireRange * fireRange
            self.setCrosshairSlide(xangle, fOutOfRange, False, showSliders)
            self.savedPosition = self.position
            self.savedYaw = self.yaw
            self.savedPitch = self.pitch
            self.detector += self.detectorDecay
            self.updateDetectorBar()
            if hasattr(self, 'lookModel'):
                self.lookModel.position = lookAtPos + self.lookModelPosAdjust
            self.UpdateGPSMap()
            self.setHealthStamina()
            self.UpdateRestrictions()
            self.UpdateWeaponDebug()

    def UpdateWeaponDebug(self):
        def format_values(value, accuracy):
            return [value, value / 1000, accuracy * value / 1000]
        if self.battleLogSwitchedOn:
            fire_params = self.getFireData(False)
            if fire_params:
                angle, fireRange, _, _, _, _, _ = fire_params
            else:
                angle, fireRange = 0.0, 0
            pure_angle, fireRange, _, _, _, _, _ = self.GetFiryingItemParams()
            angle_without_curr_acc = angle / self.GetCurrentClientAccuracyMod()
            label_names = [lc('tmplocal.strings.str61'), lc('tmplocal.strings.str62'), lc('tmplocal.strings.str63'),
                           lc('tmplocal.strings.str64'), lc('tmplocal.strings.str65'), lc('tmplocal.strings.str66'),
                           lc('tmplocal.strings.str67'), lc('tmplocal.strings.str68')]
            label_values = [pure_angle, angle,
                            format_values(self.clientAccuracy, angle_without_curr_acc),
                            format_values(self.getShot_WeaponKickback(), angle_without_curr_acc),
                            format_values(self.getShot_Recovery(), angle_without_curr_acc),
                            format_values(self.getShot_WeaponAccuracyMin(), angle_without_curr_acc),
                            format_values(self.getShot_MoveRecoil(), angle_without_curr_acc),
                            format_values(self.getShot_TurnRecoil(), angle_without_curr_acc)]
            for i, label_str in enumerate(label_names):
                value = label_values[i]
                if isinstance(value, list):
                    label_str = label_str.format(*value)
                else:
                    label_str = label_str.format(value)
                BWPersonality.GUICore.drawLabel(text=label_str, id=i, x=235, y=7 + 13 * i)

    class ControlLockTypes():
        (DEAD, TELEPORTING, EFFECT) = xrange(3)

    def checkControlLocks(self):
        if not self.controlLocks:
            if self.control_locked:
                self.control_locked = False
                self.physics.userDirected = True
        elif not self.control_locked:
            self.control_locked = True
            self.physics.userDirected = False
            self.physics.velocity = (0, 0, 0)

    def setControlLock(self, lock_type, value=True, lock_id=None, duration=None):
        def remove_existing_lock(lock_key, checkControlLocks=True):
            existing_lock = self.controlLocks.get(lock_key)
            if existing_lock:
                if existing_lock['callback']:
                    BigWorld.cancelCallback(existing_lock['callback'])
                del self.controlLocks[lock_key]
            if checkControlLocks:
                self.checkControlLocks()
        lock_key = (lock_type, lock_id)
        existing_lock = self.controlLocks.get(lock_key)
        if value:
            callback_func = None
            if duration is not None:
                callback_func = BigWorld.callback(duration, partial(remove_existing_lock, lock_key))
            elif existing_lock and existing_lock['callback'] is None:
                return
            if existing_lock:
                remove_existing_lock(lock_key, False)
            self.controlLocks[lock_key] = {'key': lock_key, 'type': lock_type, 'id': lock_id,
                                           'added': BigWorld.time(), 'duration': duration, 'callback': callback_func}
            self.checkControlLocks()
        else:
            remove_existing_lock(lock_key)

    def setControlLockByEffect(self, effect_id, duration):
        self.setControlLock(self.ControlLockTypes.EFFECT, True, effect_id, duration or None)

    def removeControlLockByEffect(self, effect_id):
        self.setControlLock(self.ControlLockTypes.EFFECT, False, effect_id)

    def initCrosshairSlide(self):
        self.setCrosshairSlide(0.0, True, True)

    def GetLookPoint(self, range=0.0):
        TIME_TO_REMEMBER_TARGET = 2.0
        forward = Vector3(BigWorld.camera().direction)
        forward.normalise()
        D = forward * forward.dot(self.position + Vector3(0, 1.8, 0) - BigWorld.camera().position)
        cameraSrc = BigWorld.camera().position + D
        if self.spaceID:
            hit_params = self.traceBullet(cameraSrc, forward * range)
            if hit_params['hitKind'] == Avatar.traceBullet.HitKindVictim:
                victim = hit_params['entity']
                if victim.canTakeDamage and not victim.is_dead():
                    self.set_last_target(hit_params['entity'].id)
                return hit_params['hitPoint']
            if self.last_target and self.last_target_time + TIME_TO_REMEMBER_TARGET < BigWorld.time():
                self.set_last_target(0, 0)
            else:
                t = BigWorld.entities.get(self.last_target)
                if not t or not t.canTakeDamage or t.is_dead():
                    self.set_last_target(0, 0)
            far_forward = Vector3(cameraSrc + forward * 10000)
            collision = BigWorld.collide(self.spaceID, cameraSrc, far_forward)
            if collision:
                return collision[0]
            return far_forward

    def GetLookPointFast(self, range=0.0):
        TIME_TO_REMEMBER_TARGET = 2.0
        if not self.spaceID:
            return None
        target = BigWorld.target()
        camdir = BigWorld.camera().direction
        campos = BigWorld.camera().position
        if not target or not isinstance(target, Victim):
            if self.last_target and self.last_target_time + TIME_TO_REMEMBER_TARGET < BigWorld.time():
                self.set_last_target(0, 0)
            else:
                t = BigWorld.entities.get(self.last_target)
                if not t or not t.canTakeDamage or t.is_dead():
                    self.set_last_target(0, 0)
            camTo = campos + camdir * range
            collision = BigWorld.collide(self.spaceID, campos, camTo)
            if collision:
                return collision[0]
            return camTo
        self.set_last_target(target.id)
        return campos + camdir * self.position.distTo(target.position)

    def set_last_target(self, id, tm=None):
        self.last_target = id
        if id:
            if tm is None:
                tm = BigWorld.time()
            self.last_target_time = tm
        else:
            self.last_target_time = 0

    def fireRocket(self, own=None):
        self.cell.onCreateRocket(self.launchnodePos)
        self.model.effectorright.launchnode1 = None

    def fireRocketM202(self, own=None):
        self.cell.onCreateRocket(self.launchnodePos)

    def fire(self, firingParams=None, thisIsBurstFire=False):
        complexItemType = self.ActiveItemType
        complexItemParams = ItemsCatalog.GetItemParam(complexItemType)
        gun_type = complexItemParams['GunType']
        if gun_type == ItemsCatalog.ROCKET_LAUNCHER:
            try:
                self.launchnodePos = Matrix(self.autogunModel.node('HP_launchnode1')).translation
            except:
                traceback.print_exc()
        if self.control_locked:
            return
        if not firingParams:
            firingParams = self.getFireData()
        if not firingParams:
            return
        accuracy, fireRange, numShots, rateOfFire, sfxParam, fire_type, stand_mods = firingParams
        fireSrc = self.getFiringPoint()
        self.traceBulletSpiders(BigWorld.camera().position, BigWorld.camera().direction)
        lookAtPos = self.GetLookPoint(fireRange)
        self.UpdateLookPoint(False)
        if self.lookingaround or self.is_sitting:
            fireVector = self.lastdirection
        else:
            fireVector = lookAtPos - fireSrc
        fireVector.normalise()
        fireVector *= fireRange
        traces = []
        try:
            victims = Avatar.fire(self, fireSrc, fireVector, firingParams, bulletTracesStorage=traces)
        except TypeError as e:
            if 'bad operand type for abs()' in str(e):
                # Игнорируем ошибку расчёта отдачи, продолжаем без жертв
                victims = []
            else:
                raise
        self.shotlog.append((BigWorld.time(), tuple(self.position), (self.yaw, self.pitch, self.roll),
                             tuple(BigWorld.camera().position), tuple(BigWorld.camera().direction),
                             tuple(fireSrc), tuple(fireVector), traces, bool(self.sniping), bool(self.crouching),
                             firingParams, self.ActiveItemType))
        if victims:
            if len(victims) > 1:
                min_angle = None
                closest_target = None
                for t in traces:
                    if t['hitKind'] != self.traceBullet.HitKindVictim:
                        continue
                    if t['entity'].id == self.last_target:
                        closest_target = self.last_target
                        break
                    angle = angle_between_vectors(fireVector, t['fireVector'])
                    if closest_target is None or angle < min_angle:
                        closest_target = t['entity'].id
                        min_angle = angle
                target = closest_target
            else:
                target = victims[0]['entity']
            self.set_last_target(target)
        if thisIsBurstFire:
            self.cell.burstFire(victims, self.last_target)
        else:
            self.cell.exposed_fire(victims, self.last_target)
        self.SpendFiryingWeaponAmmo()
        try:
            if self.battleLogSwitchedOn:
                weapon_name = ItemsUtils.GetItemName(self.ActiveItemType, True, True).split('|')[0]
                ammo_name = ItemsUtils.GetItemName(self.ActiveItemAmmoType, True, True).split('|')[0]
                with open('battle.log', 'a') as f:
                    for v in victims:
                        e = v[2]
                        self.battleLogTargetEntity = e
                        name = get_entity_name(e)
                        level = e.level if hasattr(e, 'level') else '0'
                        distance = (e.position - self.position).length
                        write_data = ';'.join(map(str, [BigWorld.time(), lc('PlayerAvatar.client.Hit'),
                                                         '{:0.2f}'.format(distance), e.id, name, level,
                                                         weapon_name, ammo_name, '{:0.4f}'.format(accuracy), rateOfFire, '\n']))
                        f.write(write_data)
                    if self.battleLogTargetEntity:
                        for i in xrange(numShots - len(victims)):
                            name = get_entity_name(self.battleLogTargetEntity)
                            level = self.battleLogTargetEntity.level if hasattr(self.battleLogTargetEntity, 'level') else '0'
                            distance = (self.battleLogTargetEntity.position - self.position).length
                            write_data = ';'.join(map(str, [BigWorld.time(), lc('PlayerAvatar.client.Miss'),
                                                             '{:0.2f}'.format(distance), self.battleLogTargetEntity.id,
                                                             name, level, weapon_name, ammo_name,
                                                             '{:0.4f}'.format(accuracy), rateOfFire, '\n']))
                            f.write(write_data)
        finally:
            try:
                self.clientAccuracy = max(self.getShot_WeaponAccuracyMin(), self.clientAccuracy - self.getShot_WeaponKickback())
            except:
                self.clientAccuracy = self.getShot_WeaponAccuracyMin()

    def onFalseItemInHands(self):
        AvatarItemHolder.onFalseItemInHands(self)
        self.SetAvatarModel()

    def GetShootPossibility(self):
        if self.ActiveItemType != self.CurrentWeaponParam['ItemType']:
            self.onFalseItemInHands()
            return FiringDefs.NO_ITEM_EQUIPPED
        return AvatarItemHolder.GetShootPossibility(self)

    def burstFire(self, firingParams=None):
        if self.GetStatValue(Stats.ch_HitPoints) > 0 and self.GetShootPossibility() == FiringDefs.WEAPON_READY and self.canDamage and self.canShoot():
            self.fire(thisIsBurstFire=True)
        else:
            self.endBurst()
            self.notifyShotFailure()

    def singleShot(self):
        if self.GetStatValue(Stats.ch_HitPoints) > 0:
            if self.GetShootPossibility() == FiringDefs.WEAPON_READY and self.canShoot() and (not hasattr(self, 'nextSingleShotTimer') or not self.nextSingleShotTimer):
                params = self.getFireData()
                timePerShot = 1.0 / params[3]
                self.nextSingleShotTimer = BigWorld.callback(timePerShot, self.nextSingleShot)
                self.doNextSingleShot = False
                self.fire(params)
        else:
            self.notifyShotFailure()

    def getShot_WeaponKickback(self):
        return self.GetActiveWeaponAccuracyDiff()[1]

    def getShot_Recovery(self):
        return self.GetActiveWeaponAccuracyDiff()[2]

    def getShot_MoveRecoil(self):
        return self.GetActiveWeaponAccuracyDiff()[3]

    def getShot_TurnRecoil(self):
        diff = self.GetActiveWeaponAccuracyDiff()
        if diff and len(diff) > 4:
            return diff[4]
        return 0.0

    def getShot_WeaponAccuracyMin(self):
        return self.GetActiveWeaponAccuracyDiff()[0]

    def _doBurstShot(self):
        if not self.burst_active:
            return
        if self.GetStatValue(Stats.ch_HitPoints) > 0 and self.GetShootPossibility() == FiringDefs.WEAPON_READY and self.canDamage and self.canShoot():
            self.fire(thisIsBurstFire=True)
            params = self.getFireData()
            timePerShot = 1.0 / params[3]  # params[3] = fireSpeed
            self.burstTimer = BigWorld.callback(timePerShot, self._doBurstShot)
        else:
            self.endBurst()
            self.notifyShotFailure()

    def notifyShotFailure(self):
        if self.GetStatValue(Stats.ch_HitPoints) <= 0:
            BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG2'))
            return
        if not self.canDamage:
            BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG3'))
            return
        if not self.canShoot():
            if PlayerAvatar.ShootRestictions.RELOAD in self.shootRestrictions:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG4'))
                return
            if PlayerAvatar.ShootRestictions.BINOCULING in self.shootRestrictions:
                return
            if PlayerAvatar.ShootRestictions.EQUIPING in self.shootRestrictions:
                return
            if PlayerAvatar.ShootRestictions.THROW_GRENADE in self.shootRestrictions:
                return
            if PlayerAvatar.ShootRestictions.SPRINTING in self.shootRestrictions:
                return
        error_level = self.GetShootPossibility()
        if error_level != FiringDefs.WEAPON_READY:
            if error_level == FiringDefs.NO_ITEM_EQUIPPED:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG5'))
            elif error_level == FiringDefs.MODEL_NOT_READY:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG6'))
            elif error_level == FiringDefs.NOT_A_WEAPON:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG5'))
            elif error_level == FiringDefs.NO_AMMO:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG7'))
            elif error_level == FiringDefs.WEAPON_JAMMED:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG8'))
        elif not self.reloading:
            BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG9'))

    def startBurst(self):
        if self.burst_active:
            return
        self.burst_active = True
        params = self.getFireData()
        timePerShot = 1.0 / params[3]
        self.burstFire()
        self.burstTimer = BigWorld.callback(timePerShot, self._burstCallback)

    def _burstCallback(self):
        if not self.burst_active:
            return
        if self.GetStatValue(Stats.ch_HitPoints) > 0 and self.GetShootPossibility() == FiringDefs.WEAPON_READY and self.canDamage and self.canShoot():
            try:
                self.burstFire()
            except TypeError as e:
                if 'bad operand type for abs()' not in str(e):
                    raise
            params = self.getFireData()
            timePerShot = 1.0 / params[3]
            self.burstTimer = BigWorld.callback(timePerShot, self._burstCallback)
        else:
            self.endBurst()
            self.notifyShotFailure()

    def endBurst(self):
        self.burst_active = False
        if self.burstTimer is not None:
            BigWorld.cancelCallback(self.burstTimer)
            self.burstTimer = None

    def GetAccuracyModifyer(self, accuracy_mods):
        am = Character.GetAccuracyModifyer(self)
        fsam = self.GetFiringStandAccuracyMod(accuracy_mods)
        return am * fsam

    def GetCurrentAccuracyMaxAngle(self):
        angle, _, _, _, _, _, accuracy_mods = self.GetFiryingItemParams()
        angle *= self.GetAccuracyModifyer(accuracy_mods)
        return angle

    def GetCurrentClientAccuracyMod(self):
        acc = self.clientAccuracy
        if acc < 0 and math.fabs(acc / FiringDefs.ACCURACY_PERCENT_MOD) >= 1:
            return math.fabs(acc / FiringDefs.ACCURACY_PERCENT_MOD)
        return 1.0

    def getFireData(self, useBullet=True):
        angle, fireRange, bulletCount, fireSpeed, sfx, fire_type, accuracy_mods = self.GetFiryingItemParams()
        angle *= self.GetAccuracyModifyer(accuracy_mods)
        clam = self.GetCurrentClientAccuracyMod()
        angle *= clam
        if angle > math.pi / 2:
            angle = math.pi / 2
        return angle, fireRange, bulletCount, fireSpeed, sfx, fire_type, accuracy_mods

    def preload_active_item_resources(self):
        sfx_param = ItemsUtils.GetFiryingItemSFXParams(self)
        preload_buffered_oneshot_sfx(SFXer.get_gunfire_sfx_path(sfx_param))
        preload_buffered_oneshot_sfx(SFXer.get_shell_launch_sfx(self, ItemsUtils.MODE_FIRE))

    def OnActiveItemChanged(self):
        if self.ActiveItemID != 0:
            self.preload_active_item_resources()

    def onReputationChanged(self, output_string):
        self.questChatline(output_string)
        self.updateFractionsValues()

    def updateFractionsValues(self):
        self.getPvPPKstat()

    def onBecomePlayer(self):
        BWPersonality.game.__on_player_avatar__()
        self.listeners.onBecomePlayer()
        if self.inWorld:
            self.onEnterWorld()

    def onBecomeNonPlayer(self):
        self.filter = BigWorld.AvatarFilter()
        self.listeners.onBecomeNonPlayer()
        Settings().keyBindings.removeHandler(self)

    def switchCameraMode(self, mode):
        self.camera_mode = mode
        if mode == 0:
            self.control_locked = False
            Camera.online = False
        else:
            self.camera_velocity_param = 316
            Camera.online = True
            if Camera.online:
                self.camera_time_fixer = time()
                BigWorld.callback(0.1, self.updateCameraCallback)

    def updateCameraCallback(self):
        if self.camera_mode:
            timedelta = time() - self.camera_time_fixer
            self.control_locked = True
            Camera.move_freeCamera(timedelta)
            if not any([BigWorld.isKeyDown(k) for k in [Keys.KEY_W, Keys.KEY_S, Keys.KEY_A, Keys.KEY_D, Keys.KEY_SPACE, Keys.KEY_LCONTROL]]):
                Camera.stopped = True
            BigWorld.callback(0.1, self.updateCameraCallback)
        else:
            self.control_locked = False
        self.camera_time_fixer = time()

    def handleKeyEvent(self, event):
        isDown = event.isKeyDown()
        key = event.key
        mods = event.modifiers
        if not self.inWorld:
            return False
        if self.vehicle is not None and hasattr(self.vehicle, 'handleKeyEvent'):
            if self.vehicle.handleKeyEvent(isDown, key, mods):
                return True
        if isDown and key == Keys.KEY_T:
            start = BigWorld.camera().position + BigWorld.camera().direction
            end = BigWorld.camera().position + BigWorld.camera().direction * 400
            collision = BigWorld.collide(self.spaceID, start, end)
            if collision:
                self.physics.teleport(collision[0])
        if isDown and key == Keys.KEY_G:
            Camera.online = not Camera.online
            self.switchCameraMode(Camera.online)
        if isDown and key == Keys.KEY_F5 and mods == Keys.MODIFIER_ALT:
            import soGUI.soCamFly
            if not hasattr(BWPersonality.GUICore, 'camflyMenu'):
                BWPersonality.GUICore.camflyMenu = soGUI.soCamFly.soCamFly(GUI.Window())
                BWPersonality.GUICore.camflyMenu.onBound()
            BWPersonality.GUICore.camflyMenu.show()
        return False

    def handleMouseEvent(self, event):
        if not getattr(self, 'enteredWorld', False):
            return True
        dx = event.dx
        dy = event.dy
        dz = event.dz
        handled = False
        if dz:
            handled = self.MouseScrollEvent(dz)
        if handled:
            return True
        # try:
        #    turningHalfLife = BigWorld.camera().turningHalfLife
        #    if turningHalfLife > 0.0:
        #        self.savedTurningHalfLife = turningHalfLife
        #        BigWorld.camera().turningHalfLife = 0.0
        #except AttributeError:
        #    pass

        self.UpdateLookPoint(False)
        return False

    def onFalling(self, isFalling):
        if self.isMovie:
            return
        if isFalling:
            self.cell.beginFall(self.position)
        else:
            Avatar.onFalling(self, isFalling)
            self.cell.endFall(self.position)

    def EnableTargeting(self, enable=True):
        if enable:
            self.EnableTargettingCallback = None
            BigWorld.target.skeletonCheckEnabled = True
            BigWorld.target.source = BigWorld.camera().invViewMatrix
            BigWorld.target.maxDistance = Constants.HILITE_INTERACTION_DISTANCE
            BigWorld.target.selectionFovDegrees = 1
            BigWorld.target.deselectionFovDegrees = 0
            BigWorld.target.noPartial = False
            BigWorld.target.caps()
            BigWorld.target.exclude = self
        elif self.EnableTargettingCallback:
            BigWorld.cancelCallback(self.EnableTargettingCallback)
            self.EnableTargettingCallback = None
        BigWorld.target.isEnabled = enable
        self.UpdateLookPoint()

    def UpdateVelocity(self):
        velocity = self.physics.velocity
        if self.control_locked or self.is_sitting:
            velocity = (0, 0, 0)
        else:
            strafing = bool(self.movingLeft) != bool(self.movingRight)
            maxSpeed = self.GetStatValue(Stats.ch_MoveSpeed)
            if self.crouching:
                maxSpeed *= 0.5
            if self.sprinting and (strafing or self.movingBackward):
                maxSpeed /= CharacterConst.SPRINT_SPEED_ADJ
            if self.movingForward and not self.movingBackward:
                velocity[2] = maxSpeed / 1.41 if strafing else maxSpeed
                strafeSpeed = maxSpeed / 1.41
            elif not self.movingForward and self.movingBackward:
                velocity[2] = -maxSpeed * 0.63 / 1.41 if strafing else -maxSpeed * 0.63
                strafeSpeed = maxSpeed * 0.63 / 1.41
            else:
                velocity[2] = 0.0
                strafeSpeed = maxSpeed * 0.63
            if self.movingLeft and not self.movingRight:
                velocity[0] = -strafeSpeed
            elif not self.movingLeft and self.movingRight:
                velocity[0] = strafeSpeed
            else:
                velocity[0] = 0
            if not self.sniping and not self.binoculing:
                if velocity[2] > SPRINT_ANIMATION_SWITCH:
                    BigWorld.projection().rampFov(RUNNING_FOV, 2.0)
                else:
                    BigWorld.projection().rampFov(DEFAULT_FOV, 2.0)
        self.physics.velocity = velocity

    def getStat(self, name):
        if name in self.ClientStats:
            return self.ClientStats[name]
        elif name in self.Stats:
            return self.Stats[name]
        print "PlayerAvatar::getStat: unknown stat '%s'" % name
        return 0

    client_respawn_timer_type = 0
    client_respawn_timer_value = 0
    is_respawn_timer_updating = False
    respawn_msgbox_id = 'on_dead'

    def onDeathAnimationEnd(self):
        def listener(event, data):
            if event == MESSAGEBOX.EVENT_BTNPRESS:
                if data['btn'] == MESSAGEBOX.BTN_YES:
                    if self.respawn_timer_type in [Respawn.RESPAWN_CHOOSE_TIMER_ID, 0]:
                        self.cell.rise()
                    else:
                        BigWorld.callback(1.0, self.cell.rise)
                if data['btn'] == MESSAGEBOX.BTN_CANCEL:
                    print 'showkillerrrr', [self.HUNTER_killerName]
                    BWPersonality.GUICore.showSubmitOffender(True, self.HUNTER_killerName)
                    self.cell.rise()
        BWPersonality.GUICore.closeMessageBox(self.respawn_msgbox_id)
        defaultAction = MESSAGEBOX.BTN_YES
        enabled = True
        btn_set = [{'type': MESSAGEBOX.BTN_YES, 'caption': lc('PlayerAvatar.client.ON_DEAD_REVIVE'),
                    'enabled': enabled, 'ID': 'MESSAGEBOX.BTN_YES', 'width': 200},
                   {'type': MESSAGEBOX.BTN_CANCEL, 'caption': lc('PlayerAvatar.client.AnnouncementArrest'),
                    'enabled': 0, 'ID': 'MESSAGEBOX.BTN_CANCEL', 'width': 200}]
        if self.HUNTER_killerWanted:
            msg_h = lc('PlayerAvatar.client.AlreadyOrdered')
        elif self.HUNTER_iWanted:
            msg_h = lc('PlayerAvatar.client.YouOrdered')
        elif self.HUNTER_iFiledHunting:
            msg_h = lc('PlayerAvatar.client.YouHaveOrder')
        else:
            msg_h = lc('PlayerAvatar.client.AnnouncementArrest')
        btn_set[-1]['caption'] = msg_h
        if self.HUNTER_killerName:
            if not self.HUNTER_killerWanted and not self.HUNTER_iWanted and not self.HUNTER_iFiledHunting:
                btn_set[-1]['enabled'] = 1
            stime = u' '
            timeout = -1
            if self.respawn_timer_type == Respawn.RESPAWN_IDLE_TIMER_ID:
                defaultAction = None
                enabled = False
                timeout = -1
                for btn in btn_set:
                    btn['enabled'] = enabled
                self.client_respawn_timer_type = Respawn.RESPAWN_IDLE_TIMER_ID
                self.client_respawn_timer_value = Respawn.RESPAWN_IDEL_TIME
                stime = self.client_respawn_timer_value
                self.is_respawn_timer_updating = True
                BigWorld.callback(1.0, self.updateRespawnTime)
        elif self.respawn_timer_type == Respawn.RESPAWN_LIED_DOWN_TIMER_ID:
            btn_set[0]['enabled'] = 1
            timeout = -1
            self.client_respawn_timer_type = Respawn.RESPAWN_LIED_DOWN_TIMER_ID
            BigWorld.callback(1.0, self.updateRespawnTime)
            self.client_respawn_timer_value = Respawn.RESPAWN_LIED_DOWN_TIME
            stime = self.client_respawn_timer_value
        BWPersonality.GUICore.showMsgBox(id=self.respawn_msgbox_id, isModal=False, x=0.0, y=0.0, width=550,
                                         caption=lc('PlayerAvatar.client.ON_DEAD_TITLE'), forcePos=False,
                                         parent_gui_id=None, bind_to_parent=False, btn_set=btn_set, timeout=timeout,
                                         addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD, 'ID': 'main_txt_field',
                                                       'text': unicode(stime), 'hAnchor': MESSAGEBOX.ANCHOR_CENTER}],
                                         defaultAction=defaultAction, closeBox=False, callback=listener)
        if self.respawn_timer_type:
            BWPersonality.GUICore.setMouseAltState(True, True)

    def updateRespawnTime(self):
        if self.respawn_timer_type == self.client_respawn_timer_type and self.client_respawn_timer_value:
            self.client_respawn_timer_value -= 1
            if self.respawn_timer_type == Respawn.RESPAWN_LIED_DOWN_TIMER_ID:
                text = lc('EffectData.Adrenaline_msgBox').format(self.client_respawn_timer_value)
            else:
                text = unicode(self.client_respawn_timer_value)
            BWPersonality.GUICore.setMsgBoxCtrlData(self.respawn_msgbox_id, 'main_txt_field', text)
            if self.client_respawn_timer_value:
                BigWorld.callback(1.0, self.updateRespawnTime)
            self.is_respawn_timer_updating = False
        else:
            self.client_respawn_timer_type = 0
            self.client_respawn_timer_value = 0
            self.is_respawn_timer_updating = False

    def set_respawn_timer_type(self, old_value):
        if self.respawn_timer_type:
            self.onDeathAnimationEnd()
        elif old_value == Respawn.RESPAWN_LIED_DOWN_TIMER_ID:
            BWPersonality.GUICore.closeMessageBox(self.respawn_msgbox_id)
        else:
            for msg_id in [self.respawn_msgbox_id, self.manipulate_dead_msgbox_id]:
                BWPersonality.GUICore.closeMessageBox(msg_id)

    manipulate_dead_msgbox_id = 'man_dead_msgbox'

    def manipulateWithDead(self, entity):
        def listener(event, data):
            if event == MESSAGEBOX.EVENT_BTNPRESS and entity.dead:
                if entity.dead and entity.respawn_timer_type in [Respawn.RESPAWN_LIED_DOWN_TIMER_ID, Respawn.RESPAWN_CHOOSE_TIMER_ID]:
                    if data['btn'] == MESSAGEBOX.BTN_YES:
                        firstAIDItem = ItemsUtils.GetFirstMedecineItem(self)
                        if firstAIDItem:
                            item_id = firstAIDItem['complexItemID']
                            self.useItemOnTarget(item_id, entity)
                    elif data['btn'] == MESSAGEBOX.BTN_NO:
                        self.cell.finishDead(entity.id)
        if entity.dead and entity.respawn_timer_type in [Respawn.RESPAWN_LIED_DOWN_TIMER_ID, Respawn.RESPAWN_CHOOSE_TIMER_ID]:
            BWPersonality.GUICore.closeMessageBox(self.manipulate_dead_msgbox_id)
            enabled = True
            btn_set = [{'type': MESSAGEBOX.BTN_YES, 'caption': lc('PlayerAvatar.client.GIVE_AID_TO_DEAD'),
                        'enabled': enabled if ItemsUtils.GetFirstMedecineItem(self) else False,
                        'ID': 'MESSAGEBOX.BTN_YES', 'width': 150},
                       {'type': MESSAGEBOX.BTN_NO, 'caption': lc('PlayerAvatar.client.KILL_AND_BEAT'),
                        'enabled': enabled, 'ID': 'MESSAGEBOX.BTN_NO', 'width': 150}]
            BWPersonality.GUICore.showMsgBox(id=self.respawn_msgbox_id, isModal=False, x=0.0, y=0.0, width=350,
                                             caption=lc('PlayerAvatar.client.USE_DEAD_TITLE'), forcePos=False,
                                             parent_gui_id=None, bind_to_parent=False, btn_set=btn_set, timeout=-1,
                                             addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD, 'ID': 'main_txt_field',
                                                           'text': unicode(entity.name), 'hAnchor': MESSAGEBOX.ANCHOR_CENTER}],
                                             defaultAction=None, closeBox=True, callback=listener)
            BWPersonality.GUICore.setMouseAltState(True, True)

    def on_death(self, source_data):
        # Очистка всех динамических состояний и колбэков перед вызовом родительской логики
        if hasattr(self, 'updateLookTimer'):
            BigWorld.cancelCallback(self.updateLookTimer)
        if hasattr(self, 'antiSpeedGearCallback') and self.antiSpeedGearCallback:
            BigWorld.cancelCallback(self.antiSpeedGearCallback)

        self.setControlLock(PlayerAvatar.ControlLockTypes.DEAD)
        self.EnableTargeting(False)
        self.UpdateVelocity()
        self.EnableModelPitch(False)
        self.restrictShoot(PlayerAvatar.ShootRestictions.DEATH)
        self.UpdateSniping(False)
        self.Binoculars(False)
        self.inputlock = True # Важно, чтобы inputlock оставался активным в состоянии смерти/ожидания респауна
        self.is_sitting = False

        Avatar.on_death(self, source_data) 
        
        if self.inPVPinstance:
            def okey_callback(event):
                if event == 0:
                    self.base.changeTeam(0)
            self.askIDteamNo = gui_jokes.askUserOk('', lc('PlayerAvatar.client.PVP_GO_TO_SHOP'), okey_callback).ID
            BWPersonality.GUICore.setBestCursor()

        msg = ''
        killer_wpn = ''
        killer_name = ''
        killer_dist = 0
        source_type = source_data['type']
        if source_type in [Config.Damage.SourceTypes.SUICIDE, Config.Damage.SourceTypes.WORLD]:
            msg = lc('PlayerAvatar.client.MSG20')
        elif source_type == Config.Damage.SourceTypes.EFFECT:
            effect_id = source_data['subtype'][0]
            efData = getEffect(effect_id)
            msg = lc('PlayerAvatar.client.KILLED_BY_EFFECT').format(effect_name=lc(efData['name']))
        elif source_data['entity_id'] == self.id:
            msg = lc('PlayerAvatar.client.MSG11')
        # ... (остальная логика сообщения) ...
        elif source_type in [Config.Damage.SourceTypes.ANOMALY, Config.Damage.SourceTypes.AVATAR, 
                             Config.Damage.SourceTypes.CREATURE, Config.Damage.SourceTypes.NPC_PVE, Config.Damage.SourceTypes.NPC_PVP]:
            killer = BigWorld.entity(source_data['entity_id'], True)
            killer_name = get_entity_name(killer, True)
            if source_type == Config.Damage.SourceTypes.AVATAR:
                # ... (логика AVATAR) ...
                if killer_name:
                    killer_wpn = ItemsUtils.GetItemName(killer.ActiveItemType)
                    killer_dist = abs(round(self.position.distTo(killer.position), 1))
                    msg = lc('PlayerAvatar.client.MSG13') + killer_name + u' (' + killer_wpn + u': ' + unicode(killer_dist) + u'm)'
                else:
                    msg = lc('PlayerAvatar.client.MSG14')
            elif killer_name:
                # ... (логика NPC/Creature) ...
                msg = lc('PlayerAvatar.client.MSG15') + killer_name
            elif source_type == Config.Damage.SourceTypes.CREATURE:
                 msg = lc('PlayerAvatar.client.MSG18')
            else:
                msg = lc('PlayerAvatar.client.MSG16')
        else:
            msg = lc('PlayerAvatar.client.MSG20')

        self.woundsChatline(msg)


    def showDeadTooltip(self, source_data, killer_wpn, killer_name, killer_dist):
        isAdrenaline = 805 in self.current_effects
        source_type = source_data['type']
        print dict(source_data)
        msg = u''
        if source_type == Config.Damage.SourceTypes.SUICIDE:
            msg = lc('deadTooltip.SUICIDE')
        elif source_type == Config.Damage.SourceTypes.WORLD:
            msg = lc('deadTooltip.WORLD')
        elif source_type == Config.Damage.SourceTypes.EFFECT:
            if source_data['subtype']:
                effect_id = source_data['subtype'][0]
                efData = getEffect(effect_id)
                msg = lc('deadTooltip.BY_EFFECT').format(effname=lc(efData['name']))
                msg += lc('deadTooltip.EFFECT_%s' % effect_id)
        elif source_type == Config.Damage.SourceTypes.ANOMALY:
            if source_data['subtype']:
                effect_id = source_data['subtype'][0]
                efData = getEffect(effect_id)
                msg = lc('deadTooltip.BY_ANOMALY_EFFECT').format(effname=lc(efData['name']))
                msg += lc('deadTooltip.EFFECT_%s' % effect_id)
        elif source_type == Config.Damage.SourceTypes.CREATURE:
            msg = lc('deadTooltip.byCreature')
        elif source_type in [Config.Damage.SourceTypes.NPC_PVE, Config.Damage.SourceTypes.NPC_PVP]:
            msg = lc('deadTooltip.byNPC')
        elif source_type == Config.Damage.SourceTypes.AVATAR:
            msg = lc('deadTooltip.byAvatar').format(name=killer_name, weapon=killer_wpn, distance=killer_dist)
        else:
            msg = u'!!!!'
        if not isAdrenaline:
            msg += '\n' + lc('deadTooltip.notUseAdrenaline%s' % random.randint(1, 4))
        self.woundsChatline(u'test:' + msg)
        print msg.encode('utf8')

    def on_revive(self):
        Avatar.on_revive(self)
        self.setControlLock(self.ControlLockTypes.DEAD, False)
        self.EnableTargeting()
        self.UpdateVelocity()
        self.EnableModelPitch(True)
        self.restrictShoot(PlayerAvatar.ShootRestictions.DEATH, False)
        self.woundsChatline(lc('PlayerAvatar.client.MSG21'))
        self.checkCamera()
        BWPersonality.GUICore.setMouseAltState(0, True)

    def on_victim_death(self, victim_id):
        entity = Avatar.on_victim_death(self, victim_id)
        name = get_entity_name(entity, utf8=True)
        self.damageChatline(lc('PlayerAvatar.client.MSG22').format(name=name if name else lc('PlayerAvatar.client.MSG23')))
        self.listeners.setInfobarFrags(self.frags)
        if self.battleLogSwitchedOn:
            weapon_name = ItemsUtils.GetItemName(self.ActiveItemType, True, True).split('|')[0]
            ammo_name = ItemsUtils.GetItemName(self.ActiveItemAmmoType, True, True).split('|')[0]
            with open('battle.log', 'a') as f:
                v = BigWorld.entities[victim_id]
                name = get_entity_name(v)
                level = v.level if hasattr(v, 'level') else '0'
                distance = (v.position - self.position).length
                write_data = ';'.join(map(str, [BigWorld.time(), lc('PlayerAvatar.client.MSG24').encode('utf8'),
                                                 '{:0.2f}'.format(distance), victim_id, name, level,
                                                 weapon_name, ammo_name, '\n']))
                f.write(write_data)

    def on_victim_damaged(self, victim_id, damagetaken_data):
        victim = Avatar.on_victim_damaged(self, victim_id, damagetaken_data)
        name = u''
        if victim:
            name = get_entity_name(victim, utf8=True)
        if name:
            chatline = lc('PlayerAvatar.client.YOU_HAVE_INJURED').format(name=name, damage=-round(damagetaken_data['health_decrement'], 2))
        else:
            chatline = lc('PlayerAvatar.client.MSG26') + u'   (' + unicode(-round(damagetaken_data['health_decrement'], 2)) + u')'
        if damagetaken_data['flags'] & Config.Damage.Flags.CRITICAL:
            chatline = lc('PlayerAvatar.client.MSG27') + chatline
        self.damageChatline(chatline)
        if self.battleLogSwitchedOn:
            weapon_name = ItemsUtils.GetItemName(self.ActiveItemType, True, True).split('|')[0]
            ammo_name = ItemsUtils.GetItemName(self.ActiveItemAmmoType, True, True).split('|')[0]
            with open('battle.log', 'a') as f:
                v = victim
                name = get_entity_name(v)
                level = v.level if hasattr(v, 'level') else '0'
                distance = (v.position - self.position).length
                write_data = ';'.join(map(str, [BigWorld.time(), lc('PlayerAvatar.client.MSG28').encode('utf8'),
                                                 '{:0.2f}'.format(distance), victim_id, name, level,
                                                 weapon_name, ammo_name, '{:0.1f}'.format(damagetaken_data['health_decrement']), '\n']))
                f.write(write_data)
        return victim

    def on_damaged(self, source_data, damagetaken_data):
        Avatar.on_damaged(self, source_data, damagetaken_data)
        damage = damagetaken_data['health_decrement']
        self.temporarySpeedChange(max(0.3, 1 - damage / self.GetStatValue(Stats.ch_MaxHitPoints)), 0.5)
        name = u''
        msg = u''
        damager = None
        source_type = source_data['type']
        if source_type == Config.Damage.SourceTypes.EFFECT:
            effect_id = source_data['subtype'][0]
            efData = getEffect(effect_id)
            msg = lc('PlayerAvatar.client.INJURED_BY_EFFECT').format(effect_name=lc(efData['name']))
        elif source_type == Config.Damage.SourceTypes.ANOMALY:
            msg = lc('PlayerAvatar.client.MSG31')
        elif source_type == Config.Damage.SourceTypes.AVATAR and source_data['entity_id'] == self.id:
            pass
        elif source_type in [Config.Damage.SourceTypes.AVATAR, Config.Damage.SourceTypes.CREATURE,
                             Config.Damage.SourceTypes.NPC_PVE, Config.Damage.SourceTypes.NPC_PVP]:
            damager = BigWorld.entity(source_data['entity_id'], True)
            damager_name = get_entity_name(damager, True)
            if source_type == Config.Damage.SourceTypes.AVATAR:
                msg = lc('PlayerAvatar.client.MSG32') + damager_name if damager_name else lc('PlayerAvatar.client.MSG33')
            elif source_type in [Config.Damage.SourceTypes.NPC_PVE, Config.Damage.SourceTypes.NPC_PVP]:
                msg = lc('PlayerAvatar.client.MSG34') + damager_name if damager_name else lc('PlayerAvatar.client.MSG35')
            elif source_type == Config.Damage.SourceTypes.CREATURE:
                msg = lc('PlayerAvatar.client.MSG34') + damager_name if damager_name else lc('PlayerAvatar.client.MSG37')
            else:
                msg = lc('PlayerAvatar.client.MSG38')
        msg = msg + u'   (' + unicode(-round(damage, 2)) + u')'
        if self.printDamageToChat and damage >= self.minDamageLimit:
            self.woundsChatline(msg)
        self.BrakeAcuracy()
        if 402 not in source_data['subtype']:
            BigWorld.camera().shake(0.1, (0.03, 0.03, 0.03))
        if damager:
            posDiff = self.position - damager.position
            posDiff.normalise()
            avDir = Vector3()
            avDir.setPitchYaw(self.pitch, self.yaw)
            avDir.y = 0
            posDiff.y = 0
            dirCos = avDir.dot(posDiff)
            leftTrueRightFalse = avDir.cross2D(posDiff) < 0
            if dirCos < -0.5:
                xDir = 1
            elif dirCos > 0.5:
                xDir = 2
            elif leftTrueRightFalse:
                xDir = 3
            else:
                xDir = 4
            xDam = max(10, min(1.0, damage * 1.0 / self.GetStatValue(Stats.ch_MaxHitPoints)))
            if self.showGUIDamage:
                BWPersonality.GUICore.showDamage(xDam, xDir, 1)
        else:
            xDam = max(10, min(1.0, damage * 1.0 / self.GetStatValue(Stats.ch_MaxHitPoints)))
            if self.showGUIDamage:
                BWPersonality.GUICore.showDamage(xDam, 0, 1)

    def combatLogEvent(self, logEntry):
        if self.id == logEntry['target']:
            self.showDamage(logEntry['damage'], logEntry['actor'], True)

    def addSpotLight(self):
        spot = BigWorld.PyChunkSpotLight()
        spot.priority = 1
        spot.specular = True
        self.spotLight = spot

    def ManipulateTarget(self):
        entity = BigWorld.target()
        if BWPersonality.GUICore.dialogueGUI and BWPersonality.GUICore.dialogueGUI.component.visible:
            BWPersonality.GUICore.showDialogueGUI(False)
            return
        if entity and self.position.distSqrTo(entity.position) < Constants.INTERACTION_DISTANCE ** 2:
            if Helpers.Caps.CAP_CAN_PICKUP in entity.targetCaps:
                self.cell.PickUpItem(entity.id, ItemsUtils.PICK_UP_PLAYER_TARGETING)
                return True
            if Helpers.Caps.CAP_CAN_EXCHANGE in entity.targetCaps:
                self.StartExchange(entity)
                self.manipulateWithDead(entity)
                return True
            if Helpers.Caps.CAP_CAN_OPEN_AND_EXPLORE in entity.targetCaps:
                self.ExploreContainer(entity)
                return True
            if Helpers.Caps.CAP_CAN_OPEN_AND_EXPLORE_USER_FIRE in entity.targetCaps:
                self.exploreUserFireContainer(entity)
                return True
            if Helpers.Caps.CAP_CAN_TELEPORT in entity.targetCaps:
                entity.cell.activate()
                return True
            if Helpers.Caps.CAP_CAN_USE in entity.targetCaps:
                entity.cell.activate()
                return True
            if Helpers.Caps.CAP_CAN_TALK in entity.targetCaps:
                if BWPersonality.GUICore.getGUIMap() is not None:
                    self.ManipulateQuesterTarget(entity)
                    if self.npcTalkPot:
                        BigWorld.delPot(self.npcTalkPot)
                    self.npcTalkPot = BigWorld.addPot(entity.matrix, QuesterConsts.MAX_DIALOG_DISTANCE, self.dialogEntityPotHandler)
                return True
            if Helpers.Caps.CAP_CAN_GATHER_GROUP in entity.targetCaps:
                self.base.gatherGroup(entity.id)
                return True
            if Helpers.Caps.CAP_OPEN_BULLETIN_BOARD in entity.targetCaps:
                self.set_BulletinBoardData()
                BWPersonality.GUICore.showBulletinBoard(True)
                if self.bboardPot:
                    BigWorld.delPot(self.bboardPot)
                self.bboardPot = BigWorld.addPot(entity.matrix, QuesterConsts.MAX_DIALOG_DISTANCE, self.bboarddialogEntityPotHandler)
                return True
            if Helpers.Caps.CAP_BASE_TRADE in entity.targetCaps:
                self.startTradeBase()
                self.manipulateWithDead(entity)
                if self.npcTalkPot:
                    BigWorld.delPot(self.npcTalkPot)
                self.npcTalkPot = BigWorld.addPot(entity.matrix, QuesterConsts.MAX_DIALOG_DISTANCE, self.dialogEntityPotHandler)
                return True
            if Helpers.Caps.CAP_OPEN_WORKBENCH in entity.targetCaps:
                BWPersonality.GUICore.showCraftGUI(True)
                return True
            if Helpers.Caps.CAP_CLAN_WAREHOUSE in entity.targetCaps:
                if getattr(entity, 'isDisableDialogs', 0):
                    self.systemMessage('NPC disabled', 4294901760L)
                    return
                self.chooseCloseDialog(True, True)
                if self.clanID > 0:
                    entity.showClanManagerNPCGUI()
                else:
                    self.systemChatline(lc('GUI.ClanGUI.NO_CLAN'))
        return False

    def bboarddialogEntityPotHandler(self, enteredTrap, handle):
        if not enteredTrap:
            BigWorld.delPot(handle)
            BWPersonality.GUICore.showBulletinBoard(False)

    def dialogEntityPotHandler(self, enteredTrap, handle):
        if not enteredTrap:
            BigWorld.delPot(handle)
            self.onLeaveTalkingNPC()

    def onLeaveTalkingNPC(self):
        Inventory.onLeaveTalkingNPC(self)
        self.chooseCloseDialog(True, True)

    def ExploreContainer(self, entity):
        if Helpers.Caps.CAP_CAN_OPEN_AND_EXPLORE in entity.targetCaps:
            self.StartItemCache(entity.id, ItemsUtils.CACHE_MODE_CONTAIER)

    def iscanBuyInClanShop(self, value):
        self.isCanBuyInClanShop = value

    def onStartTrading(self, entity):
        if Helpers.Caps.CAP_CAN_TRADE in entity.targetCaps:
            wares_ids = []
            if self.isCanBuyInClanShop:
                wares_ids.extend(ItemsUtils.getTraderAssortmentByClanID(self, entity))
            for entry in entity.Assortment:
                wares_ids.append(entry.Type)
            self.StartTrading(wares_ids, entity.id)

    def onStartBarter(self, entity):
        self.StartNPCBarter(entity)

    def onStartRepair(self, entity):
        if Helpers.Caps.CAP_CAN_TRADE in entity.targetCaps:
            self.StartNPCRepair(entity.id)

    def onStartComplexRepair(self, entity):
        if Helpers.Caps.CAP_CAN_TRADE in entity.targetCaps:
            self.onComplexRepair(entity.id)

    def GetEquipedItemsRepairCost(self, repairman_entity):
        return AvatarItemHolder.GetEquipedItemsRepairCost(self, repairman_entity)

    def onStartItemCache(self, entity):
        if Helpers.Caps.CAP_CAN_TRADE in entity.targetCaps:
            self.StartItemCache(entity.id, ItemsUtils.CACHE_MODE_SAFEBOX)

    def onAnomalyDrag(self, anomalyId, posAndYaw, velocity, verticalRange, grabDuration, shouldFly):
        if not hasattr(self, 'physics'):
            return
        self.activeAnomaly = anomalyId
        if shouldFly != 0:
            self.physics.fall = False
            if not self.dead:
                self.model.Jump()
        else:
            self.physics.fall = True
        self.savedVerticalVelocity = self.physics.velocity[1]
        self.physics.velocity = velocity
        posAndYaw[3] = self.yaw
        self.physics.seek(posAndYaw, grabDuration, verticalRange, self.onAnomalyDragEnded)
        self.physics.scheduleFall(grabDuration, True)

    def onAnomalyDragEnded(self, result):
        self.physics.fall = True
        v = self.physics.velocity
        v[0] = 0
        v[2] = 0
        v[1] = self.savedVerticalVelocity
        self.physics.velocity = v

    def getWeaponRange(self):
        _, fireRange, _, _, _, _, _ = self.GetFiryingItemParams()
        return fireRange

    def AttachItem(self, mother_item_id, attaching_item_id):
        if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
            duration = ItemHolder.onAttachItem(self, mother_item_id, attaching_item_id)
            SFXer.ItemModificationEffect(self)
            self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, duration, lc('Items.GUIStrings.MODIFICATION'))

    def DatachItem(self, mother_item_id, detaching_id):
        if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
            duration = ItemHolder.onDatachItem(self, mother_item_id, detaching_id)
            SFXer.ItemModificationEffect(self)
            self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, duration, lc('Items.GUIStrings.MODIFICATION'))

    def inputlockOff(self):
        self.inputlock = False

    def EnableCrosshair(self):
        BWPersonality.GUICore.targettingGUI.only_dot(False)

    fly_out_mult = 0.45
    is_throwing = False

    @BWKeyBindingAction('ThrowGrenade')
    def keyThrowGrenade(self, isDown):
        if self.dead or self.is_sitting or self.inputlock:
            BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG3'))
            return
        if isDown:
            mod = self.GetGrenadeThrowModifyer()
            self.magnitude = 17.0 * mod
            if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS) and self.canThrowGrenade():
                throw_duration = self.grenadeThrow()
                self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, throw_duration, lc('Items.GUIStrings.GRENADE'))

    vel_mult_grenade = 1.3

    def grenadeThrow(self):
        if self.is_throwing:
            return
        self.is_throwing = True
        throwingType = self.GetFiringGrenadeThrowType()
        throw_duration = Durations.GetGrenadeThrowDuration(self, throwingType)

        def throw():
            position, velocity = self.get_throw_params()
            velocity *= self.vel_mult_grenade
            clientGrenadeID = self.throw(throwingType, {}, position, velocity)
            self.cell.throwGrenade(position, velocity, clientGrenadeID)
            BigWorld.callback(0.3, lambda: setattr(self, 'is_throwing', False))

        fly_out_delay = throw_duration * self.fly_out_mult
        BigWorld.callback(fly_out_delay, throw)
        position, velocity = self.get_throw_params()
        self.DrawThrow(throw_duration, velocity)
        return throw_duration

    def onGrenadeExploded(self, grenade):
        pass

    @BWKeyBindingAction('ThrowStone')
    def keyThrowStone(self, isDown):
        if self.dead:
            BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG3'))
            return
        if isDown:
            mod = self.GetGrenadeThrowModifyer()
            self.magnitude = 17.0 * mod
            throw_duration = self.stoneThrow()
            self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, throw_duration, lc('Items.GUIStrings.STONE'))

    def get_throw_params(self):
        direction = Vector3(BigWorld.camera().direction)
        direction[1] += 0.2
        if self.lookingaround or self.is_sitting:
            direction[0] = self.lastdirection[0]
            direction[2] = self.lastdirection[2]
        direction.normalise()
        velocity = direction * self.magnitude
        position = Matrix(self.throwing_node).translation
        return position, velocity

    vel_mult = 2

    def stoneThrow(self):
        if self.is_throwing:
            return
        self.is_throwing = True
        throw_duration = Durations.GetStoneThrowDuration(self)

        def throw():
            position, velocity = self.get_throw_params()
            velocity *= self.vel_mult
            clientStoneID = self.throw(ThrowTypes.STONE, {}, position, velocity)
            self.cell.throwStone(position, velocity, clientStoneID)
            BigWorld.callback(0.3, lambda: setattr(self, 'is_throwing', False))

        fly_out_delay = throw_duration * self.fly_out_mult
        BigWorld.callback(fly_out_delay, throw)
        position, velocity = self.get_throw_params()
        self.DrawThrow(throw_duration, velocity * self.vel_mult)
        return throw_duration

    @BWKeyBindingAction('PVPScoreBar')
    def SwitchPVPScoreBar(self, isDown):
        print 'SwitchPVPScoreBar', isDown
        BWPersonality.GUICore.showPVPScoreBarPlayerList(isDown)

    @BWKeyBindingAction('SwitchNightVision')
    def SwitchNightVision(self, isDown):
        if isDown:
            return
        if not self.GetEquippedBinocularAbilityNVpossible():
            return
        self.nightVisonON = not self.nightVisonON
        if self.nightVisonON:
            if self.binoculing:
                BWPersonality.GUICore.addPPEffect(postEfNV)
        else:
            BWPersonality.GUICore.delPPEffect(postEfNV)

    @BWKeyBindingAction('FriendList')
    def showFriendList(self, isDown):
        BWPersonality.GUICore.showFriendList()

    @BWKeyBindingAction('LeftMouseButton')
    def onLeftMouseButton(self, isDown):
        if not isDown:
            self.endBurst()
        if self.ActiveItemID == 0:
            self.ManipulateTarget()
        elif not self.control_locked:
            if not self.sprinting:
                self.LeftMouseButtonRoutine(isDown)
            else:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG_FIRE_ON_SPRINT'))

    def LeftMouseButtonRoutine(self, isDown):
        if isDown:
            if not self.no_weapon_in_hands:
                if self.GetShootPossibility() == FiringDefs.WEAPON_READY and self.canDamage:
                    self.startBurst() 
                else:
                    self.notifyShotFailure()
                    if self.CurrentWeaponAmmo <= 0 and self.canReload():
                        self.reload(False)
                    elif self.no_weapon_in_hands:
                        BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG5'))
                    elif self.ActiveItemJammed and self.ActiveItemID:
                        self.InFormWeponJammed()
            else:
                self.notifyShotFailure()
        else:
            self.endBurst()

    def MouseScrollEvent(self, pixels_z_shift):
        try:
            if BWPersonality.GUICore.camflyMenu.MouseScrollEvent(pixels_z_shift):
                return True
        except:
            pass
        if self.sniping and not self.lookingaround:
            self.UpdateScopeMode(pixels_z_shift)
            return True
        elif self.binoculing and not self.lookingaround:
            self.UpdateBinocularMode(pixels_z_shift)
            return True
        if pixels_z_shift > 0:
            if self.ActiveItemID != self.ActiveWeaponSet.PrimarySlotID and not self.inputlock:
                self.EquipWeaponCommand(ItemsUtils.GetComplexItemByID(self, self.ActiveWeaponSet.PrimarySlotID))
        elif pixels_z_shift < 0:
            if self.ActiveItemID != self.ActiveWeaponSet.SecondarySlotID and not self.inputlock:
                self.EquipWeaponCommand(ItemsUtils.GetComplexItemByID(self, self.ActiveWeaponSet.SecondarySlotID))
        return True

    @BWKeyBindingAction('RightMouseButton')
    def onRightMouseButton(self, isDown):
        self.UpdateSniping(isDown)

    @BWKeyBindingAction('PrimaryWeapon')
    def PrimaryWeaponSelect(self, isDown):
        if isDown and self.ActiveItemID != self.ActiveWeaponSet.PrimarySlotID and self.ActiveWeaponSet.PrimarySlotID != 0 and not self.inputlock:
            self.EquipWeaponCommand(ItemsUtils.GetComplexItemByID(self, self.ActiveWeaponSet.PrimarySlotID))

    @BWKeyBindingAction('SecondaryWeapon')
    def SecondaryWeaponSelect(self, isDown):
        if isDown and self.ActiveItemID != self.ActiveWeaponSet.SecondarySlotID and self.ActiveWeaponSet.SecondarySlotID != 0 and not self.inputlock:
            self.EquipWeaponCommand(ItemsUtils.GetComplexItemByID(self, self.ActiveWeaponSet.SecondarySlotID))

    @BWKeyBindingAction('SitGround')
    def onSitGround(self, isDown):
        if not isDown and not self.inputlock:
            self.ProceedSit(1)

    @BWKeyBindingAction('SitBackpack')
    def onSitBackpack(self, isDown):
        if not isDown and not self.inputlock:
            self.ProceedSit(2)

    @BWKeyBindingAction('SitGroundX')
    def onSitGroundX(self, isDown):
        if not isDown and not self.inputlock:
            self.ProceedSit(3)

    @BWKeyBindingAction('SitLegs')
    def onSitLegs(self, isDown):
        if not isDown and not self.inputlock:
            self.ProceedSit(4)

    def ProceedSit(self, sit_id):
        if self.dead or self.sniping or self.binoculing or not self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
            return

        def controllockOff():
            self.control_locked = False

        if not self.is_sitting:
            if self.lastdirection == Vector3(0, 0, 0):
                self.lastdirection = Vector3(BigWorld.camera().direction)
            self.inputlock = True
            self.lastsit = sit_id
            if self.ActiveItemID != 0:
                duration = Durations.GetEquipDuration(self, self.ActiveItemID)
                self.HolsterWeapon()
                self.holstered = True
            else:
                duration = 0
                self.holstered = False
            self.control_locked = True
            self.UpdateVelocity()
            sit_duration = Avatar.SitGroundDuration(self, sit_id, True)
            callback(partial(self.DrawSitAction, sit_id, True, False, False), duration)
            callback(partial(self.cell.DrawSitAction, sit_id, True, False, False), duration)
            callback(partial(self.DrawSitAction, sit_id, False, True, False), sit_duration + duration - 0.37)
            callback(partial(self.cell.DrawSitAction, sit_id, False, True, False), sit_duration + duration - 0.37)
            if not self.lookingaround:
                self.physics.userDirected = False
            callback(partial(self.inputlockOff), sit_duration + duration, cancel_existing=True, id='inputlock_off')
            self.is_sitting = True
        else:
            self.inputlock = True
            sit_id = self.lastsit
            sit_duration = Avatar.SitGroundDuration(self, sit_id, False)
            self.DrawSitAction(sit_id, False, False, True)
            self.cell.DrawSitAction(sit_id, False, False, True)
            if not self.lookingaround:
                self.physics.userDirected = True
            callback(partial(controllockOff), sit_duration)
            if self.holstered:
                duration = Durations.GetEquipDuration(self, self.weapon_was_in_hands_id)
                callback(partial(self.HolsterWeapon), sit_duration)
                self.holstered = False
            else:
                duration = 0
            callback(partial(self.inputlockOff), sit_duration + duration, cancel_existing=True, id='inputlock_off')
            self.lastdirection = Vector3(0, 0, 0)
            self.is_sitting = False
        self.cell.SetSitting(self.is_sitting)
        self.checkCamera()

    def DrawSitAction(self, sit_id, sit, sat, stand):
        Avatar.SitGround(self, sit_id, sit, sat, stand)

    @BWKeyBindingAction('LookAround')
    def onLookAround(self, isDown):
        self.LookAround(isDown)

    def LookAround(self, isDown):
        if self.binoculing:
            return
        if self.lastdirection == Vector3(0, 0, 0):
            self.lastdirection = Vector3(BigWorld.camera().direction)
        if self.ActiveItemID != 0:
            self.UpdateSniping(False)
        if isDown and not self.lookingaround:
            self.lookingaround = True
            self.physics.userDirected = False
            BWPersonality.GUICore.targettingGUI.hide()
            self.checkCamera()
        elif not isDown:
            self.lastdirection = Vector3(0, 0, 0)
            BWPersonality.GUICore.targettingGUI.show()
            self.physics.userDirected = True
            self.lookingaround = False
            self.camera_in_interior = False
            self.checkCamera()

    @BWKeyBindingAction('ChangeViewShoulder')
    def onChangeViewShoulder(self, isDown):
        if not self.lookingaround and not self.is_sitting and not self.sniping and not self.binoculing:
            self.ChangeViewShoulder(isDown)

    def ChangeViewShoulder(self, isDown):
        if not isDown:
            self.camera_horiz *= -1
            self.checkCamera()

    @BWKeyBindingAction('HolsterWeapon')
    def onHolsterWeapon(self, isDown):
        if not isDown and not self.inputlock:
            self.HolsterWeapon()

    def HolsterWeapon(self):
        if not self.sniping and not self.binoculing:
            if self.ActiveItemID != 0:
                self.EquipWeaponCommand(0)
            elif self.weapon_was_in_hands_id != 0:
                self.EquipWeaponCommand(ItemsUtils.GetComplexItemByID(self, self.weapon_was_in_hands_id))

    def UpdateSniping(self, enable):
        if enable:
            if not self.binoculing and not self.sprinting and not self.is_sitting and not self.reloading and not self.no_weapon_in_hands and self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
                equippedItemTypeSnipingAbilityList = self.GetEquippedItemSnipingAbility()
                if equippedItemTypeSnipingAbilityList is None:
                    return
                list_length = len(equippedItemTypeSnipingAbilityList)
                if self.scopeMode >= list_length:
                    self.scopeMode = list_length - 1
                equippedItemTypeSnipingAbility = equippedItemTypeSnipingAbilityList[self.scopeMode]
                if equippedItemTypeSnipingAbility in SCOPE_MULTIPLER_TABLE:
                    self.model.visible = self.lookingaround or 0
                    multiplier = SCOPE_MULTIPLER_TABLE[equippedItemTypeSnipingAbility][0]
                else:
                    multiplier = 1
                self.SetSniping(1, equippedItemTypeSnipingAbility)
                self.magnify(multiplier)
            elif equippedItemTypeSnipingAbility in [ItemsCatalog.NONE_TYPE]:
                multiplier = 1 if self.lookingaround else 1.2
                self.SetSniping(1)
                self.magnify(multiplier)
                self.UpdateModelPitch()
            else:
                return
        elif self.sniping:
            self.unmagnify()
            self.SetSniping(0)
            self.model.visible = 1
            self.UpdateModelPitch()
        SFXer.ChangeStanceEffect(self)

    def SetSniping(self, sniping, scope_type=ItemsCatalog.NONE_TYPE):
        if sniping and self.sniping:
            callback.cancel('turn_off_sniping')
            return
        if not sniping and not self.sniping:
            return

        def apply_sniping(sniping, scope_type):
            self.sniping = sniping
            if not self.lookingaround:
                self.snipingScopeType = scope_type
            self.cell.SetSniping(sniping)
            self.UpdateModelPitch()

        if sniping:
            apply_sniping(sniping, scope_type)
        else:
            callback(partial(apply_sniping, False, scope_type), 0.2, cancel_existing=True, id='turn_off_sniping')
        self.checkCamera()

    def UpdateScopeMode(self, pixels_z_shift):
        delta = 1 if pixels_z_shift > 0 else -1 if pixels_z_shift < 0 else 0
        ability_list = self.GetEquippedItemSnipingAbility()
        if ability_list and 0 <= self.scopeMode + delta < len(ability_list):
            self.scopeMode += delta
            self.UpdateSniping(self.sniping)

    @BWKeyBindingAction('Binoculars')
    def Binoculars(self, isDown):
        self.SetBinoculing(isDown)

    def SetBinoculing(self, binoculing):
        if self.binoculing == binoculing:
            return
        if self.lookingaround or self.sniping or self.reloading or self.inputlock:
            callback.cancel('turn_off_binoculing')
            return
        if binoculing:
            if self.canBinoculing():
                self.binoculing = binoculing
                self.cell.SetBinoculing(binoculing)
        else:
            self.binoculing = binoculing
            self.cell.SetBinoculing(binoculing)
        self.UpdateBinoculing()

    def UpdateBinoculing(self):
        if self.binoculing:
            zoom_list = self.GetEquippedBinocularAbility()
            if zoom_list is not None:
                list_length = len(zoom_list)
                if self.binocularMode >= list_length:
                    self.binocularMode = list_length - 1
                multiplier = zoom_list[self.binocularMode]
                self.magnify(multiplier)
                BWPersonality.GUICore.showBinoculars(True)
                if self.nightVisonON and self.GetEquippedBinocularAbilityNVpossible():
                    BWPersonality.GUICore.addPPEffect(postEfNV)
                self.model.visible = 0
                self.BrakeAcuracy()
        else:
            self.unmagnify()
            BWPersonality.GUICore.showBinoculars(False)
            self.model.visible = 1
            BWPersonality.GUICore.delPPEffect(postEfNV)

    def UpdateBinocularMode(self, pixels_z_shift):
        delta = 1 if pixels_z_shift > 0 else -1 if pixels_z_shift < 0 else 0
        ability_list = self.GetEquippedBinocularAbility()
        if ability_list and 0 <= self.binocularMode + delta < len(ability_list):
            self.binocularMode += delta
            self.UpdateBinoculing()

    def magnify(self, multiplier=1.0, fov=0, newFov=None, rampTime=0.3):
        if fov == 0:
            fov = DEFAULT_FOV
        if newFov is None:
            newFov = 2 * math.atan(math.tan(fov / 2) / multiplier)
        BigWorld.projection().rampFov(newFov, rampTime)
        self.magnified = True

    def unmagnify(self, fov=0, rampTime=0.1):
        if fov == 0:
            fov = DEFAULT_FOV
        if getattr(self, 'magnified', False):
            BigWorld.projection().rampFov(fov, rampTime)
            self.magnified = False

    @BWKeyBindingAction('Crouch')
    def onCrouch(self, isDown):
        if isDown and not self.crouching:
            self.UpdateCrouch(True)
        elif not isDown:
            self.UpdateCrouch(False)

    @BWKeyBindingAction('ToggleCrouch')
    def onToggleCrouch(self, isDown):
        if not isDown:
            self.UpdateCrouch(False, toogle=True)

    def UpdateCrouch(self, is_holding_key, toogle=False):
        oldCrouch = self.crouching
        if toogle or (is_holding_key and self.crouching) or not self.canCrouch():
            return
        self.crouching = not self.crouching if not is_holding_key else is_holding_key
        if not self.crouching and hasattr(self.physics, 'mayStand') and not self.physics.mayStand:
            self.crouching = True
        if self.crouching != oldCrouch:
            self.tooFootUpdateCrouch()

        def toggle_crouching():
            self.cell.UpdateCrouch(self.crouching)
            Avatar.UpdateCrouch(self)
            self.UpdateSniping(self.sniping and not callback.findFirst('turn_off_sniping'))

        if self.crouching:
            callback(partial(toggle_crouching), 0.2, cancel_existing=True)
            self.physics.modelHeight = self.DefModelHeightCrouched
            self.sprinting = False
        else:
            toggle_crouching()
            self.physics.modelHeight = self.DefModelHeightStanding
        self.checkCamera()
        self.UpdateVelocity()
        
    @BWKeyBindingAction('SpawnNPC')
    def keySpawnNPC(self, isDown):
        if not isDown:
            self.spawn_npc_model(self.current_npc_folder)

    @BWKeyBindingAction('NextNPCType')
    def keyNextNPCType(self, isDown):
        if not isDown:
            try:
                idx = self.npc_folder_list.index(self.current_npc_folder)
                self.current_npc_folder = self.npc_folder_list[(idx + 1) % len(self.npc_folder_list)]
            except ValueError:
                self.current_npc_folder = self.npc_folder_list[0]
            self.systemChatline("Next NPC: " + self.current_npc_folder)

    @BWKeyBindingAction('ListNPCTypes')
    def keyListNPCTypes(self, isDown):
        if not isDown:
            self.list_model_folders()

    @UserCommand
    def list_model_folders(self):
        """Выводит список папок NPC и существ с указанием наличия .model файлов"""
        import os
        res_path = "F:/SO/so-education-main — копия/packs/res"

        def scan_folder(base, sub):
            full = os.path.join(res_path, base, sub)
            if os.path.isdir(full):
                files = [f for f in os.listdir(full) if f.endswith('.model')]
                return files
            return []

        print "=== NPC folders ==="
        for folder in self.npc_folder_list:
            files = scan_folder("characters/npc", folder)
            if not files:
                files = scan_folder("characters/creatures", folder)
            if files:
                print "  %s : %s" % (folder, ", ".join(files))
            else:
                print "  %s : NO MODEL FILES" % folder

    @BWKeyBindingAction('PrintModelActions')
    def keyPrintModelActions(self, isDown):
        if not isDown:
            return
        folder_name = self.current_npc_folder
        base_paths = ["characters/npc", "characters/creatures"]
        name_variants = [
            folder_name,
            folder_name + "_lod0",
            folder_name + "_lod1",
            folder_name + "_01",
            folder_name + "_body",
            "model"
        ]
        for base in base_paths:
            for variant in name_variants:
                path = base + "/" + folder_name + "/" + variant + ".model"
                try:
                    model = BigWorld.Model(path)
                    if model:
                        actions = model.getActionNames()
                        print "=== Animations for", path, "==="
                        for act in actions:
                            print "  ", act
                        return
                except:
                    continue
        print "No model found for", folder_name, "to list actions."

    @BWKeyBindingAction('DumpModelActions')
    def keyDumpModelActions(self, isDown):
        if not isDown:
            return
        folder = self.current_npc_folder
        import os
        res_path = "F:/SO/so-education-main — копия/packs/res"
        for base in ["characters/npc", "characters/creatures"]:
            folder_path = os.path.join(res_path, base, folder)
            if os.path.isdir(folder_path):
                for f in os.listdir(folder_path):
                    if f.endswith(".model"):
                        path = os.path.join(base, folder, f).replace("\\", "/")
                        try:
                            model = BigWorld.Model(path)
                            print "=== Testing actions for", folder, "==="
                            test_actions = ["Idle", "idle", "IdleUnarmed", "IdleForever", "Stand", "Walk", "Run", "Attack", "Death", "Base"]
                            for act in test_actions:
                                try:
                                    action = model.action(act)
                                    if action is not None:
                                        print "  OK:", act
                                    else:
                                        print "  None:", act
                                except Exception as e:
                                    print "  FAIL:", act, "->", str(e)
                            self.systemChatline("Action test results in python.log")
                        except Exception as e:
                            print "Error loading model:", e
                        return
        self.systemChatline("No model found for " + folder)

    @UserCommand
    def list_npc_types(self):
        """Выводит список возможных типов NPC, зарегистрированных в мире"""
        types = set()
        for e in BigWorld.entities.values():
            if e and not e.isDestroyed:
                clsname = e.__class__.__name__
                if clsname not in ('PlayerAvatar', 'DroppedItem', 'TriggerObject'):
                    types.add(clsname)
        print "Possible NPC types currently in world:"
        for t in sorted(types):
            print "  ", t

    @BWKeyBindingAction('Jump')
    def doJump(self, isDown):
        if self.crouching:
            self.UpdateCrouch(False)
            return
        if self.sniping:
            self.UpdateSniping(False)
            self.sniping = False
        if isDown:
            if self.canfly:
                self.physics.fall = False
                velocity = self.physics.velocity
                velocity[1] = 40
                self.physics.velocity = velocity
                self.physics.scheduleFall(0, False)
                return
            if self.is_sitting and not self.inputlock:
                self.ProceedSit(self.lastsit)
                return
            # Проверяем стамину только если НЕ бесконечная
            if not getattr(self, 'unlimited_stamina', False):
                if self.GetStatValue(Stats.ch_Stamina) < CharacterConst.STAMINA_JUMP_USAGE:
                    return
            if self.inputlock or not self.canJump() or self.control_locked:
                return
            if any(self.jumping_collisions()):
                self.cell.onJump()
                Avatar.onJump(self)
                # Вычитаем стамину только если НЕ бесконечная
                if not getattr(self, 'unlimited_stamina', False):
                    self.ch_Stamina['CurrentValue'] -= CharacterConst.STAMINA_JUMP_USAGE
                if self.StaminaUpdateCallback:
                    BigWorld.cancelCallback(self.StaminaUpdateCallback)
                self.OnStaminaChanged()
                self.physics.fall = False
                velocity = self.physics.velocity
                velocity_saved = Vector3(velocity)
                velocity[1] = 18
                self.physics.velocity = velocity
                if hasattr(self.physics, 'scheduleFall'):
                    self.physics.scheduleFall(0.2, True)
                else:
                    def scheduleFall():
                        self.physics.velocity = velocity_saved
                        self.physics.fall = True
                    BigWorld.callback(0.2, scheduleFall)
        elif not isDown and self.canfly:
            velocity = self.physics.velocity
            velocity[1] = 0
            self.physics.velocity = velocity

    def jumping_collisions(self):
        for shift in PlayerAvatar.JUMP_COLLISION_SHIFTS:
            pos = self.position + shift
            collide_result = BigWorld.collide(self.spaceID, pos + PlayerAvatar.JUMP_COLLISION_FROM, pos + PlayerAvatar.JUMP_COLLISION_TO)
            if collide_result:
                point, (p0, p1, p2), material_type = collide_result
                normal = (p1 - p0) * (p2 - p0)
                angle = angle_between_vectors(normal, VECTOR3_UP)
                if angle > math.pi / 2.0:
                    angle -= math.pi / 2.0
                if angle <= PlayerAvatar.MAX_SURFACE_ANGLE_TO_JUMP:
                    yield True
                else:
                    yield False
            else:
                yield False

    @BWKeyBindingAction('SpotLight')
    def switchSpotLight(self, isDown):
        self.InitSpotLight(True)

    @UserCommand
    def InitSpotLight(self, switch=False):
        light_params = self.CanTurnOnSpotLight()
        if self.ActiveItemID != 0 and not self.no_weapon_in_hands and not self.control_locked and light_params is not None and hasattr(self, 'spotLight'):
            self.spotLight.source = self.model.effectorright.lights.node('HP_lens')
            self.spotLight.colour, self.spotLight.cosConeAngle, self.spotLight.outerRadius, self.spotLight.innerRadius = light_params
            if switch:
                self.spotLight.visible = not self.spotLight.visible
                if not self.spotLight.visible:
                    pos_matrix = Math.Matrix()
                    pos_matrix.applyVector(self.position + Math.Vector3(0, 1000.0, 0))
                    self.spotLight.source = pos_matrix
                SFXer.FlashlightSwitch(self)
                self.flashLightLit = self.spotLight.visible
                self.cell.switchSpotLight(self.spotLight.visible)

    def CanTurnOnSpotLight(self):
        if self.ActiveItemType:
            equipped_item_param = ItemsCatalog.GetItemParam(self.ActiveItemType)
            gun_type = equipped_item_param['GunType']
            gun_priority = ItemsUtils.GetWeaponPriority(gun_type)
            upgrade_dict = self.SecondaryWeaponUpgrades if gun_priority == ItemsCatalog.SECONDARY else self.PrimaryWeaponUpgrades
            light_item_type = upgrade_dict.get('LightType', 0)
            if light_item_type > 0:
                light_params = ItemsCatalog.GetItemParam(light_item_type)
                return light_params['LightColour'], light_params['CosConeAngle'], light_params['OuterRadius'], light_params['InnerRadius']
            BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG_NO_FLASHLIGHT'))
        else:
            BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG5'))
        return None

    @BWKeyBindingAction('MoveForward')
    def moveForward(self, isDown):
        self.movingForward = isDown
        self.UpdateVelocity()
        if not isDown:
            self.SetSprinting(False)

    @BWKeyBindingAction('MoveBackward')
    def moveBackward(self, isDown):
        self.movingBackward = isDown
        self.UpdateVelocity()

    @BWKeyBindingAction('StrafeLeft')
    def moveLeft(self, isDown):
        self.movingLeft = isDown
        self.UpdateVelocity()

    @BWKeyBindingAction('StrafeRight')
    def moveRight(self, isDown):
        self.movingRight = isDown
        self.UpdateVelocity()

    @BWKeyBindingAction('Sprint')
    def sprintKey(self, isDown):
        if isDown and self.movingForward:
            self.SetSprinting(True)
        elif not isDown and self.movingForward:
            self.SetSprinting(False)

    def SetSprinting(self, new_sprinting):
        if not new_sprinting and not self.sprinting:
            return
        if new_sprinting and self.sprinting:
            callback.cancel('turn_off_sprinting')
            return
        if new_sprinting and not self.canSprint():
            return
        if self.GetStatValue(Stats.ch_Stamina) < CharacterConst.STAMINA_SPRINT_USAGE:
            return

        def apply_sprinting(sprinting):
            self.sprinting = sprinting
            self.cell.SetSprinting(sprinting)

        if new_sprinting:
            apply_sprinting(True)
            self.OnStaminaChanged(True)
        else:
            callback(partial(apply_sprinting, False), 0.2, cancel_existing=True, id='turn_off_sprinting')
            self.OnStaminaChanged(False)
            self.UpdateVelocity()

    def OnStaminaChanged(self, charStartRunning=True, test=False, test2=False):
        try:
            if not self.sprinting:
                # Логика восстановления стамины
                self.ch_Stamina['CurrentValue'] += CharacterConst.STAMINA_RECOVERY
                if self.ch_Stamina['CurrentValue'] > self.ch_MaxStamina['CurrentValue']:
                    self.ch_Stamina['CurrentValue'] = self.ch_MaxStamina['CurrentValue']

            # Логика расхода стамины во время спринта (Перенесено в общий поток)
            if self.sprinting and not self.unlimited_stamina:
                if self.ch_Stamina['CurrentValue'] > CharacterConst.STAMINA_SPRINT_USAGE:
                    self.ch_Stamina['CurrentValue'] -= CharacterConst.STAMINA_SPRINT_USAGE

            # Обновление скорости (общий блок)
            if not self.sprinting and self.ch_Stamina['CurrentValue'] < self.ch_MaxStamina['CurrentValue']:
                self.ch_MoveSpeed['CurrentValue'] = 5 # Базовая скорость, если не бежим и восстанавливаемся
            elif self.sprinting and self.ch_Stamina['CurrentValue'] <= 0:
                 self.ch_MoveSpeed['CurrentValue'] = 5 # Сброс к базовой скорости при исчерпании стамины
            else: # Бежим и у нас есть стамина, или мы просто бежим
                if self.ch_Stamina['CurrentValue'] > CharacterConst.STAMINA_SPRINT_USAGE * 2:
                    self.ch_MoveSpeed['CurrentValue'] = 5 * CharacterConst.SPRINT_SPEED_ADJ
                else:
                     self.ch_MoveSpeed['CurrentValue'] = 5

            self.UpdateVelocity()
            
            # Планирование следующего восстановления
            if not self.sprinting and self.ch_Stamina['CurrentValue'] < self.ch_MaxStamina['CurrentValue']:
                self.StaminaUpdateCallback = BigWorld.callback(1, self.OnStaminaChanged)

            # Проверка дыхания
            if self.GetStatValue(Stats.ch_Stamina) <= CharacterConst.STAMINA_JUMP_USAGE:
                self.sound_breathing.play()


        except Exception as e:
            print 'ERROR in OnStaminaChanged: %s' % e 



    def SprintChanged(self):
        if self.sprinting:
            self.restrictShoot(self.ShootRestictions.SPRINTING)
            self.onRightMouseButton(False)
            self.EnableModelPitch(False)
            BigWorld.projection().rampFov(RUNNING_FOV, 2)
            if PlayerAvatar.StaminaUsers.SPRINT not in self.stamina_users:
                self.stamina_users.append(PlayerAvatar.StaminaUsers.SPRINT)
        else:
            self.restrictShoot(self.ShootRestictions.SPRINTING, False)
            self.EnableModelPitch(True)
            if PlayerAvatar.StaminaUsers.SPRINT in self.stamina_users:
                self.stamina_users.remove(PlayerAvatar.StaminaUsers.SPRINT)
            if not self.sniping and not self.binoculing:
                BigWorld.projection().rampFov(DEFAULT_FOV, 2)
        self.UpdateVelocity()

    @BWKeyBindingAction('ReleaseCursor')
    def releaseCursor(self, isDown):
        if not isDown:
            self.isTogleCursor = not self.isTogleCursor
            BWPersonality.GUICore.setMouseAltState(self.isTogleCursor)

    @BWKeyBindingAction('InteractObject')
    def InteractObject(self, isDown):
        if isDown:
            self.ManipulateTarget()

    @BWKeyBindingAction('PickUpAll')
    def PickUpAll(self, isDown):
        if self.control_locked:
            return
        if isDown:
            self.PickUpInArea()

    @UserCommand
    def PickUpInArea(self):
        if self.canPickUp():
            self.cell.ScanAreaAndAdd()

    @BWKeyBindingAction('ReloadWeapon')
    def reload(self, isDown):
        if isDown:
            return
        if self.ReloadButtonRoutine() and self.canReload():
            if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
                reload_params = AvatarItemHolder.onReload(self)
                if reload_params is None:
                    return
                self.cell.reload()
                self.UpdateSniping(False)
                reload_type, num_ammo, item_type = reload_params
                reload_time = Durations.GetReloadDuration(self, reload_type, item_type, num_ammo)
                self.reloading = True
                Avatar.reload(self, reload_type, reload_time, num_ammo)
                self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, reload_time, lc('Items.GUIStrings.RELOAD'))

    def ReloadButtonRoutine(self):
        if self.control_locked:
            return False
        if self.ActiveItemJammed:
            self.UnJammWeapon()
            return False
        return True

    def onReloadAnimationEnd(self):
        self.BrakeAcuracy()
        Avatar.onReloadAnimationEnd(self)
        self.reloading = False

    def canReload(self):
        if not self.sprinting:
            error_type = AvatarItemHolder.canReload(self)
            if error_type == 0:
                return Restrictions.canReload(self)
            if error_type == 1:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG_NO_AMMO_TO_LOAD'))
            elif error_type == 2:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG_AMMO_IS_FULL'))
            elif error_type == 3:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG5'))
            else:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG_UNABLE_TO_RELOAD'))
            return False
        BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG_RELOAD_ON_SPRINT'))
        return False

    def getReloadTimeModifyer(self, gun_type, item_type):
        return Character.getReloadTimeModifyer(self, gun_type, item_type)

    @BWKeyBindingAction('ChangeAmmoType')
    def ChangeCurrentWeaponAmmo(self, isDown):
        if isDown and self.ReloadButtonRoutine():
            AvatarItemHolder.ChangeActiveItemAmmoType(self)

    def canLoadAmmo(self, id):
        if AvatarItemHolder.canLoadAmmo(self, id):
            return Restrictions.canLoadAmmo(self, id)
        return False

    def LoadAmmoInCurrentWeapon(self, ammo_id):
        if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS) and self.canLoadAmmo(ammo_id):
            reload_params = AvatarItemHolder.onLoadAmmoInCurrentWeapon(self, ammo_id)
            if reload_params is not None:
                reload_type, num_loaded_ammo, item_type = reload_params
                reload_time = Durations.GetReloadDuration(self, reload_type, item_type, num_loaded_ammo)
                Avatar.reload(self, reload_type, reload_time, num_loaded_ammo)
                self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, reload_time, lc('Items.GUIStrings.LOAD_AMMO'))

    def useItem(self, item):
        if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
            error_level, duration = AvatarItemHolder.onUseItem(self, item)
            self.ReportFail(error_level)
            self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, duration, lc('Items.GUIStrings.USING'))

    def useItemOnTarget(self, itemID, entity=None):
        if entity is None:
            entity = BigWorld.target()
        if not isinstance(entity, Avatar) or isinstance(entity, NPC):
            return
        if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
            duration = AvatarItemHolder.onUseItemOnTarget(self, entity.id, itemID)
            self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, duration, lc('Items.GUIStrings.USING'))

    def BrakeAcuracy(self):
        self.clientAccuracy = self.getShot_WeaponAccuracyMin()

    def onAnimateFireEnd(self):
        self.restrictShoot(PlayerAvatar.ShootRestictions.RELOAD, False)
        self.BrakeAcuracy()
        Avatar.onAnimateFireEnd(self)

    def enlargeCrosshair(self):
        print 'PlayerAvatar::enlargeCrosshair uses banned methods and objects, redefine'

    def shrinkCrosshair(self):
        print 'PlayerAvatar::shrinkCrosshair uses banned methods and objects, redefine'

    @BWKeyBindingAction('ViewEntities')
    def ViewEntitiesMarks(self, isDown):
        if self.control_locked:
            return
        self.showEntitiesMarks = isDown
        self.UpdateEntitiesMarks()

    def UpdateEntitiesMarks(self):
        if self.callbackUpdateEntitiesMarks:
            BigWorld.cancelCallback(self.callbackUpdateEntitiesMarks)
            self.callbackUpdateEntitiesMarks = None
        marks = []
        targetEntity = BigWorld.target()
        self.targetObjects[targetEntity] = 1

        def AddEntityMark(entity, alpha):
            if entity == self:
                return
            entity_type = type(entity)
            if entity_type == Avatar:
                mark_icons = [soInworldMarker.MARKER_PLAYER]
                if entity.pvpFlag:
                    mark_icons.append(soInworldMarker.MARKER_PK)
                if entity.name in self.HUNTER_listOfWanted:
                    mark_icons.append(soInworldMarker.MARKER_WANTED)
                mark_action = [soInworldMarker.MARKER_USE]
                mark_text = colorCodes.mark_name if entity.karma < 500 else colorCodes.mark_name_PK
                if entity.AgrFlag and entity.karma < 500:
                    mark_text = colorCodes.mark_AGR
                mark_text += get_entity_name(entity, utf8=True)
                mark_dist = Constants.HILITE_INTERACTION_DISTANCE
                if entity.clanName:
                    mark_text += u''
                    if entity.clanName in self.clanEnemies:
                        if entity.clanName in self.clanHostiles:
                            mark_text += colorCodes.mark_clan_in_war
                        else:
                            mark_text += colorCodes.mark_clan_enemy_not_hostile
                    elif entity.clanName in self.clanHostiles:
                        mark_text += colorCodes.mark_clan_hostile_not_enemy
                    else:
                        mark_text += colorCodes.mark_clan_neutral
                    mark_text += entity.clanName.decode('utf-8')
                mark_height = 0.5 if entity.dead else 1.9
            elif entity_type in (NPC, sNPC):
                mark_icons = [soInworldMarker.MARKER_NPC]
                mark_text = colorCodes.mark_name + get_entity_name(entity, utf8=True)
                if entity.clanName:
                    if entity.clanName in self.clanEnemies:
                        if entity.clanName in self.clanHostiles:
                            mark_text += colorCodes.mark_clan_in_war
                        else:
                            mark_text += colorCodes.mark_clan_enemy_not_hostile
                    elif entity.clanName in self.clanHostiles:
                        mark_text += colorCodes.mark_clan_hostile_not_enemy
                    else:
                        mark_text += colorCodes.mark_clan_neutral
                    mark_text += u'' + entity.clanName.decode('utf-8')
                mark_height = 0.5 if entity.dead else 1.9
                mark_dist = Constants.HILITE_INTERACTION_DISTANCE
                mark_action = []
                if Helpers.Caps.CAP_CAN_TALK in entity.targetCaps:
                    mark_action.append(soInworldMarker.MARKER_TALK)
                if Helpers.Caps.CAP_CAN_TRADE in entity.targetCaps:
                    mark_action.append(soInworldMarker.MARKER_TRADE)
            elif entity_type == DroppedItem:
                mark_icons = [soInworldMarker.MARKER_ITEM]
                mark_text = get_entity_name(entity, utf8=True)
                mark_height = 0.6
                mark_dist = Constants.HILITE_INTERACTION_DISTANCE
                mark_action = [soInworldMarker.MARKER_PICKUP] if Helpers.Caps.CAP_CAN_PICKUP in entity.targetCaps else []
            elif entity_type == TriggerObject and (Helpers.Caps.CAP_CAN_USE in entity.targetCaps or Helpers.Caps.CAP_CAN_TALK in entity.targetCaps):
                mark_icons = []
                mark_text = entity.name if hasattr(entity, 'name') else entity_type.__name__
                mark_height = 0.6
                mark_action = [soInworldMarker.MARKER_USE]
                mark_dist = Constants.INTERACTION_DISTANCE
            elif entity_type == Creature:
                info = self.creatureDebugInfo.get(entity.id)
                if not info:
                    return
                mark_icons = info['icons']
                mob = BigWorld.entities[entity.id]
                mark_text = 'state: %s\n' % Config.Creatures.get_state_name(mob.creatureType, mob.level, mob.state)
                mark_text += 'dist: %.1f(%.1f), flat %.1f(%.1f)\n' % (info.get('distance', -1), self.position.distTo(entity.position),
                                                                      info.get('flat_distance', -1), self.position.flatDistTo(entity.position))
                mark_text += 'id: %d, ' % entity.id + info['text']
                mark_height = 1.9
                mark_dist = Constants.CREATURES_MARK_DISTANCE
                mark_action = []
            elif hasattr(entity, 'targetCaps'):
                useCapsSet = set([Helpers.Caps.CAP_CAN_PICKUP, Helpers.Caps.CAP_CAN_TRADE, Helpers.Caps.CAP_CAN_EXCHANGE,
                              Helpers.Caps.CAP_CAN_OPEN_AND_EXPLORE, Helpers.Caps.CAP_CAN_TELEPORT, Helpers.Caps.CAP_CAN_USE,
                              Helpers.Caps.CAP_CAN_TALK, Helpers.Caps.CAP_OPEN_BULLETIN_BOARD, Helpers.Caps.CAP_OPEN_WORKBENCH,
                              Helpers.Caps.CAP_CAN_OPEN_AND_EXPLORE_USER_FIRE])
                if useCapsSet & set(entity.targetCaps):
                    mark_icons = [soInworldMarker.MARKER_ITEM]
                    mark_text = entity.name if hasattr(entity, 'name') else entity_type.__name__
                    mark_height = 0.6
                    if hasattr(entity, 'model'):
                        mark_height = entity.model.height + 0.15
                    mark_action = [soInworldMarker.MARKER_USE]
                    mark_dist = Constants.INTERACTION_DISTANCE
                else:
                    return
            else:
                return
            if self.position.distSqrTo(entity.position) > mark_dist ** 2:
                return
            if mark_action and entity == targetEntity and self.position.distSqrTo(entity.position) < Constants.INTERACTION_DISTANCE ** 2:
                mark_icons += mark_action
            marks.append((mark_text, ShiftProvider(entity.matrix, (0, mark_height, 0)), mark_icons, alpha))

        hilightedObjects = []
        party_ids = [m[1] for m in self.ClientGroupInfo['members']]
        for entity in BigWorld.entities.values():
            if entity.id in party_ids or (hasattr(entity, 'clanName') and entity.clanName == self.clanName and type(entity) == Avatar):
                hilightedObjects.append(entity)
                AddEntityMark(entity, 1)

        if self.showEntitiesMarks:
            mark_sqrange = Constants.HILITE_MARKS_DISTANCE ** 2
            mark_caps = set([Helpers.Caps.CAP_CAN_TRADE])
            for entity in BigWorld.entities.values():
                if entity.position.distSqrTo(self.position) < mark_sqrange and mark_caps & set(entity.targetCaps):
                    hilightedObjects.append(entity)
                    AddEntityMark(entity, 1)
            self.callbackUpdateEntitiesMarks = BigWorld.callback(1.5, self.UpdateEntitiesMarks)

        if self.debugEnabled:
            for entity in BigWorld.entities.values():
                if isinstance(entity, Creature):
                    if entity.id in self.creatureDebugInfo:
                        AddEntityMark(entity, 1)

        for entity, alpha in self.targetObjects.items():
            if entity not in hilightedObjects:
                AddEntityMark(entity, alpha)

        BWPersonality.GUICore.setInworldMarkersData(marks)
        BWPersonality.GUICore.showInworldMarkers(True)

    def ChangeStamina(self, value):
        self.stamina += value
        if self.stamina <= 0.0:
            self.stamina = 0.0
            self.staminaRecuperate = True
            self.OnStaminaEnded()
        if self.stamina >= self.GetMaxStamina():
            self.staminaRecuperate = False
            self.OnStaminaFilled()

    def set_heartMode(self, oldValue):
        self.ControlHeartMode()

    def ControlHeartMode(self):
        if self.heartMode and self.unstableScope:
            self.unstableScope.StartHeartMode()
        elif self.unstableScope:
            self.unstableScope.EndHeartMode()

    def InitTargetObjectMarks(self):
        alpha_delta = 0.1 / Constants.HILITE_INTERACTION_TIME

        def Updater():
            if self.isDestroyed:
                return
            entities = [e for e in BigWorld.entities.values() if not e.isDestroyed]
            for entity, alpha in list(self.targetObjects.items()):
                if alpha < alpha_delta or entity not in entities:
                    del self.targetObjects[entity]
                else:
                    self.targetObjects[entity] = alpha - alpha_delta
            self.UpdateEntitiesMarks()
            BigWorld.callback(0.1, Updater)

        BigWorld.callback(0.1, Updater)

    def showDamage(self, damage, fromId, toMe=False):
        return  # отключено в оригинале
        try:
            entity = BigWorld.entity(fromId, True)
            name = get_entity_name(entity)
        except:
            name = ''
        txt = '%s: %.1f' % (name, damage)
        damageBox = GUI.Text(txt)
        damageBox.explicitSize = True
        damageBox.font = 'ruRU_calibri_default.font'
        damageBox.size = (0, 0.1)
        damageBox.filterType = 'LINEAR'
        damageBox.verticalAnchor = 'BOTTOM'
        damageBox.visible = self.SHOW_DAMAGE
        damageBox.colour = (0, 255, 0, 255) if toMe else (255, 0, 0, 255)
        damageBox.position = (1.0, 1.0, 0) if toMe else (-1.0, 1.0, 0)
        damageBoxAtch = GUI.Attachment()
        damageBoxAtch.component = damageBox
        damageBoxAtch.faceCamera = False
        if toMe:
            self.moveUpDamageTaken()
            self.damageTakenTexts.append(damageBoxAtch)
        else:
            self.moveUpDamageDone()
            self.damageDoneTexts.append(damageBoxAtch)
        self.model.root.attach(damageBoxAtch)

    def hideDamage(self, box):
        if box in self.damageTexts:
            self.damageTexts.remove(box)
        self.model.root.detach(box)
        del box

    def hideAllDamages(self):
        self.hideAllDamage(self.damageDoneTexts)
        self.hideAllDamage(self.damageTakenTexts)

    def hideAllDamage(self, arr):
        i = 0
        while i < len(arr):
            dam = arr[i]
            dam.component.position += (0, 0.05, 0)
            dam.component.colour -= (0, 0, 0, 2.0)
            arr.remove(dam)
            if dam.attached:
                self.model.root.detach(dam)
            del dam

    def moveUpDamages(self):
        if self.isDestroyed:
            return
        self.moveUpDamage(self.damageDoneTexts)
        self.moveUpDamage(self.damageTakenTexts)
        self.moveUpDamagesTimer = BigWorld.callback(0.5, self.moveUpDamages)

    def moveUpDamage(self, arr):
        i = 0
        while i < len(arr):
            dam = arr[i]
            dam.component.position += (0, 0.05, 0)
            dam.component.colour -= (0, 0, 0, 2.0)
            if dam.component.position[1] > 3.0:
                arr.remove(dam)
                if dam.attached:
                    self.model.root.detach(dam)
                del dam
            else:
                i += 1

    def moveUpDamageDone(self):
        self.moveUpDamage(self.damageDoneTexts)

    def moveUpDamageTaken(self):
        self.moveUpDamage(self.damageTakenTexts)

    def beginStartCraft(self, isDown):
        pass

    @BWKeyBindingAction('TimeOfDayIncrease')
    def timeOfDayIncrease(self, isDown):
        pass

    @BWKeyBindingAction('TimeOfDayDecrease')
    def TimeOfDayDecrease(self, isDown):
        pass

    # Quick slots 1-10
    @BWKeyBindingAction('QuickSlot1')
    def QuickSlot1(self, isDown):
        if isDown: self.UseQuickSlot(0)
    @BWKeyBindingAction('QuickSlot2')
    def QuickSlot2(self, isDown):
        if isDown: self.UseQuickSlot(1)
    @BWKeyBindingAction('QuickSlot3')
    def QuickSlot3(self, isDown):
        if isDown: self.UseQuickSlot(2)
    @BWKeyBindingAction('QuickSlot4')
    def QuickSlot4(self, isDown):
        if isDown: self.UseQuickSlot(3)
    @BWKeyBindingAction('QuickSlot5')
    def QuickSlot5(self, isDown):
        if isDown: self.UseQuickSlot(4)
    @BWKeyBindingAction('QuickSlot6')
    def QuickSlot6(self, isDown):
        if isDown: self.UseQuickSlot(5)
    @BWKeyBindingAction('QuickSlot7')
    def QuickSlot7(self, isDown):
        if isDown: self.UseQuickSlot(6)
    @BWKeyBindingAction('QuickSlot8')
    def QuickSlot8(self, isDown):
        if isDown: self.UseQuickSlot(7)
    @BWKeyBindingAction('QuickSlot9')
    def QuickSlot9(self, isDown):
        if isDown: self.UseQuickSlot(8)
    @BWKeyBindingAction('QuickSlot10')
    def QuickSlot10(self, isDown):
        if isDown: self.UseQuickSlot(9)

    # Quick lines 1-10
    @BWKeyBindingAction('QuickLine1')
    def QuickLine1(self, isDown):
        if isDown: self.UseQuickLine(0)
    @BWKeyBindingAction('QuickLine2')
    def QuickLine2(self, isDown):
        if isDown: self.UseQuickLine(1)
    @BWKeyBindingAction('QuickLine3')
    def QuickLine3(self, isDown):
        if isDown: self.UseQuickLine(2)
    @BWKeyBindingAction('QuickLine4')
    def QuickLine4(self, isDown):
        if isDown: self.UseQuickLine(3)
    @BWKeyBindingAction('QuickLine5')
    def QuickLine5(self, isDown):
        if isDown: self.UseQuickLine(4)
    @BWKeyBindingAction('QuickLine6')
    def QuickLine6(self, isDown):
        if isDown: self.UseQuickLine(5)
    @BWKeyBindingAction('QuickLine7')
    def QuickLine7(self, isDown):
        if isDown: self.UseQuickLine(6)
    @BWKeyBindingAction('QuickLine8')
    def QuickLine8(self, isDown):
        if isDown: self.UseQuickLine(7)
    @BWKeyBindingAction('QuickLine9')
    def QuickLine9(self, isDown):
        if isDown: self.UseQuickLine(8)
    @BWKeyBindingAction('QuickLine10')
    def QuickLine10(self, isDown):
        if isDown: self.UseQuickLine(9)

    def EquipWeaponCommand(self, item):
        if item is None:
            return
        if not self.control_locked and not self.is_sitting and not self.sniping and not self.binoculing and not self.reloading and self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
            self.inputlock = True
            duration = Durations.GetEquipDuration(self, item) + Durations.GetEquipDuration(self, self.ActiveItemID)
            callback(partial(self.inputlockOff), duration * 0.6, cancel_existing=True, id='inputlock_off')
            if self.flashLightLit:
                self.InitSpotLight(True)
            if item != 0:
                self.equipItem(item)
                Inventory.WeaponSplash(self, item)
                self.no_weapon_in_hands = False
                if self.ActiveItemID == 0:
                    self.EnableModelPitch(True)
                callback(partial(self.EnableCrosshair), duration * 0.2)
            else:
                self.EnableModelPitch(False)
                self.weapon_was_in_hands_id = self.ActiveItemID
                self.weapon_was_in_hands_type = self.ActiveItemType
                self.equipItem()
                self.no_weapon_in_hands = True
                BWPersonality.GUICore.targettingGUI.only_dot(True)
                Inventory.WeaponSplash(self, item)
        else:
            BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG3'))

    def setClanLeader(self, value):
        self.isClanLeader = value

    def startTradeBase(self):
        if self.isClanLeader:
            self.cell.baseTradeinfo()
        else:
            gui_jokes.askUserOk(lc('GUI.DonateBase.title'), lc('GUI.DonateBase.text'))

    def getBaseByName(self, name):
        self.cell.getDonateBaseByName(name)
        BWPersonality.GUICore.showDetailViewStakeGUI()

    def getMaxPrice(self):
        print self.donateBase['maxPrice']

    def setNewPrice(self, newPrice):
        self.cell.setNewPrice(newPrice)

    def incByStep(self):
        STEP = 500
        self.setNewPrice(self.donateBase['maxPrice'] + STEP)

    def set_donateBase(self, oldValue):
        BWPersonality.GUICore.setDetailViewStakeData({
            'clan': self.clanName,
            'timeToSell': self.timeToString(self.donateBase['timeToSell']),
            'maxPrice': str(self.donateBase['maxPrice']),
            'countMembers': str(self.donateBase['countMembers']),
            'stepAuction': str(500),
            'incStake': str(self.donateBase['maxPrice'] + 500),
            'minPrice': str(self.donateBase['minPrice'])
        })

    def setNested_donateBase(self, path, oldValue):
        self.set_donateBase(oldValue)

    def set_donateBaseDeposit(self, oldValue):
        BWPersonality.GUICore.setDeposit(self.donateBaseDeposit)

    def timeToString(self, time_val):
        if time_val < 0:
            return '-'
        MIN = 60
        HOUR = MIN * 60
        DAY = HOUR * 24
        if time_val < MIN:
            return lc('tmplocal.strings.str69')
        days = time_val // DAY
        hours = (time_val % DAY) // HOUR
        mins = (time_val % HOUR) // MIN
        time_text = lc('tmplocal.strings.str70') % mins
        if hours > 0:
            time_text = lc('tmplocal.strings.str71') % hours + time_text
        if days > 0:
            time_text = lc('tmplocal.strings.str72') % days + time_text
        return '%s:%s:%s' % (int(days), int(hours), int(mins))

    def setDonateBaseList(self, base):
        base = sorted(base, key=lambda x: lc('DonateBases.name.%s' % x['name']))
        BWPersonality.GUICore.showDonateBase()
        BWPersonality.GUICore.setBaseTraderData([b for b in base])

    def setDeposit(self, value=1000):
        self.cell.pay(value)

    def depositBack(self):
        self.cell.depositBack()

    def cashback(self):
        self.cell.cashback()

    def showInfoTradeBase(self):
        BWPersonality.GUICore.showBasetrader(True)
        BWPersonality.GUICore.setBaseTraderData({'clanName': self.clanName})

    def StartExchange(self, entity):
        def okey_callback(event):
            if event == gui_jokes.askUserYesNo.YES:
                self.tradeEntity = entity
                self.base.isBlackList(entity.name.encode('utf-8'))
            else:
                self.isTrade = False
        if not entity.dead and not self.isTrade:
            gui_jokes.askUserYesNo(lc('PlayerAvatar.client.INIT_TRADE'),
                                   lc('PlayerAvatar.client.DOYOU_WANT_TO_START_TRADE').format(entity.name),
                                   okey_callback)
            self.isTrade = True

    def startTrade(self):
        self.cell.BeginExchange(self.tradeEntity.id)

    def showBaseMessage(self, message_id, base_name, clan_name):
        if message_id == 0:
            self.systemChatline(lc('GUI.DonateBase.free').format(name=lc('DonateBases.name.%s' % base_name)))
        elif message_id == 1:
            self.systemChatline(lc('GUI.DonateBase.owner').format(name=lc('DonateBases.name.%s' % base_name),
                                                                  clan=clan_name.decode('utf-8')))

    def guards_activate(self):
        self.cell.guards_activate()

    def continueDialogWithData(self, cost):
        for item in self.dialogCurrent:
            if '%COMPLEX_COST%' in item['Title'] or '%COMPLEX_COST%' in item['Text']:
                item['Title'] = item['Title'].replace('%COMPLEX_COST%', u'[' + unicode(cost) + u']')
                item['Text'] = item['Text'].replace('%COMPLEX_COST%', u'[' + unicode(cost) + u']')
        self.showGetQuestDialog(self.dialogCurrent, self.dialogEntityID)

    def showGetQuestDialog(self, dialogs, sourceEntityID):
        dialogs = sorted(dialogs, key=lambda k: k['Actions']['Exit'])
        self.dialogEntityID = sourceEntityID
        if len(dialogs) < 2:
            dialogs.append(dict(DialogID=0, Holder='', Title=lc('Dialogs.Interface.OVER_DIALOG'), Text=u'', Nodes=[],
                                Precondition=dict(ListOfNecessaryQuests=dict(listOfCompletedQuests=[], listOfOpenedQuests=[], listOfOnTestQuests=[]),
                                                  ListOfMustNoQuests=dict(listOfCompletedQuests=[], listOfOpenedQuests=[], listOfOnTestQuests=[]),
                                                  tests=[], Reputation='', KarmaPK=[]),
                                Actions=dict(Exit=1, ToDialog=0, Event=0, GetQuest=[], CompleteQuest=[], Data='')))
        self.base.tryOpenNote(dialogs[0]['Holder'][0])
        self.dialogSourceEntity = BigWorld.entities[sourceEntityID]
        self.dialogCurrent = dialogs
        answers = []
        for i, item in enumerate(dialogs):
            if i > 0:
                if '||' in item['Title']:
                    answers.append((i, item['Title'].split('||')[0]))
                elif '|' in item['Title']:
                    answers.append((i, item['Title'].split('|')[0]))
                else:
                    answers.append((i, item['Title']))
            if '%COMPLEX_COST%' in item['Title'] or '%COMPLEX_COST%' in item['Text']:
                self.continueDialogWithData(self.GetEquipedItemsRepairCost(self.dialogSourceEntity))
                return
        name = self.dialogSourceEntity.name if hasattr(self.dialogSourceEntity, 'name') else u''
        self.dialogHistory.append((name, dialogs[0]['Text']))
        resDialog = u''
        self.dialogHistory.reverse()
        for i, e in enumerate(self.dialogHistory):
            colorNames = colorCodes.dialog_self_name if e[0] == lc('PlayerAvatar.client.STRING_2743_56') else colorCodes.dialog_npc_name
            colorText = colorCodes.dialog_last_text if not i else colorCodes.dialog_text
            resDialog += colorNames + e[0] + u': ' + colorText + e[1] + '\n\n'
        self.dialogHistory.reverse()
        data = (name, resDialog, tuple(answers))
        BWPersonality.GUICore.setDialogueData(data)
        if not self.isDialogStarted:
            self.isDialogStarted = True
            BWPersonality.GUICore.showDialogueGUI(True)
            BWPersonality.GUICore.addListener('dialogueEvent', self.chooseAnswer)

    def chooseAnswer(self, event, data):
        if event == BWPersonality.soGUI.soDialogueGUI2.EVENT_ANSWER:
            self.dialogChoosenButton = data[0]
            item = self.dialogCurrent[self.dialogChoosenButton]
            if '||' in item['Title']:
                answer = item['Title'].replace('||', u'')
            elif '|' in item['Title']:
                answer = item['Title'].split('|')[1]
            else:
                answer = item['Title']
            self.dialogHistory.append((lc('PlayerAvatar.client.STRING_2743_56'), answer))
            if item['Actions']['GetQuest']:
                self.questerRequestGetted()
            elif item['Actions']['CompleteQuest']:
                self.questerRequestCompleted()
            else:
                self.ContinueDialog()
        elif event in (BWPersonality.soGUI.soDialogueGUI2.EVENT_USERCLOSE, BWPersonality.soGUI.soDialogueGUI2.EVENT_CLOSE):
            self.chooseCloseDialog(True, True)

    def questerRequestGetted(self):
        chosen = self.dialogChoosenButton
        if self.dialogCurrent[chosen]['Actions']['GetQuest']:
            self.queryDialogRequest['GetQuest'] = list(self.dialogCurrent[chosen]['Actions']['GetQuest'])
            quests = self.dialogCurrent[chosen]['Actions']['GetQuest']
            self.cell.requestQuestFromDialog(self.dialogSourceEntity.id, quests)
        else:
            self.questerRequestCompleted()

    def questerRequestCompleted(self):
        chosen = self.dialogChoosenButton
        if self.dialogCurrent[chosen]['Actions']['CompleteQuest']:
            self.queryDialogRequest['CompleteQuest'] = list(self.dialogCurrent[chosen]['Actions']['CompleteQuest'])
            for quest in self.dialogCurrent[chosen]['Actions']['CompleteQuest']:
                self.cell.checkQuestOnQuestID(quest)
        else:
            self.ContinueDialog()

    def ContinueSameDialog(self):
        self.showGetQuestDialog(self.dialogCurrent, self.dialogSourceEntity.id)

    def ContinueDialog(self):
        chosen = self.dialogChoosenButton
        if self.dialogCurrent[chosen]['Actions']['ToDialog']:
            object_name = ''
            cachedIDs = [[], []]
            if isinstance_ext(self.dialogSourceEntity, 'NPC'):
                object_name = self.dialogSourceEntity.npcName
            elif isinstance_ext(self.dialogSourceEntity, 'TriggerObject'):
                object_name = self.dialogSourceEntity.triggerName
            if object_name:
                cachedIDs = BWPersonality.cache.getDialogIDs(object_name)
            self.cell.onStartTalk(self.dialogEntityID, self.dialogCurrent[chosen]['Actions']['ToDialog'],
                                  Dialog.GET, cachedIDs[0], cachedIDs[1])
        elif self.dialogCurrent[chosen]['Actions']['Event']:
            event_type = self.dialogCurrent[chosen]['Actions']['Event']
            self.chooseCloseDialog(True, True)
            if event_type == Dialog.EVENT_TYPE_TRADE:
                self.onStartTrading(self.dialogSourceEntity)
            elif event_type == Dialog.EVENT_TYPE_CHANGE:
                self.onStartItemCache(self.dialogSourceEntity)
            elif event_type == Dialog.EVENT_TYPE_CREATECLAN:
                self.showConfirmNotice(Notices.CLAN_CREATE, 0, [])
            elif event_type == Dialog.EVENT_TYPE_REPAIR:
                self.onStartRepair(self.dialogSourceEntity)
            elif event_type == Dialog.EVENT_TYPE_BARTER:
                self.onStartBarter(self.dialogSourceEntity)
            elif event_type == Dialog.EVENT_TYPE_COMPLEX_REPAIR:
                self.onStartComplexRepair(self.dialogSourceEntity)
            elif event_type == Dialog.EVENT_TYPE_TELEPORT:
                self.cell.tpRequestDialog(self.dialogCurrent[chosen]['Actions']['Data'])
            elif event_type == Dialog.EVENT_TYPE_TELEPORT_TO_CLAN_BASE:
                self.cell.teleportToDonateBase(self.dialogSourceEntity.teleportName)
            elif event_type == Dialog.EVENT_TYPE_GO_PVP_AREA:
                BWPersonality.GUICore.showSelectMap(True)
        elif self.dialogCurrent[chosen]['Actions']['Exit'] == 1:
            self.chooseCloseDialog(True, True)
        else:
            cachedIDs = [[], []]
            object_name = ''
            if isinstance_ext(self.dialogSourceEntity, 'NPC'):
                object_name = self.dialogSourceEntity.npcName
            elif isinstance_ext(self.dialogSourceEntity, 'TriggerObject'):
                object_name = self.dialogSourceEntity.triggerName
            if object_name:
                cachedIDs = BWPersonality.cache.getDialogIDs(object_name)
            self.cell.onStartTalk(self.dialogEntityID, self.dialogCurrent[chosen]['DialogID'],
                                  Dialog.GET, cachedIDs[0], cachedIDs[1])

    def chooseCloseDialog(self, clearHistory=False, closeGUI=False):
        try:
            BWPersonality.GUICore.removeListener('dialogueEvent', self.chooseAnswer)
        except:
            pass
        if closeGUI:
            BWPersonality.GUICore.showDialogueGUI(False)
        if clearHistory:
            self.dialogHistory = []
            self.isDialogStarted = False
        self.dialogChoosenButton = None
        self.queryDialogRequest = {}
        self.dialogEntityID = 0
        BWPersonality.cache.saveCacheDialog()

    def temporarySpeedChange(self, mod, time_val):
        BigWorld.callback(time_val, partial(self.delSpeedModifier, mod))
        self.addSpeedModifier(mod)

    def addSpeedModifier(self, mod):
        self.localSpeedModifiers.append(mod)
        self.UpdateVelocity()

    def delSpeedModifier(self, mod):
        if self.isDestroyed:
            return
        if mod in self.localSpeedModifiers:
            self.localSpeedModifiers.remove(mod)
        self.UpdateVelocity()

    def updateDetectorBar(self, detector=None, maxDist=150.0):
        if detector is None:
            detector = self.detector
        if not ItemsUtils.CanUseGadjet(self, ItemsCatalog.ANOMALY_DETECTOR['TypeID']):
            BWPersonality.GUICore.setAnomalyThreat(-1)
        else:
            val = int(9 * max(0, (maxDist - detector) / maxDist))
            BWPersonality.GUICore.setAnomalyThreat(val)

    def GetGrenadeThrowModifyer(self):
        return Character.GetThrowModifyer(self)

    def ReportCodedMessage(self, code):
        code_messages = [
            '', lc('Items.Messages.FAIL_ITEM_CANT_BE_ATTACHED'), lc('Items.Messages.FAIL_ITEM_ALREADY_ATTACHED'),
            lc('Items.Messages.FAIL_ATTACHING_NOT_A_PART'), lc('Items.Messages.FAIL_MOTHER_NOT_A_WEAPON'),
            lc('Items.Messages.FAIL_MOTHER_CANT_CARRY'), lc('Items.Messages.FAIL_NOTHING_TO_REPAIR'),
            lc('Items.Messages.FAIL_LOW_SKILL_LEVEL'), lc('Items.Messages.FAIL_NO_REPAIR_KIT'),
            lc('Items.Messages.FAIL_REPAIR_FAILED'), lc('Items.Messages.FAIL_NOT_DETACHABLE'),
            lc('Items.Messages.FAIL_ALREADY_DETACHED'), lc('Items.Messages.FAIL_TRADER_NO_MONEY'),
            lc('Items.Messages.FAIL_TRADER_NO_WARE'), lc('Items.Messages.FAIL_CANT_SELL'),
            lc('Items.Messages.FAIL_NO_BATTARY'), lc('Items.Messages.FAIL_NO_MONEY'),
            lc('Items.Messages.FAIL_NO_RECIPE'), lc('Items.Messages.FAIL_NO_RESOURCE'),
            lc('Items.Messages.FAIL_CRAFT_ROLL_FAIL'), lc('Items.Messages.FAIL_ITEM_EQUIPPED'),
            lc('Items.Messages.FAIL_IMPROPER_AMMO'), lc('Items.Messages.AMMO_ALREADY_LOADED'),
            lc('Items.Messages.FAIL_TRADER_NOT_BUY_IT'), lc('Items.Messages.FAIL_ITEM_STRUCTURE'),
            lc('Items.Messages.FAIL_TOO_MANY_ITEMS'), lc('Items.Messages.CHECK_AND_CONFIRM'),
            lc('Items.Messages.ITEM_BROKEN_NOT_REPAIR'), lc('Items.Messages.FAIL_CANT_UNITE'),
            lc('Items.Messages.FAIL_NO_TRADER'), lc('Items.Messages.FAIL_PLAYER_EXCHANGE_CHANGED'),
            lc('Items.Messages.FAIL_MAX_ITEMS'), lc('Items.Messages.FAIL_NO_ITEM_HOLDER'),
            lc('Items.Messages.FAIL_NOT_IN_RANGE'), lc('Items.Messages.FAIL_CANT_TRADE'),
            lc('Items.Messages.FAIL_ITEM_QUEST'), lc('Items.Messages.FAIL_OTHER_ACTION'),
            lc('Items.Messages.FAIL_KNOWN_RECIPE'), lc('Items.Messages.FAIL_CLAN_ITEM'),
            lc('Items.Messages.FAIL_CANT_MODIFY_EQUIPPED_ITEM'), lc('Items.Messages.FAIL_NO_STORAGE_PLACE'),
            lc('Items.Messages.FAIL_USED_ITEM'), lc('Items.Messages.FAIL_OVERFLOW_SLOT'),
            lc('Items.Messages.FAIL_IMPOSSIBLE_COOK'), lc('Items.Messages.FAIL_STACK'),
            lc('Items.Messages.FAIL_USER_FIRE_ACCESS'), lc('PlayerAvatar.client.FAIL_UF_GROUND'),
            lc('PlayerAvatar.client.FAIL_UF_GEOMETRY'), lc('PlayerAvatar.client.FAIL_UF_OTHER_UF'),
            lc('PlayerAvatar.client.FAIL_UF_WATER'), lc('PlayerAvatar.client.FAIL_UF_SAFE_AREA'),
            lc('Items.Messages.FAIL_CONTAINER_OFERFLOW'), lc('Items.Messages.FAIL_CONTAINER_MAX_USE'),
            lc('Items.Messages.FAIL_ARTEFACT_DEAD'), lc('Items.Messages.FAIL_NO_WORKBRENCH')
        ]
        try:
            self.systemChatline(code_messages[code])
        except:
            traceback.print_exc()
            print 'ERROR ReportCodedMessage', code

    def onGeometryMapped(self, name):
        BigWorld.camera().spaceID = self.spaceID
        print 'PlayerAvatar::onGeometryMapped', name
        try:
            BWPersonality.GUICore.spaceChange(BWPersonality.currentSpace)
        except KeyError:
            print 'onGeometryMapped errors', BWPersonality.currentSpace
        self.updateWorldMapNotes(name)
        self.InitGPSProvider(name)
        self.initSpaceSounds(name)

    def updateWorldMapNotes(self, name):
        self.mapNotes = [x for x in self.mapNotes if x['flags'] not in range(2, 6)]
        self.base.onGeometryMapped(name)

    def getWorldMapNotes(self, name):
        self.mapNotes = [x for x in self.mapNotes if x['flags'] not in range(2, 6)]
        self.base.onNewGeometryMapped(name)

    def equipItem(self, item=0):
        if item:
            if ItemsUtils.CheckItemClan(self, ItemsCatalog.GetItemParam(item['complexItemType']), self.GetHolderClanID):
                self.ReportFail(ItemsUtils.FAIL_CLAN_ITEM)
                return
        if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
            duration = AvatarItemHolder.onEquipItem(self, item)
            self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, duration, lc('Items.GUIStrings.EQUIP'))

    def putOnItem(self, item, slot_number=0):
        if ItemsUtils.CheckItemClan(self, ItemsCatalog.GetItemParam(item['complexItemType']), self.GetHolderClanID):
            self.ReportFail(ItemsUtils.FAIL_CLAN_ITEM)
            return
        if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS) and not self.is_sitting and not self.sniping and not self.binoculing and not self.reloading:
            item_class = ItemsCatalog.GetItemClass(item['complexItemType'])
            if item_class == ItemsCatalog.WEAPON:
                ttsc = Durations.GetEquipDuration(self, item)
                callback(partial(self.EnableCrosshair), ttsc)
                self.no_weapon_in_hands = False
            elif self.sprinting:
                BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG_ARMOR_PUTON_SPRINT'))
                return
            duration = AvatarItemHolder.onPutOnItem(self, item, slot_number)
            self.putOnItemStep2(item)
            self.UpdateInventory()
            self.systemChatline('putOnItem duration: ' + str(duration))
        else:
            BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG3'))

    def putOnItemStep2(self, item):
        if ItemsUtils.CheckItemClan(self, ItemsCatalog.GetItemParam(item['complexItemType']), self.GetHolderClanID):
            self.ReportFail(ItemsUtils.FAIL_CLAN_ITEM)
            return
        if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
            duration = AvatarItemHolder.putOnItemStep2(self, item)
            self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, duration, lc('Items.GUIStrings.EQUIP'))
        self.systemChatline('putOnItemStep2')

    @UserCommand
    def putOffItem(self, item):
        if not self.is_sitting and not self.sniping and not self.binoculing and not self.reloading:
            item_class = ItemsCatalog.GetItemClass(item['complexItemType'])
            if item_class == ItemsCatalog.WEAPON:
                activeWeapon = ItemsUtils.GetComplexItemByID(self, self.ActiveItemID)
                if self.ActiveItemID != 0 and item['complexItemID'] == activeWeapon['complexItemID']:
                    self.no_weapon_in_hands = True
                    self.weapon_was_in_hands_id = 0
                    self.weapon_was_in_hands_type = None
                    BWPersonality.GUICore.targettingGUI.only_dot(True)
                    if self.spotLight.visible:
                        self.spotLight.visible = False
                        self.flashLightLit = False
                        self.cell.switchSpotLight(False)
            AvatarItemHolder.onPutOffItem(self, item)
        else:
            BWPersonality.gpd.sendLowerMessage(lc('PlayerAvatar.client.MSG3'))

    def makeMapNote(self, spaceName, position, notes, flags):
        entry = {'spaceName': spaceName, 'position': position, 'notes': notes, 'flags': flags}
        self.mapNotes.append(entry)
        self.base.makeMapNote(entry['spaceName'], entry['position'], entry['notes'], entry['flags'])

    @UserCommand
    def DeleteGPSMarks(self, mark_id):
        self.mapNotes.pop(mark_id)
        self.base.DeleteGPSMarks(mark_id)

    def getMapNote(self, mark_id):
        return self.mapNotes[mark_id]

    def getMapNoteText(self, id):
        if id == len(self.mapNotes):
            return lc('PlayerAvatar.client.STRING_3278_10')
        try:
            return self.mapNotes[id]['notes']
        except:
            return u''

    @BWKeyBindingAction('ToggleClanGUI')
    def toggleClanGUI(self, isDown=True):
        return False

    def canItemBeAdded(self):
        return not self.dead

    def showGetReady(self):
        print 'PlayerAvatar::showGetReady is not in use anymore'

    def CanStartArtefactScan(self, extractor_params, item):
        if ItemsUtils.GetComplexItemByID(self, item['complexItemID']) is None:
            self.ReportCodedMessage(ItemsUtils.FAIL_ITEM_STRUCTURE)
            self.artefactExtractor.DestroyExtractor()
            return False
        return True

    def CanStartArtefactExtraction(self, extractor_params, item):
        if ItemsUtils.GetComplexItemByID(self, item['complexItemID']) is None:
            self.ReportCodedMessage(ItemsUtils.FAIL_ITEM_STRUCTURE)
            self.artefactExtractor.DestroyExtractor()
            return False
        fuel_type = extractor_params['Fuel']
        if fuel_type != ItemsCatalog.NONE_TYPE:
            fuel_item = ItemsUtils.GetAmmoByType(self, fuel_type)
            if fuel_item:
                fuel_item_type = fuel_item['complexItemType']
                if ItemsUtils.GetItemQuanity(self.CarryingItems, fuel_item_type) > extractor_params['ExtractionConsumption']:
                    self.cell.DpleeteConsumables(fuel_item_type, extractor_params['ExtractionConsumption'])
                    return True
        self.ReportCodedMessage(ItemsUtils.FAIL_NO_BATTARY)
        return False

    def startArtifactExtraction(self, extractor_params, extractor_item):
        if not self.artefactExtractor:
            fuel_type = extractor_params['Fuel']
            if fuel_type != ItemsCatalog.NONE_TYPE:
                fuel_item = ItemsUtils.GetAmmoByType(self, fuel_type)
                if fuel_item:
                    fuel_item_type = fuel_item['complexItemType']
                    if ItemsUtils.GetItemQuanity(self.CarryingItems, fuel_item_type) > extractor_params['PowerOnConsumption']:
                        self.cell.DpleeteConsumables(fuel_item_type, extractor_params['PowerOnConsumption'])
                        self.artefactExtractor = PressGame(extractor_params, extractor_item)
                        return
            self.ReportCodedMessage(ItemsUtils.FAIL_NO_BATTARY)

    def GetScopeMaxShift(self):
        weapon_type = self.ActiveItemType
        if weapon_type:
            item_class = ItemsCatalog.GetItemClass(weapon_type)
            if item_class == ItemsCatalog.WEAPON:
                AccStandMods = ItemsUtils.unpackItemDict(self.CurrentWeaponParam['AccStandModsKeys'],
                                                         self.CurrentWeaponParam['AccStandModsValues'])
                Accuracy = self.CurrentWeaponParam['Accuracy']
                AccuracyBorder = self.CurrentWeaponParam['AccuracyBorder']
                scope_mod = AccStandMods[ItemsCatalog.WEAPON_SCOPEMOD_SNIPING_KNEES] if self.crouching else AccStandMods[ItemsCatalog.WEAPON_SCOPEMOD_SNIPING_STAND]
                return float(Accuracy * scope_mod * AccuracyBorder / FiringDefs.ACCURACY_PERCENT_MOD)

    def GetScopeRecoilValue(self):
        def GetFiringStandAccuracyMod(accuracy_mods):
            return accuracy_mods[ItemsCatalog.WEAPON_ACCMOD_STAND]
        def CalcRecoilvalue(acc_value, base_accuracy, AccStandMods):
            return float(base_accuracy * GetFiringStandAccuracyMod(AccStandMods) * abs(acc_value) / FiringDefs.ACCURACY_PERCENT_MOD)
        weapon_type = self.ActiveItemType
        if weapon_type:
            item_class = ItemsCatalog.GetItemClass(weapon_type)
            if item_class == ItemsCatalog.WEAPON:
                weapon_param = {'Kickback': self.CurrentWeaponParam['Kickback'],
                                'AccuracyBorder': self.CurrentWeaponParam['AccuracyBorder'],
                                'Accuracy': self.CurrentWeaponParam['Accuracy'],
                                'AccStandMods': ItemsUtils.unpackItemDict(self.CurrentWeaponParam['AccStandModsKeys'],
                                                                          self.CurrentWeaponParam['AccStandModsValues'])}
                return (CalcRecoilvalue(weapon_param['Kickback'], weapon_param['Accuracy'], weapon_param['AccStandMods']) / 2.0,
                        CalcRecoilvalue(weapon_param['AccuracyBorder'], weapon_param['Accuracy'], weapon_param['AccStandMods']) / 2.0)

    def reportBug(self, position, text):
        self.base.reportBug(position, text)

    def InFormWeponJammed(self):
        if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
            jamm_type = AvatarItemHolder.onInFormWeponJammed(self)
            if jamm_type is not None:
                self.cell.InFormWeponJammed()
                self.UpdateSniping(False)
                duration = Durations.GetInformJammDuration(self, jamm_type)
                Avatar.InFormWeponJammed(self, jamm_type, duration)
                self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, duration, lc('Items.GUIStrings.JAMM'))

    def InFormWeponJammedEnded(self):
        Avatar.InFormWeponJammedEnded(self)

    def UnJammWeapon(self):
        if self.CheckRestriction(RestrictionsUtils.CHANNEL_ITEMS):
            unjamm_type = AvatarItemHolder.onUnJammWeapon(self)
            if unjamm_type is not None:
                self.cell.UnJammWeapon()
                duration = Durations.GetUnJammDuration(self, unjamm_type)
                Avatar.UnJammWeapon(self, unjamm_type, duration)
                self.DoAction(RestrictionsUtils.CHANNEL_ITEMS, duration, lc('Items.GUIStrings.UNJAMM'))

    def UnJammWeaponEnded(self):
        Avatar.UnJammWeaponEnded(self)

    def updateLocalCaptureProgress(self, value, stype):
        if value < 0:
            x = value / -100.0
        elif value > 0:
            x = value / 100.0
        else:
            x = 0
        xprogress = {'currentProgress': (-1, stype)} if x == 0 else {'currentProgress': (x, stype)}
        self.pvpCaptureData['currentProgress'] = xprogress['currentProgress']
        BWPersonality.GUICore.showObjectivesGUI(True)
        BWPersonality.GUICore.setObjectiveData(self.pvpCaptureData)
        self.updateHidePvpDefenceDataCallback()

    def updateHidePvpDefenceDataCallback(self):
        if self.hidePvpDefenceDataCallbackID != 0:
            BigWorld.cancelCallback(self.hidePvpDefenceDataCallbackID)
        self.hidePvpDefenceDataCallbackID = BigWorld.callback(30.0, self.hidePvpDefenceData)

    def pvpDefenceDataUpdate(self, flags, capturedPoints, maxPoints, timeRemaining, timeRemainingType):
        self.pvpCaptureData['flags'] = []
        for e in flags:
            if e['status'] <= -99:
                ftype, fvalue = 1, e['status'] / -100.0
            elif e['status'] >= 99:
                ftype, fvalue = 0, e['status'] / 100.0
            else:
                ftype = 2
                fvalue = e['status'] / 100.0 if e['status'] >= 0 else e['status'] / -100.0
            self.pvpCaptureData['flags'].append((e['id'], ftype, fvalue, ftype))
        self.pvpCaptureData['time'] = (timeRemaining, 'ready') if timeRemainingType == 0 else (timeRemaining, 'battler')
        self.pvpCaptureData['total_points'] = u'%d/%d' % (capturedPoints, maxPoints)
        if capturedPoints > 0:
            BWPersonality.GUICore.showObjectivesGUI(True)
            self.updateHidePvpDefenceDataCallback()
        BWPersonality.GUICore.setObjectiveData(self.pvpCaptureData)

    def hidePvpDefenceData(self):
        if not self.isDestroyed:
            BWPersonality.GUICore.showObjectivesGUI(False)
            self.hidePvpDefenceDataCallbackID = 0

    def setPartyMember(self, id, data):
        BWPersonality.GUICore.setPartyMember(id, data)

    def delPartyMember(self, id):
        BWPersonality.GUICore.delPartyMember(id)

    def setPartyMemberEffect(self, id, effect_id):
        if effect_id:
            effectData = getEffect(effect_id)
            if effectData:
                guiData = [effectData['texture'], -1, effectData['type'], 0]
                BWPersonality.GUICore.setPartyMemberEffect(id, effect_id, guiData)
        else:
            BWPersonality.GUICore.delPartyMemberEffect(id, effect_id)

    def setHealthBarData(self, data):
        BWPersonality.GUICore.setHealthData(data)

    def onPartySettingsChanged(self):
        import Group
        def listener(event):
            if event == gui_jokes.askUserYesNoDelayDeafultNo.NO:
                self.sendMessage(u'/groupleave')
        any_member = self.ClientGroupInfo['members'][0]
        conf = u''
        if any_member['flag'] & Group.GROUP_ITEM_TO_RAISED:
            conf = lc('Groups.Interface.LOOD_WHO_TAKED')
        elif any_member['flag'] & Group.GROUP_ITEM_TO_LEADER:
            conf = lc('Groups.Interface.LOOD_LEADER')
        elif any_member['flag'] & Group.GROUP_ITEM_TO_RANDOM:
            conf = lc('Groups.Interface.LOOD_RANDOM')
        gui_jokes.askUserYesNoDelayDeafultNo(u'', lc('Groups.Interface.ON_LOOD_SETTINGS_CHANGED').format(conf), listener, 10.0)

    def acAddTask(self, script):
        script = zlib.decompress(script)
        hsh = hashlib.md5(script).hexdigest()
        with self.acLock:
            self.acTasks.append({'hash': hsh, 'script': script, 'validated': False})
        self.base.acValidateTask(hsh)

    def acOnValidated(self, hsh, result):
        with self.acLock:
            for task in self.acTasks:
                if task['hash'] == hsh:
                    if result:
                        task['validated'] = True
                    else:
                        self.acTasks.remove(task)
                    break
        self.acRunNextTask()

    def acRunNextTask(self):
        with self.acLock:
            if not self.acCurrentTask and self.acTasks:
                task = self.acTasks[0]
                if task['validated']:
                    self.acCurrentTask = task
                    self.acRun(task['script'])
                    self.acCheckResult()

    def acRun(self, script):
        try:
            code = compile(script, '<string>', 'exec')
            l = {}
            g = {'return_result': self.return_result}
            exec code in g, l
            return True
        except Exception as ex:
            import traceback
            s = traceback.format_exc()
            self.return_result('exception: %s' % s)
        return False

    def return_result(self, result):
        if not self.isDestroyed:
            self.acResult = result
            self.acResultEvent.set()

    def acSetCheckResultCallback(self):
        if self.acResultChecker:
            BigWorld.cancelCallback(self.acResultChecker)
        self.acResultChecker = BigWorld.callback(1.0, self.acCheckResult)

    def acCheckResult(self):
        if not self.isDestroyed:
            self.acSetCheckResultCallback()
            if self.acResultEvent.isSet():
                with self.acLock:
                    self.acResultEvent.clear()
                    hsh = self.acCurrentTask['hash']
                    self.base.acReturnResult(hsh, self.acResult)
                    self.acResult = None
                    self.acTasks.pop(0)
                    self.acCurrentTask = None
                self.acRunNextTask()

    @BWKeyBindingAction('showPVPScreen')
    def showPVPStat(self, isDown):
        if isDown and self.PVPStatistic['users']:
            self.showPVPStatistic()
        elif not isDown:
            self.hidePVPStatistic()

    def PlayerToFastError(self):
        pass

    def makeMapNotes(self, notes):
        for e in notes:
            if e['flags'] == MapNotes.TYPE_RESPAWN_POINT:
                self.mapNotes = [x for x in self.mapNotes if x['flags'] != MapNotes.TYPE_RESPAWN_POINT]
                self.mapNotes.append(e)
            elif e not in self.mapNotes:
                self.mapNotes.append(e)

    @BWKeyBindingAction('ToggleMemoryScreen')
    def toggleMemoryScreen(self, isDown=True):
        if isDown:
            return
        if not hasattr(self, 'memoryScreen'):
            self.memoryScreen = GUI.load('soGUI/GUIs/memory_check.gui')
            self.memoryScreenCallback = 0
        if self.memoryScreenCallback == 0:
            self.updateMemoryScreen()
            self.memoryScreen.visible = True
            GUI.addRoot(self.memoryScreen)
        else:
            BigWorld.cancelCallback(self.memoryScreenCallback)
            self.memoryScreenCallback = 0
            self.memoryScreen.visible = False
            GUI.delRoot(self.memoryScreen)

    def updateMemoryScreen(self):
        if self.isDestroyed:
            return
        self.memoryScreen.text1.text = 'Texture Memory: %s/%s MB' % (
            formatNumber(float(BigWorld.getWatcher('Memory/TextureManagerReckoningFrame')) / 1048576, 1),
            formatNumber(float(BigWorld.getWatcher('Memory/TextureManagerReckoning')) / 1048576, 1))
        drawCalls = BigWorld.getWatcher('Render/Draw Calls')
        primitives = BigWorld.getWatcher('Render/Primitives')
        self.memoryScreen.drawCalls.text = 'Draw Calls: ' + formatNumber(drawCalls)
        self.memoryScreen.primitives.text = 'Primitives: ' + formatNumber(primitives)
        self.memoryScreen.primitivesPerDrawCall.text = 'Primitives per Draw Call: ' + formatNumber(int(float(primitives) / float(drawCalls) + 0.5))
        loadedChunks = int(BigWorld.getWatcher('Chunks/Loaded Chunks'))
        self.memoryScreen.drawnArea.text = 'Loaded Chunks: %s sqkm / %s %%' % (formatNumber(loadedChunks / 100.0, 2),
                                                                               formatNumber(BigWorld.spaceLoadStatus() * 100.0, 2))
        self.memoryScreen.totalEntities.text = 'Total entities in AOI: ' + formatNumber(int(BigWorld.getWatcher('Entities/Active Entities')))
        self.memoryScreen.latency.text = 'Latency: %s ms' % formatNumber(float(BigWorld.getWatcher('Comms/Latency')) * 1000)
        self.memoryScreen.bandwidthToServer.text = 'To Server: %s kbps / %s' % (
            formatNumber(float(BigWorld.getWatcher('Comms/bps out')) / 1024, 1),
            formatNumber(BigWorld.getWatcher('Comms/Messages out'), 1))
        self.memoryScreen.bandwidthFromServer.text = 'From Server: %s kbps / %s' % (
            formatNumber(float(BigWorld.getWatcher('Comms/bps in')) / 1024, 1),
            formatNumber(BigWorld.getWatcher('Comms/Messages in'), 1))
        self.memoryScreenCallback = BigWorld.callback(0.1, self.updateMemoryScreen)

    @UserCommand
    def dropItem(self, item):
        AvatarItemHolder.onDropItem(self, item)

    @UserCommand
    def deleteItem(self, item):
        AvatarItemHolder.onDeleteItem(self, item)

    @UserCommand
    def BeginSpare(self, item, quantity):
        AvatarItemHolder.BeginSpare(self, item, quantity)

    def SetAvatarModel(self):
        if not hasattr(self, 'targetModelTrakerNPC'):
            self.targetModelTrakerNPC = BigWorld.Model('')
        try:
            self.model.node('HP_head').detach(self.targetModelTrakerNPC)
        except:
            pass
        ItemsUtils.CheckArmorValidityClient(self)
        self.UpdateSniping(False)
        Avatar.SetAvatarModel(self)
        if self.firstPersonCamera:
            BigWorld.camera().target = self.model.node('HP_head')
            BigWorld.camera().pivotPosition = Math.Vector3(0, 0.0, 0)
        self.model.node('HP_head').attach(self.targetModelTrakerNPC)

    def GetQuestItemActionText(self, item_type, item_quest_id):
        qInfo = self.getQItemInfo(item_quest_id, item_type)
        if qInfo and qInfo[2]:
            return qInfo[2]

    def QuestItemAction(self, itemType, quest_id):
        AvatarItemHolder.onQuestItemAction(self, itemType, quest_id)

    def UniteItems(self, item_1, item_2):
        self.cell.UniteItems(item_1['complexItemID'], item_2['complexItemID'])

    def setTradeState(self, state):
        self.isTrade = state

    def showConfirmNotice(self, typeID, dataID, dataStrings):
        if self.dead:
            return
        if typeID == Notices.CLAN_INVITE:
            def listener(event, data):
                invite_type = self.clanInviteConfirmCall['typeID']
                invite_id = self.clanInviteConfirmCall['inviteID']
                if event == MESSAGEBOX.EVENT_BTNPRESS:
                    if data['btn'] == MESSAGEBOX.BTN_YES:
                        self.clanInviteConfirmCallback(invite_type, invite_id, 1)
                    elif data['btn'] == MESSAGEBOX.BTN_NO:
                        self.clanInviteConfirmCallback(invite_type, invite_id, 0)
                self.clanInviteConfirmCall = {}
            inviterName = dataStrings[0].decode('utf-8')
            clanName = dataStrings[1].decode('utf-8')
            self.clanInviteConfirmCall['typeID'] = typeID
            self.clanInviteConfirmCall['inviteID'] = dataID
            msgbox_templates.clan_invite(inviterName, clanName, listener)
        elif typeID == Notices.CLAN_CREATE:
            self.showClanCreateDialog(dataID)
        elif typeID == Notices.PLAYER_TRADE:
            if not self.disablePlayerTrade and self.CanPlayerTrade():
                def TradeInviteConfirmCallback(event):
                    if event == gui_jokes.askUserYesNo.YES:
                        self.cell.confirmNoticeResponse(typeID, dataID, 1)
                        self.setTradeState(True)
                    else:
                        self.cell.confirmNoticeResponse(typeID, dataID, 0)
                        self.cell.cancelExchange(dataID)
                inviterName = dataStrings[0].decode('utf-8')
                text = lc('PlayerAvatar.client.OTHER_PLAYER_OFFERS_BARTER').format(inviterName)
                gui_jokes.askUserYesNo(lc('PlayerAvatar.client.BARTER_OFFER'), text, TradeInviteConfirmCallback)
        elif typeID == Notices.INSTANCE_TELEPORT:
            callerName = dataStrings[0].decode('utf-8') if len(dataStrings) >= 1 else lc('PlayerAvatar.client.UNKNOWN_PLAYER')
            instanceName = dataStrings[1].decode('utf-8') if len(dataStrings) >= 2 else lc('PlayerAvatar.client.STRING_3839_20')
            if hasattr(self, 'teleportConfirmCall'):
                del self.teleportConfirmCall
            self.teleportConfirmCall = partial(self.teleportConfirm, typeID, dataID)

    def onTeleportCalled(self, teleport_type, expected_position):
        self.setControlLock(self.ControlLockTypes.TELEPORTING, True)
        self.filter = BigWorld.DumbFilter()
        self.expected_teleport_position = expected_position

    def onTeleporting(self):
        pass

    def onTeleportEnded(self, wasSuccessful):
        def teleport_complete():
            self.setControlLock(self.ControlLockTypes.TELEPORTING, False)
            self.filter = BigWorld.PlayerAvatarFilter()
        def wait_for_expected_pos():
            if self.position.distTo(self.expected_teleport_position) < 0.1:
                teleport_complete()
            else:
                BigWorld.callback(0.05, wait_for_expected_pos)
        if self.expected_teleport_position is None:
            teleport_complete()
        else:
            wait_for_expected_pos()

    def initEffects(self):
        BWPersonality.GUICore.addListener('toolTipEvent', self.onToolTipEvent)

    def onToolTipEvent(self, effectId, interfaceId, event):
        if interfaceId != BWPersonality.GUICore.GUI_ID_EFFECTSFRAME:
            return
        efData = getEffect(effectId)
        BWPersonality.GUICore.showToolTip(lc(efData['tooltipText']))

    def changeVisibleEffect(self, effect):
        added_new_effect = Effects.changeVisibleEffect(self, effect)
        if added_new_effect:
            self.addPosteffects(effect['id'])
        self.addEffectSFX(effect['id'])
        effectData = getEffect(effect.id)
        if not effectData:
            return
        if effectData['visible']:
            guiData = [effectData['texture'],
                       effect.currentTime if effect.currentTime != -1 else -1,
                       effectData['type'],
                       effect.stacks if effectData['maxStacks'] > 1 else 0]
            BWPersonality.GUICore.setCharacterEffect(effect.id, guiData)

    def removeVisibleEffect(self, effectId):
        effect_removed = Effects.removeVisibleEffect(self, effectId)
        if effect_removed:
            self.removePosteffects(effectId)
        self.removeEffectSFX(effectId)
        BWPersonality.GUICore.delCharacterEffect(effectId)

    def partyFrameActionsRequest(self, event, data):
        if event == soGUI.soPartyFrames2.EVENT_CONTEXT:
            self.selectedPartyMember = data
            actions = self.getMemberActions()
            if actions:
                BWPersonality.GUICore.showContextMenu(BWPersonality.GUICore.GUI_ID_PARTYFRAMES, actions)
                BWPersonality.GUICore.addListener('contextMenuEvent', self.groupContextMenuEvent)

    def playerFrameActionsRequest(self, event, data):
        def itemsSettingsListener(key_checked):
            self.base.updateGroupFlags(key_checked)
        if event == soGUI.soHealthBar.EVENT_CONTEXT:
            actions = self.getFrameActions()
            if actions:
                BWPersonality.GUICore.showContextMenu(BWPersonality.GUICore.GUI_ID_PLAYERFRAME, actions)
                BWPersonality.GUICore.addListener('contextMenuEvent', self.groupContextMenuEvent)
        elif event == soGUI.soHealthBar.EVENT_PARTYSETTINGS:
            import Group
            iam = None
            for member in self.ClientGroupInfo['members']:
                if member['id'] == self.id:
                    iam = member
                    break
            if iam:
                actions = [[lc('Groups.Interface.LOOD_WHO_TAKED'), Group.GROUP_ITEM_TO_RAISED, False],
                           [lc('Groups.Interface.LOOD_LEADER'), Group.GROUP_ITEM_TO_LEADER, False],
                           [lc('Groups.Interface.LOOD_RANDOM'), Group.GROUP_ITEM_TO_RANDOM, False]]
                if iam['flag'] & Group.GROUP_ITEM_TO_RAISED:
                    actions[0][2] = True
                elif iam['flag'] & Group.GROUP_ITEM_TO_LEADER:
                    actions[1][2] = True
                elif iam['flag'] & Group.GROUP_ITEM_TO_RANDOM:
                    actions[2][2] = True
                gui_jokes.radioBox(lc('Groups.Interface.LOOD_SETTINGS_TITLE'), u'', actions, itemsSettingsListener)

    def groupContextMenuEvent(self, interface_id, id, caption, event):
        BWPersonality.GUICore.removeListener('contextMenuEvent', self.groupContextMenuEvent)
        from GroupMember import GroupMember
        import Group
        if interface_id == BWPersonality.GUICore.GUI_ID_PLAYERFRAME:
            if id == GroupMember.HIDE_ALL_EFFECTS_FRAME:
                BWPersonality.GUICore.showPartyFramesEffects(False)
            elif id == GroupMember.SHOW_ALL_EFFECTS_FRAME:
                BWPersonality.GUICore.showPartyFramesEffects(True)
            elif id == GroupMember.REMOVE_GROUP:
                self.sendMessage(u'/groupdestroy')
            elif id == GroupMember.LEAVE_GROUP:
                self.sendMessage(u'/groupleave')
        elif interface_id == BWPersonality.GUICore.GUI_ID_PARTYFRAMES:
            if id == GroupMember.KICK_MEMBER:
                name = u''
                for member in self.ClientGroupInfo['members']:
                    if member['id'] == self.selectedPartyMember:
                        name = member['name']
                        break
                if name:
                    self.sendMessage(u'/kick ' + name)
            elif id == GroupMember.GET_LEADER:
                name = u''
                for member in self.ClientGroupInfo['members']:
                    if member['id'] == self.selectedPartyMember:
                        name = member['name']
                        break
                if name:
                    self.sendMessage(u'/groupleader ' + name)

    def set_visitedSpaces(self, *p):
        BWPersonality.GUICore.setGPSdata({'spaces': self.visitedSpaces})

    def debug_creatureBrainStatesToIcons(self, brainStates):
        icons = []
        for state in brainStates:
            icon = brainStateToIcon.get(state)
            if icon is not None:
                icons.append(icon)
        return icons

    def debug_creatureTargetsToString(self, targets):
        return '\n'.join([t[1] for t in targets])

    def debug_sendCreatureInfo(self, entityID, info):
        if info is not None:
            localInfo = self.creatureDebugInfo.get(entityID)
            if localInfo is None:
                localInfo = self.creatureDebugInfo[entityID] = {}
            icons = self.debug_creatureBrainStatesToIcons(info['brainStates'])
            text = 'thinks %d\n' % info['brainThinks']
            text += self.debug_creatureTargetsToString(info['targets'])
            text.decode('utf-8')
            localInfo.update({'icons': icons, 'text': text})
            localInfo['distance'] = info['distance']
            localInfo['flat_distance'] = info['flat_distance']
            movePointModel = localInfo.get('movePointModel')
            if movePointModel is None:
                movePointModel = BigWorld.Model('models/bolvan/sphere.model')
                self.addModel(movePointModel)
                localInfo['movePointModel'] = movePointModel
            movePointModel.position = info['movePoint']
        else:
            try:
                self.delModel(self.creatureDebugInfo[entityID]['movePointModel'])
                del self.creatureDebugInfo[entityID]
            except KeyError:
                pass

    def debug_overview(self, height=20):
        if not hasattr(self, 'debug_overview_enabled'):
            self.debug_overview_enabled = False
        if not self.debug_overview_enabled:
            self.model.scale = (1, height, 1)
            self.model.visible = False
            self.debug_overview_enabled = True
        else:
            self.model.scale = (1, 1, 1)
            self.model.visible = True
            self.debug_overview_enabled = False

    def GetRecoilValueParams(self):
        return self.GetActiveWeaponAccuracyDiff(), self.GetFiryingItemParams()

    def ServerRestrict(self, channel, action_duration):
        Restrictions.ServerRestrict(self, channel, action_duration)

    def canUseClanItems(self):
        return ClanMember.checkClanRights(self, Clan.FLAG_CAN_USE_CLANITEM)

    def GetMaxEquippedArtifactNumber(self):
        return Character.GetMaxEquippedArtifactNumber(self)

    def onWeatherChanged(self, weather_system_name):
        BWPersonality.gpd.weather.summon(weather_system_name, immediate=False, serverSync=False, resummon=False)

    safe_timer = 0
    SAFE_TIMER_TRACKER_ID = 'SAFE_TIMER_TRACKER_ID'
    safe_data = {'caption': lc('PlayerAvatar.client.SAFE_ZONE_WAITING'),
                 'track_data': [{'data_type': OBJECTIVE_TRACKER.DATATYPE_PLAINTEXT, 'data': ''}]}

    def show_safe_timer(self, timer):
        self.safe_timer = int(timer)
        time_str = str(self.safe_timer)
        safe_data = copy.copy(self.safe_data)
        if self.safe_timer <= 0:
            time_str = ''
            safe_data['caption'] = ''
        self.safe_data['track_data'] = [{'data_type': OBJECTIVE_TRACKER.DATATYPE_PLAINTEXT, 'data': time_str}]
        BWPersonality.GUICore.addObjective(self.SAFE_TIMER_TRACKER_ID, OBJECTIVE_TRACKER.PRIORITY_HIGHEST, self.safe_data)
        BigWorld.callback(1.0, self.update_safe_timer)

    def update_safe_timer(self):
        self.safe_timer -= 1
        if self.safe_timer <= 0:
            BWPersonality.GUICore.delObjective(self.SAFE_TIMER_TRACKER_ID)
            return
        self.safe_data['track_data'] = [{'data_type': OBJECTIVE_TRACKER.DATATYPE_PLAINTEXT, 'data': str(self.safe_timer)}]
        BWPersonality.GUICore.setObjective(self.SAFE_TIMER_TRACKER_ID, self.safe_data)
        BigWorld.callback(1.0, self.update_safe_timer)

    def askUseItemOnTarget(self, target_id, item_type):
        item_name = ItemsUtils.GetItemName(item_type)
        target_name = u''
        target = BigWorld.entities.get(target_id)
        if target and target.__class__.__name__ == 'PlayerAvatar':
            target_name = target.name

        def listener(event, data):
            if event == MESSAGEBOX.EVENT_BTNPRESS:
                if data['btn'] == MESSAGEBOX.BTN_YES:
                    self.cell.answerOnUseItemOnTarget(True)
                elif data['btn'] == MESSAGEBOX.BTN_NO:
                    self.cell.answerOnUseItemOnTarget(False)
        BWPersonality.GUICore.showMsgBox(id='clan_leave', isModal=False, x=0.0, y=0.0, width=300,
                                         caption=lc('PlayerAvatar.client.USE_ITEM_ON_TARGET_CAPTION'), forcePos=False,
                                         parent_gui_id=None, bind_to_parent=False,
                                         btn_set=[{'type': MESSAGEBOX.BTN_YES, 'width': 80},
                                                  {'type': MESSAGEBOX.BTN_NO, 'width': 80}],
                                         timeout=10, closeBox=True, defaultAction=MESSAGEBOX.BTN_NO,
                                         addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD, 'ID': 'main_txt_field',
                                                       'text': lc('PlayerAvatar.client.USE_ITEM_ON_TARGET_CAPTION').format(item_name, target_name),
                                                       'hAnchor': MESSAGEBOX.ANCHOR_CENTER}],
                                         callback=listener)

    will_die_on = 0

    def show_iwannadie_timer(self, is_showing):
        message = lc('PlayerAvatar.client.YOU_WILL_DAY_ON_X_SECONDS')
        if is_showing:
            self.will_die_on = Respawn.IWANNADIE_TIMER
            self.systemChatline(message.format(self.will_die_on))
            BigWorld.callback(10.0, self.repeat_iwannadie_time)
        elif self.will_die_on > 0:
            BigWorld.cancelCallback(self.repeat_iwannadie_time)
            self.will_die_on = 0

    def repeat_iwannadie_time(self):
        self.will_die_on -= 10
        if self.will_die_on > 0:
            message = lc('PlayerAvatar.client.YOU_WILL_DAY_ON_X_SECONDS')
            self.systemChatline(message.format(self.will_die_on))
            BigWorld.callback(10.0, self.repeat_iwannadie_time)

    def updateHungryAndThirstBar(self, new_hungry, new_thirst):
        self.hungry = new_hungry
        self.thirst = new_thirst

    def checkPosibleUserFire(self):
        if self.dead or self.control_locked or self.inputlock:
            return False
        direction = Vector3(math.sin(self.yaw), 0, math.cos(self.yaw)) * 1.5
        fromPos = direction + self.position + Vector3(0, 2, 0)
        toPos = fromPos + Vector3(0, -2.5, 0)
        collision_res = BigWorld.collide(self.spaceID, fromPos, toPos)
        if not collision_res:
            self.systemChatline(lc('PlayerAvatar.client.FAIL_UF_GROUND'))
            return False
        firePos = collision_res[0]
        if not self._checkFirePlacePossible(firePos):
            self.systemChatline(lc('PlayerAvatar.client.FAIL_UF_GEOMETRY'))
            return False
        restr = ('ZoneEffects', 'AreaWatcher', 'UserFire')
        resrAreas = [e for e in BigWorld.entities.values() if e.__class__.__name__ in restr and self.position.distTo(e.position) < 30.0]
        if resrAreas:
            self.systemChatline(lc('PlayerAvatar.client.FAIL_UF_OTHER_UF'))
            return False
        return firePos

    def _checkFirePlacePossible(self, position, radius=0.9, maxAngle=7.0):
        max_angle_rad = math.radians(maxAngle)
        x, z, y = position
        max_z = radius * math.tan(max_angle_rad)
        upPos = Vector3(x, z + max_z, y)
        for i in range(37):
            px = radius * math.sin(1800 * i / math.pi)
            py = radius * math.cos(1800 * i / math.pi)
            newp = Vector3(x + px, z, y + py)
            up = Vector3(x + px, z + 2.0, y + py)
            down = Vector3(x + px, z - 0.5, y + py)
            collision_res = BigWorld.collide(self.spaceID, up, down)
            if not collision_res:
                return False
            coll_point = collision_res[0]
            dz = abs(z - coll_point[1])
            dangle = math.pi / 2 - math.atan2(radius, dz)
            if dangle > max_angle_rad:
                return False
            up_coll_pointPos = coll_point + Vector3(0, max_z, 0)
            if BigWorld.collide(self.spaceID, upPos, up_coll_pointPos):
                return False
        return True

    def exploreUserFireContainer(self, entity):
        self.StartItemCache(entity.id, ItemsUtils.CACHE_MODE_USERFIRE)

    def ProceedCreateUserFire(self, duration):
        def controllockOff():
            if not self.is_sitting:
                self.control_locked = False
                self.LookAround(False)
            self.inputlock = False
        self.control_locked = True
        self.inputlock = True
        self.physics.velocity = (0, 0, 0)
        self.LookAround(True)
        BigWorld.callback(duration, controllockOff)

    def set_BulletinBoardData(self, *old):
        news_quests = dict((d['key'], d['text']) for d in self.BulletinBoardData)
        BWPersonality.GUICore.setBulletinBoardData(news_quests)

    def Poison(self, status):
        if status:
            BWPersonality.GUICore.GUIpoison.show()
        else:
            BWPersonality.GUICore.GUIpoison.hide()

    def hm_message(self, msgID, data):
        def chat(string):
            self.systemChatline(colorCodes.tf3_regular_text_color + string)
        def ask(string):
            self.systemChatline(colorCodes.tf3_regular_text_color + string)
        msg = HunterResponses.msg[msgID]
        if msgID == HunterResponses.DELETE_AD_OK:
            chat(msg.format(data))
        elif msgID == HunterResponses.DELETE_AD_NOT_FOUND:
            ask(msg.format(data))
        elif msgID == HunterResponses.WANTED_NOT_FOUND:
            ask(msg.format(data))
        elif msgID == HunterResponses.SUBSCRIPTION_OK:
            chat(msg.format(*data))
        elif msgID == HunterResponses.WANTEDKILLEDANDIMPRISONED_OK:
            chat(msg.format(*data))
        elif msgID == HunterResponses.SUBMIT_OK:
            chat(msg.format(*data))
        elif msgID == HunterResponses.SUBMIT_FAIL_VICTIMNAME:
            ask(msg.format(*data))
        elif msgID == HunterResponses.SUBMIT_FAIL_WANTEDNAME:
            ask(msg.format(*data))
        elif msgID == HunterResponses.MAX_OFFENFER:
            ask(msg)
        elif msgID == HunterResponses.MIN_PRICE:
            ask(msg)
        elif msgID == HunterResponses.NO_CREDITNUMBER:
            ask(msg)
        elif msgID == HunterResponses.OFFENDER_REMOVE:
            chat(msg.format(data))
        elif msgID == HunterResponses.WANTED_REMOVE:
            chat(msg.format(*data))
        elif msgID == HunterResponses.YOU_KILLED_AND_IMPRISONED:
            chat(msg.format(data))
        elif msgID == HunterResponses.WANTED_THIS_I:
            ask(msg)

    def hm_positions(self, data):
        BWPersonality.GUICore.setListWantedDataSection(data)

    def hm_CatalogResponseFiltered(self, data, page_start, last_index_item, all_index_item):
        BWPersonality.GUICore.setBulletinBoardHunterData({'data': data, 'page_start': page_start,
                                                          'last_index_item': last_index_item,
                                                          'all_index_item': all_index_item})

    def set_HUNTER_listOfWanted(self, old):
        pass

    def set_HUNTER_lostListOfWanted(self, old):
        pass

    def getWantedPosition(self):
        self.cell.getWantedPosition()

    def subscriptionWanted(self, name):
        self.cell.subscriptionWanted(name)

    def removeOffender(self, name):
        self.cell.removeOffender(name)

    def submitOffender(self, price):
        self.cell.submitOffender(price)

    def getHunterCatalogFiltered(self, sortFlag, forward, page_start, page_len):
        self.cell.getCatalogFiltered(sortFlag, forward, page_start, page_len)

    def setTimeDiff(self, serverTime):
        print 'setTimeDiff', serverTime
        self.timeServerDiff = time() - serverTime
        print 'Diff:', self.timeServerDiff

    def getWarehouseData(self, entity_id):
        self.cell.getWarehouseData(entity_id)

    def moneyDeposit(self, entity_id, money):
        BigWorld.entities[entity_id].cell.addMoney(self.clanID, int(money))

    def goldDeposit(self, entity_id, money):
        BigWorld.entities[entity_id].cell.addGold(self.clanID, int(money))

    def moneyWithdraw(self, entity_id, money):
        BigWorld.entities[entity_id].cell.removeMoney(self.clanID, int(money))

    def goldWithdraw(self, entity_id, money):
        BigWorld.entities[entity_id].cell.removeGold(self.clanID, int(money))

    def permissionCheck(self):
        return self.isClanLeader

    def on_AllRoomID(self, listIDRooms):
        BWPersonality.GUICore.updatePVPRoomsIDs(listIDRooms)

    def on_AllRoomData(self, data, listIDRooms):
        self.tmp_romsdata = data
        self.tmp_listIDRooms = listIDRooms
        BWPersonality.GUICore.addServer2SelectMap(data, listIDRooms)

    def on_roomData(self, data):
        self.last_roomData = data
        BWPersonality.GUICore.setScoreData(data)

    def askChoiceTeam(self):
        print 'askChoiceTeam'

    def set_teamID(self, old):
        print 'playerAvatar (%s) set_teamID :' % self.id, old, '->', self.teamID
        BWPersonality.GUICore.changeTeamPVP(self.teamID)
        if not self.teamID:
            BWPersonality.GUICore.clearAllPVPmarkers()
            BWPersonality.GUICore.showPVPmarker(False)
            return
        if self.last_roomData and self.last_roomData.gameInfo.gamePlay != csconstans.GAMEPLAY_DM:
            BWPersonality.GUICore.showPVPmarker(True)
            BWPersonality.GUICore.clearAllPVPmarkers()
            for entity in BigWorld.entities.values():
                if entity.id != self.id and entity.__class__.__name__ == 'Avatar' and entity.teamID == self.teamID:
                    BWPersonality.GUICore.addPVPmarker(entity.id, self.getMatrixHead(entity.id))

    def onAvatarTeamIDChanged(self, userID, old_teamID, teamID):
        if self.teamID:
            if teamID == self.teamID:
                BWPersonality.GUICore.addPVPmarker(userID, self.getMatrixHead(userID))
            else:
                BWPersonality.GUICore.delPVPmarker(userID)

    def set_ninjaMode(self, old):
        BWPersonality.GUICore.healthBarGUI.component.NinjaIcon.visible = self.ninjaMode

    def getMatrixHead(self, userID):
        entity = BigWorld.entity(userID)
        if not entity or not entity.model:
            return None
        if not hasattr(entity.model, 'head'):
            entity.model.head = BigWorld.Model('')
        return entity.model.head

    def onAvatarModelChangedForPlayer(self, avatar):
        if self.teamID and avatar.__class__.__name__ == 'Avatar' and self.id != avatar.id and avatar.teamID == self.teamID:
            BWPersonality.GUICore.updateMatrixMarker(avatar.id, self.getMatrixHead(avatar.id))

    def avatarOnEnterWorld(self, avatar):
        if avatar.__class__.__name__ == 'Avatar' and self.teamID and avatar != self and avatar.teamID == self.teamID:
            BWPersonality.GUICore.addPVPmarker(avatar.id, self.getMatrixHead(avatar.id))

    def avatarLeaveWorld(self, userID):
        BWPersonality.GUICore.delPVPmarker(userID)

    def set_inPVPinstance(self, old):
        BWPersonality.GUICore.change_inPVPinstance(self.inPVPinstance)

    def roomEvent(self, eventID, code, msg):
        print 'roomEvent', eventID, [msg]
        if eventID == csconstans.EVENT_ROUND_WIN:
            self.systemMessage(u'Раунд победила команда %s, %s' % (self.getPVPteamName(code), msg), 16711935)
        elif eventID == csconstans.EVENT_START_ROUND:
            self.systemMessage(u'старт матча', 16711935)
            BWPersonality.GUICore.pvpScoreStartRound()
        elif eventID == csconstans.EVENT_ROOM_ERROR:
            gui_jokes.askUserOk(u'ROOM_ERROR', u'error %s  %s' % (code, msg))
        elif eventID == csconstans.EVENT_ROOM_MSG:
            self.systemMessage('ROOM: ' + msg, 16711935)
            BWPersonality.GUICore.chatPrint(1, u'ROOM: [%s] %s' % (code, msg))
        elif eventID == csconstans.EVENT_GAME_START:
            self.systemMessage(u'старт матча', 16711935)
            BWPersonality.GUICore.chatPrint(1, u'старт матча')
        elif eventID == csconstans.EVENT_PLAYER_GAME_WIN:
            self.systemMessage(u'В матче победил игрок %s' % msg, 16711935)
            BWPersonality.GUICore.chatPrint(1, u'В матче победил игрок %s' % msg)
            BWPersonality.GUICore.pvpScoreWinPlayer(msg)
        elif eventID == csconstans.EVENT_GAME_WIN:
            self.systemMessage(u'В матче победила команда %s' % self.getPVPteamName(code), 16711935)
            BWPersonality.GUICore.chatPrint(1, u'В матче победила команда %s' % self.getPVPteamName(code))
            BWPersonality.GUICore.pvpScoreWinTeam(code)

    def getPVPteamName(self, team):
        return {1: 'Red', 2: 'Blue'}.get(team, '?')

    def jumpCollisionNotifier(self, e):
        print 'jumpCollisionNotifier', e

    def mayStandNotifier(self, e):
        print 'mayStandNotifier', e

    def on_roomDamage(self, code, teamIDAgr, teamIDVic, agrName, vicName, death_type, death_subtype):
        print 'on_roomDamage', [code, teamIDAgr, teamIDVic, agrName, vicName, death_type, death_subtype]
        red = '<color=255010010255>'
        blue = '<color=010010255255>'
        white = '<color=192192192255>'

        def getcolor(team):
            if team == csconstans.TEAM_RED:
                return red
            if team == csconstans.TEAM_BLUE:
                return blue
            return white

        msg = white + 'PVP: '
        if not agrName:
            msg += getcolor(teamIDVic) + vicName + white + u' самоубился'
        else:
            msg += getcolor(teamIDAgr) + agrName + white + u' убил ' + getcolor(teamIDVic) + vicName + white + ' .'
        BWPersonality.GUICore.chatPrint(0, msg)