# Embedded file name: scripts/client/StalkerModel.py
import BigWorld
import ItemsUtils
from Items import ItemsCatalog
import AnimationCaps
import traceback

def set_model_due_to_inventory(entity, default_models):
    """
    \xd0\x98\xd0\xa1\xd0\x9f\xd0\xa0\xd0\x90\xd0\x92\xd0\x9b\xd0\x95\xd0\x9d\xd0\x9d\xd0\x90\xd0\xaf \xd0\x92\xd0\x95\xd0\xa0\xd0\xa1\xd0\x98\xd0\xaf: \xd0\xa3\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb0 \xd0\xbe\xd1\x88\xd0\xb8\xd0\xb1\xd0\xba\xd0\xb0 \xd1\x81 tint_cap
    
    \xd0\x92\xd0\xbe\xd0\xb7\xd0\xb2\xd1\x80\xd0\xb0\xd1\x89\xd0\xb0\xd0\xb5\xd1\x82:
    - model_set: \xd0\xbd\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x80 \xd0\xbc\xd0\xbe\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xb9 \xd0\xbf\xd0\xb5\xd1\x80\xd1\x81\xd0\xbe\xd0\xbd\xd0\xb0\xd0\xb6\xd0\xb0
    - head_attachments: \xd0\xb0\xd1\x82\xd1\x82\xd0\xb0\xd1\x87\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd1\x8b \xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd1\x8b
    - back_pack_attachments: \xd0\xb0\xd1\x82\xd1\x82\xd0\xb0\xd1\x87\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd1\x8b \xd1\x80\xd1\x8e\xd0\xba\xd0\xb7\xd0\xb0\xd0\xba\xd0\xb0
    - weapon_back_attachments: \xd0\xbe\xd1\x80\xd1\x83\xd0\xb6\xd0\xb8\xd0\xb5 \xd0\xbd\xd0\xb0 \xd1\x81\xd0\xbf\xd0\xb8\xd0\xbd\xd0\xb5
    - weapon_pistol_attachments: \xd0\xbf\xd0\xb8\xd1\x81\xd1\x82\xd0\xbe\xd0\xbb\xd0\xb5\xd1\x82
    - model_tints_dict: \xd1\x81\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x80\xd1\x8c \xd1\x82\xd0\xb8\xd0\xbd\xd1\x82\xd0\xbe\xd0\xb2 \xd0\xbc\xd0\xbe\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb8
    - head_tints_dict: \xd1\x81\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x80\xd1\x8c \xd1\x82\xd0\xb8\xd0\xbd\xd1\x82\xd0\xbe\xd0\xb2 \xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd1\x8b
    - backback_tints_dict: \xd1\x81\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x80\xd1\x8c \xd1\x82\xd0\xb8\xd0\xbd\xd1\x82\xd0\xbe\xd0\xb2 \xd1\x80\xd1\x8e\xd0\xba\xd0\xb7\xd0\xb0\xd0\xba\xd0\xb0
    """
    try:
        model_set = []
        model_tints_dict = {}
        head_tints_dict = {}
        backback_tints_dict = {}
        armor_parts = [('HeadID', ItemsCatalog.HEAD),
         ('BodyID', ItemsCatalog.SHIRT),
         ('HandsID', ItemsCatalog.HANDS),
         ('PantsID', ItemsCatalog.PANTS),
         ('BootsID', ItemsCatalog.BOOTS)]
        for slot_name, item_class in armor_parts:
            item_id = getattr(entity.ActiveArmorSet, slot_name, 0)
            if item_id > 0:
                item = ItemsUtils.GetComplexItemByID(entity, item_id)
                if item:
                    item_type = item.get('complexItemType', 0)
                    item_params = ItemsCatalog.GetItemParam(item_type)
                    if item_params and 'ModelNames' in item_params:
                        model_names = item_params['ModelNames']
                        if model_names:
                            model_path = model_names.values()[0] if isinstance(model_names, dict) else model_names
                            model_set.append(model_path)
                            if 'Tint' in item_params:
                                tint_data = item_params['Tint']
                                if item_class == ItemsCatalog.HEAD:
                                    head_tints_dict.update(tint_data)
                                else:
                                    model_tints_dict.update(tint_data)
            elif item_class in default_models:
                default_path = default_models[item_class]
                model_set.append(default_path)

        head_attachments = []
        head_attach_slots = [('HelmetID', 'HP_helmet'), ('GlassesID', 'HP_glasses'), ('MaskID', 'HP_mask')]
        for slot_name, hardpoint in head_attach_slots:
            item_id = getattr(entity.ActiveArmorSet, slot_name, 0)
            if item_id > 0:
                item = ItemsUtils.GetComplexItemByID(entity, item_id)
                if item:
                    item_params = ItemsCatalog.GetItemParam(item['complexItemType'])
                    if item_params and 'ModelNames' in item_params:
                        model_names = item_params['ModelNames']
                        if model_names:
                            model_path = model_names.values()[0] if isinstance(model_names, dict) else model_names
                            head_attachments.append((model_path, hardpoint))

        back_pack_attachments = []
        backpack_id = getattr(entity.ActiveArmorSet, 'BackPackID', 0)
        if backpack_id > 0:
            item = ItemsUtils.GetComplexItemByID(entity, backpack_id)
            if item:
                item_params = ItemsCatalog.GetItemParam(item['complexItemType'])
                if item_params and 'ModelNames' in item_params:
                    model_names = item_params['ModelNames']
                    if model_names:
                        model_path = model_names.values()[0] if isinstance(model_names, dict) else model_names
                        back_pack_attachments.append((model_path, 'HP_backpack'))
                        if 'Tint' in item_params:
                            backback_tints_dict.update(item_params['Tint'])
        weapon_back_attachments = {}
        primary_weapon_id = getattr(entity.ActiveWeaponSet, 'PrimarySlotID', 0)
        if primary_weapon_id > 0 and primary_weapon_id != entity.ActiveItemID:
            weapon_models = entity.GetEquippedItemModels(ItemsCatalog.PRIMARY)
            if weapon_models:
                weapon_back_attachments = weapon_models
        weapon_pistol_attachments = {}
        secondary_weapon_id = getattr(entity.ActiveWeaponSet, 'SecondarySlotID', 0)
        if secondary_weapon_id > 0 and secondary_weapon_id != entity.ActiveItemID:
            pistol_models = entity.GetEquippedItemModels(ItemsCatalog.SECONDARY)
            if pistol_models:
                weapon_pistol_attachments = pistol_models
        return (model_set,
         head_attachments,
         back_pack_attachments,
         weapon_back_attachments,
         weapon_pistol_attachments,
         model_tints_dict,
         head_tints_dict,
         backback_tints_dict)
    except Exception as e:
        print '[StalkerModel] Error in set_model_due_to_inventory:', e
        traceback.print_exc()
        return ([],
         [],
         [],
         {},
         {},
         {},
         {},
         {})


