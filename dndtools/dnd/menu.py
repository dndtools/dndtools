# -*- coding: utf-8 -*-


class MenuItem:
    def __init__(self):
        pass

    RULEBOOKS = "rulebooks"

    class Rulebooks:
        def __init__(self):
            pass

        RULEBOOKS = "rulebooks"
        EDITIONS = "editions"
        CORE_3_5 = "core_3_5"
        SUPPLEMENTS_3_5 = "supplements_3_5"
        DRAGONLANCE_3_5 = "dragonlance_3_5"
        EBERRON_3_5 = "eberron_3_5"
        FORGOTTEN_REALMS_3_5 = "forgotten_realms_3_5"
        BOOKS_3_0 = "books_3_0"
        RULES = "rules"

    CHARACTER_OPTIONS = "character_options"

    class CharacterOptions:
        def __init__(self):
            pass

        CLASSES = "classes"
        FEATS = "feats"
        FEAT_CATEGORIES = "feat_categories"
        SKILLS = "skills"
        SKILL_TRICKS = "skill_tricks"
        TRAITS = "traits"
        FLAWS = "flaws"
        DEITIES = "deities"
        LANGUAGES = "languages"

    MAGIC = "magic"

    class Magic:
        def __init__(self):
            pass

        SPELLS = "spells"
        SCHOOLS = "schools"
        DESCRIPTORS = "descriptors"
        SHADOW_CASTING = "shadow_casting"
        INVOCATIONS = "invocations"
        PSIONICS = "psionics"
        AURAS = "auras"
        MANEUVERS = "maneuvers"
        DOMAINS = "domains"

    BESTIARY = "bestiary"

    class Bestiary:
        def __init__(self):
            pass

        RACES = "races"
        RACE_TYPES = "race_types"
        MONSTERS = "monsters"
        MONSTROUS_TYPES = "monstrous_types"
        MONSTROUS_TRAITS = "monstrous_traits"
        TEMPLATES = "templates"


    ITEMS = "items"

    class Items:
        def __init__(self):
            pass

        MAGICAL = "magical"
        MUNDANE_ALCHEMICAL = "mundane_alchemical"

    CONTACTS = "contacts"

    class Contacts:
        def __init__(self):
            pass

        NEWS = "news"
        CONTACT_US = "contact_us"
        STAFF = "staff"

    ANDROID = "android"

    class Android:
        def __init__(self):
            pass


def menu_item(menu_item_name):
    def menu_item_generator(old_function):
        def new_function(*args, **kwargs):
            if 'request' in kwargs:
                kwargs['request'].menu_item = menu_item_name
            else:
                args[0].menu_item = menu_item_name

            return old_function(*args, **kwargs)

        return new_function

    return menu_item_generator


def submenu_item(menu_item_name):
    def submenu_item_generator(old_function):
        def new_function(*args, **kwargs):
            if 'request' in kwargs:
                kwargs['request'].submenu_item = menu_item_name
            else:
                args[0].submenu_item = menu_item_name

            return old_function(*args, **kwargs)

        return new_function

    return submenu_item_generator