def ComposePlayerModel(entity):
    """
    \xd0\x98\xd0\xa1\xd0\x9f\xd0\xa0\xd0\x90\xd0\x92\xd0\x9b\xd0\x95\xd0\x9d\xd0\x9d\xd0\x90\xd0\xaf \xd0\x92\xd0\x95\xd0\xa0\xd0\xa1\xd0\x98\xd0\xaf: \xd0\xa1\xd0\xbe\xd0\xb7\xd0\xb4\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x84\xd0\xb8\xd0\xbd\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe\xd0\xb9 \xd0\xbc\xd0\xbe\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb8 \xd0\xb8\xd0\xb3\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0
    \xd0\xa3\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb0 \xd0\xbe\xd1\x88\xd0\xb8\xd0\xb1\xd0\xba\xd0\xb0 \xd0\xbf\xd1\x80\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x82\xd0\xb8\xd0\xbd\xd1\x82\xd0\xbe\xd0\xb2
    """
    try:
        model_set, head_attachments, back_pack_attachments, weapon_back_attachments, weapon_pistol_attachments, model_tints_dict, head_tints_dict, backback_tints_dict = set_model_due_to_inventory(entity, entity.getDefaultModels())
        if not model_set:
            print '[StalkerModel] WARNING: Empty model_set, using default'
            model_set = ['models/characters/default_body.model']
        final_model = BigWorld.Model(model_set[0])
        for i, model_path in enumerate(model_set[1:], 1):
            try:
                part_model = BigWorld.Model(model_path)
            except Exception as e:
                print '[StalkerModel] Error loading body part %s: %s' % (model_path, e)

        for tint_key, tint_value in model_tints_dict.items():
            if hasattr(final_model, tint_key):
                try:
                    setattr(final_model, tint_key, tint_value)
                except Exception as e:
                    print '[StalkerModel] WARNING: Cannot set tint %s = %s' % (tint_key, tint_value)

            else:
                print "[StalkerModel] INFO: Model has no attribute '%s', skipping tint" % tint_key

        for head_model_path, hardpoint in head_attachments:
            try:
                head_model = BigWorld.Model(head_model_path)
                for tint_key, tint_value in head_tints_dict.items():
                    if hasattr(head_model, tint_key):
                        setattr(head_model, tint_key, tint_value)

                if hasattr(final_model, hardpoint):
                    node = getattr(final_model, hardpoint)
                    node.attach(head_model)
            except Exception as e:
                print '[StalkerModel] Error attaching head part %s: %s' % (head_model_path, e)

        for backpack_model_path, hardpoint in back_pack_attachments:
            try:
                backpack_model = BigWorld.Model(backpack_model_path)
                for tint_key, tint_value in backback_tints_dict.items():
                    if hasattr(backpack_model, tint_key):
                        setattr(backpack_model, tint_key, tint_value)

                if hasattr(final_model, hardpoint):
                    node = getattr(final_model, hardpoint)
                    node.attach(backpack_model)
            except Exception as e:
                print '[StalkerModel] Error attaching backpack %s: %s' % (backpack_model_path, e)

        if weapon_back_attachments:
            try:
                weapon_model = entity.getModelByNamesDict(weapon_back_attachments)
                if weapon_model and hasattr(final_model, 'HP_weapon_back'):
                    final_model.HP_weapon_back.attach(weapon_model)
            except Exception as e:
                print '[StalkerModel] Error attaching back weapon:', e

        if weapon_pistol_attachments:
            try:
                pistol_model = entity.getModelByNamesDict(weapon_pistol_attachments)
                if pistol_model and hasattr(final_model, 'HP_pistol_holster'):
                    final_model.HP_pistol_holster.attach(pistol_model)
            except Exception as e:
                print '[StalkerModel] Error attaching pistol:', e

        AnimationCaps.setCapsList(final_model, entity.getAvatarAnimationCaps())
        return final_model
    except Exception as e:
        print '[StalkerModel] CRITICAL ERROR in ComposePlayerModel:', e
        traceback.print_exc()
        return BigWorld.Model('models/characters/emergency_model.model')


def ApplyTintSafely(model, tint_dict):
    """
    \xd0\x91\xd0\xb5\xd0\xb7\xd0\xbe\xd0\xbf\xd0\xb0\xd1\x81\xd0\xbd\xd0\xbe\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x82\xd0\xb8\xd0\xbd\xd1\x82\xd0\xbe\xd0\xb2 \xd0\xba \xd0\xbc\xd0\xbe\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb8
    \xd0\x9f\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd1\x80\xd1\x8f\xd0\xb5\xd1\x82 \xd0\xbd\xd0\xb0\xd0\xbb\xd0\xb8\xd1\x87\xd0\xb8\xd0\xb5 \xd0\xb0\xd1\x82\xd1\x80\xd0\xb8\xd0\xb1\xd1\x83\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xb5\xd1\x80\xd0\xb5\xd0\xb4 \xd1\x83\xd1\x81\xd1\x82\xd0\xb0\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xba\xd0\xbe\xd0\xb9
    """
    applied = []
    failed = []
    for tint_key, tint_value in tint_dict.items():
        if hasattr(model, tint_key):
            try:
                setattr(model, tint_key, tint_value)
                applied.append(tint_key)
            except Exception as e:
                failed.append((tint_key, str(e)))

        else:
            failed.append((tint_key, 'Attribute not found'))

    return (applied, failed)


def GetModelHardpoints(model):
    """
    \xd0\x9f\xd0\xbe\xd0\xbb\xd1\x83\xd1\x87\xd0\xb8\xd1\x82\xd1\x8c \xd1\x81\xd0\xbf\xd0\xb8\xd1\x81\xd0\xbe\xd0\xba \xd0\xb2\xd1\x81\xd0\xb5\xd1\x85 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xbd\xd1\x8b\xd1\x85 \xd1\x85\xd0\xb0\xd1\x80\xd0\xb4\xd0\xbf\xd0\xbe\xd0\xb8\xd0\xbd\xd1\x82\xd0\xbe\xd0\xb2 \xd0\xbc\xd0\xbe\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb8
    \xd0\x9f\xd0\xbe\xd0\xbb\xd0\xb5\xd0\xb7\xd0\xbd\xd0\xbe \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xbe\xd1\x82\xd0\xbb\xd0\xb0\xd0\xb4\xd0\xba\xd0\xb8
    """
    hardpoints = []
    try:
        for attr_name in dir(model):
            if attr_name.startswith('HP_'):
                hardpoints.append(attr_name)

    except:
        pass

    return hardpoints


def PrintModelDebugInfo(model):
    """
    \xd0\x92\xd1\x8b\xd0\xb2\xd0\xb5\xd1\x81\xd1\x82\xd0\xb8 \xd0\xbe\xd1\x82\xd0\xbb\xd0\xb0\xd0\xb4\xd0\xbe\xd1\x87\xd0\xbd\xd1\x83\xd1\x8e \xd0\xb8\xd0\xbd\xd1\x84\xd0\xbe\xd1\x80\xd0\xbc\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8e \xd0\xbe \xd0\xbc\xd0\xbe\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb8
    """
    print '=' * 60
    print '[StalkerModel] Model Debug Info:'
    print '  Model:', model
    print '  Hardpoints:', GetModelHardpoints(model)
    standard_attrs = ['tint_weapon', 'tint_armor', 'tint_clothes']
    for attr in standard_attrs:
        has_attr = hasattr(model, attr)
        print '  %s: %s' % (attr, 'YES' if has_attr else 'NO')

    print '=' * 60