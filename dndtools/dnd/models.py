# -*- coding: utf-8 -*-

from PIL import Image
from django.db import models

from dndtools.dnd.utilities import update_html_cache_attributes


class DndEdition(models.Model):
    name = models.CharField(
        max_length=32,
        db_index=True,
    )
    system = models.CharField(
        max_length=16,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
    )
    core = models.BooleanField()

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.edition_detail', (),
            {
                'edition_slug': self.slug,
                'edition_id': self.id,
            }
        )


class Rulebook(models.Model):
    dnd_edition = models.ForeignKey(
        DndEdition,
    )
    name = models.CharField(
        max_length=128,
        db_index=True,
    )
    abbr = models.CharField(
        max_length=7,
    )
    description = models.TextField(
        blank=True,
    )
    year = models.CharField(
        max_length=4,
        null=True,
        blank=True,
    )
    published = models.DateField(
        null=True,
        blank=True,
        help_text='Use 1 is day is not known and January if month is.',
    )
    image = models.ImageField(
        upload_to='media/rulebook',
        blank=True,
        null=True,
        help_text='200px * ~250px please.'
    )
    official_url = models.URLField(
        max_length=255,
        blank=True,
    )
    slug = models.SlugField(
        max_length=128,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.rulebook_detail', (),
            {
                'edition_slug': self.dnd_edition.slug,
                'edition_id': self.dnd_edition.id,
                'rulebook_slug': self.slug,
                'rulebook_id': self.id,
            }
        )


class CharacterClass(models.Model):
    name = models.CharField(
        max_length=64,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )
    prestige = models.BooleanField()

    short_description = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    short_description_html = models.TextField(
        editable=False,
        blank=True,
    )

    class Meta:
        ordering = ['name', ]

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'short_description')
        super(CharacterClass, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.character_class_detail', (),
            {
                'character_class_slug': self.slug,
            }
        )


class CharacterClassVariant(models.Model):
    character_class = models.ForeignKey(
        CharacterClass,
    )
    rulebook = models.ForeignKey(
        Rulebook,
    )
    page = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    skill_points = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='X + Int modifier',
    )
    class_skills = models.ManyToManyField(
        'Skill',
        blank=True,
    )
    requirements = models.TextField(
        blank=True,
        help_text='Textile enabled! ONLY other requirements than BAB, Skills, Feats, Races',
    )
    requirements_html = models.TextField(
        editable=False,
        blank=True,
    )
    required_bab = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='Results in Base Attack Bonus: +x',
    )
    class_features = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    class_features_html = models.TextField(
        editable=False,
        blank=True,
    )
    hit_die = models.PositiveSmallIntegerField(
        help_text='For d4 write 4 etc.',
        blank=True,
        null=True,
    )
    alignment = models.CharField(
        blank=True,
        max_length=256,
    )
    starting_gold = models.CharField(
        blank=True,
        max_length=32,
        help_text='Do NOT use gold from Starting package! That amount is reduced by other equipment used. Check p. 111 '
                  'in PHB for more info. Do not put in Average gold amount.'
    )

    advancement = models.TextField(
        blank=True,
        help_text='Textile enabled! (bit.ly/JigkFt)',
    )
    advancement_html = models.TextField(
        editable=False,
        blank=True,
    )

    class Meta:
        unique_together = (("character_class", "rulebook",))
        ordering = ['character_class__name', ]

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'requirements', 'advancement', 'class_features')
        super(CharacterClassVariant, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s variant (%s)" % (self.character_class.name, self.rulebook.name)

    @models.permalink
    def get_absolute_url(self):
        return (
            'character_class_variant_detail', (),
            {
                'rulebook_slug': self.rulebook.slug,
                'rulebook_id': self.rulebook.id,
                'character_class_slug': self.character_class.slug
            }
        )


class CharacterClassVariantRequiresRace(models.Model):
    character_class_variant = models.ForeignKey(
        CharacterClassVariant,
        related_name='required_races',
    )
    race = models.ForeignKey(
        'Race',
    )
    extra = models.CharField(
        blank=True,
        max_length=32
    )
    text_before = models.CharField(
        blank=True,
        max_length=64,
        help_text='Displayed before Race, no parenthesis! Use to create "or", "and" etc.',
    )
    text_after = models.CharField(
        blank=True,
        max_length=64,
        help_text='Displayed after Race, no parenthesis! Use to create "or", "and" etc.',
    )
    remove_comma = models.BooleanField(
        help_text='Removes comma before Race! Use to create "or", "and" etc.',
    )


class CharacterClassVariantRequiresFeat(models.Model):
    character_class_variant = models.ForeignKey(
        CharacterClassVariant,
        related_name='required_feats',
    )
    feat = models.ForeignKey(
        'Feat',
    )
    extra = models.CharField(
        blank=True,
        max_length=32
    )
    text_before = models.CharField(
        blank=True,
        max_length=64,
        help_text='Displayed before Feat, no parenthesis! Use to create "or", "and" etc.',
    )
    text_after = models.CharField(
        blank=True,
        max_length=64,
        help_text='Displayed after Feat, no parenthesis! Use to create "or", "and" etc.',
    )
    remove_comma = models.BooleanField(
        help_text='Removes comma before Feat! Use to create "or", "and" etc.',
    )


class CharacterClassVariantRequiresSkill(models.Model):
    character_class_variant = models.ForeignKey(
        CharacterClassVariant,
        related_name='required_skills',
    )
    skill = models.ForeignKey(
        'Skill',
    )
    ranks = models.PositiveSmallIntegerField(

    )

    extra = models.CharField(
        blank=True,
        max_length=32
    )
    text_before = models.CharField(
        blank=True,
        max_length=64,
        help_text='Displayed before Skill, no parenthesis! Use to create "or", "and" etc.',
    )
    text_after = models.CharField(
        blank=True,
        max_length=64,
        help_text='Displayed after Skill, no parenthesis! Use to create "or", "and" etc.',
    )
    remove_comma = models.BooleanField(
        help_text='Removes comma before Skill! Use to create "or", "and" etc.',
    )


class Domain(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.spell_domain_detail', (),
            {
                'spell_domain_slug': self.slug,
            }
        )


class SpellDescriptor(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.spell_descriptor_detail', (),
            {
                'spell_descriptor_slug': self.slug,
            }
        )


class SpellSchool(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.spell_school_detail', (),
            {
                'spell_school_slug': self.slug,
            }
        )


class SpellSubSchool(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.spell_sub_school_detail', (),
            {
                'spell_sub_school_slug': self.slug,
            }
        )


class Spell(models.Model):
    added = models.DateTimeField(
        auto_now_add=True,
    )
    rulebook = models.ForeignKey(
        Rulebook,
    )
    page = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=64,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=64,
    )
    school = models.ForeignKey(
        SpellSchool,
    )
    sub_school = models.ForeignKey(
        SpellSubSchool,
        null=True,
        blank=True,
    )
    descriptors = models.ManyToManyField(
        SpellDescriptor,
        blank=True,
    )
    class_levels = models.ManyToManyField(
        CharacterClass,
        through='SpellClassLevel',
    )
    domain_levels = models.ManyToManyField(
        Domain,
        through='SpellDomainLevel',
    )
    verbal_component = models.BooleanField()
    somatic_component = models.BooleanField()
    material_component = models.BooleanField()
    arcane_focus_component = models.BooleanField()
    divine_focus_component = models.BooleanField()
    xp_component = models.BooleanField()
    meta_breath_component = models.BooleanField()
    true_name_component = models.BooleanField()

    extra_components = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text='Extra obscure components like Archon, Eldarin etc. Comma separated.',
    )

    casting_time = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    # noinspection PyShadowingBuiltins
    range = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    target = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    effect = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    area = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    duration = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    saving_throw = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    spell_resistance = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text='Textile enabled!',
    )
    description_html = models.TextField(
        editable=False,
        blank=True,
    )

    corrupt_component = models.BooleanField(
        help_text='Corrupt spells are special spells described in p. 77-78 of Book of Vile Darkness.',
        default=False,
    )
    corrupt_level = models.PositiveSmallIntegerField(
        help_text='Level of corrupt spells (as they are not binded to any class)',
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = (("name", "rulebook",))
        ordering = ['name', ]

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'description')
        super(Spell, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.spell_detail', (),
            {
                'spell_slug': self.slug,
                'spell_id': self.id,
                'rulebook_slug': self.rulebook.slug,
                'rulebook_id': self.rulebook.id,
            }
        )


class SpellClassLevel(models.Model):
    character_class = models.ForeignKey(
        CharacterClass,
    )
    spell = models.ForeignKey(
        Spell,
    )
    level = models.PositiveSmallIntegerField()
    extra = models.CharField(
        max_length=32,
        blank=True,
    )

    class Meta:
        ordering = ['spell', 'level', ]
        unique_together = (("character_class", "spell",))


class SpellDomainLevel(models.Model):
    domain = models.ForeignKey(
        Domain,
    )
    spell = models.ForeignKey(
        Spell,
    )
    level = models.PositiveSmallIntegerField()
    extra = models.CharField(
        max_length=32,
        blank=True,
    )

    class Meta:
        ordering = ['spell', 'level', ]
        unique_together = (("domain", "spell",))


class FeatCategory(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = 'feat categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.feat_category_detail', (),
            {
                'category_slug': self.slug,
            }
        )


class Skill(models.Model):
    required_by_feats = models.ManyToManyField(
        'Feat',
        through='FeatRequiresSkill',
    )

    name = models.CharField(
        max_length=64,
        unique=True,
    )
    base_skill = models.CharField(
        max_length=4,
    )

    slug = models.SlugField(
        max_length=64,
        unique=True,
    )

    trained_only = models.BooleanField()
    armor_check_penalty = models.BooleanField()

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.skill_detail', (),
            {
                'skill_slug': self.slug,
            }
        )


class SkillVariant(models.Model):
    skill = models.ForeignKey(
        Skill,
    )
    rulebook = models.ForeignKey(
        Rulebook,
    )
    page = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    description_html = models.TextField(
        editable=False,
        blank=True,
    )

    check = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    check_html = models.TextField(
        editable=False,
        blank=True,
    )

    action = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    action_html = models.TextField(
        editable=False,
        blank=True,
    )

    try_again = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    try_again_html = models.TextField(
        editable=False,
        blank=True,
    )

    special = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    special_html = models.TextField(
        editable=False,
        blank=True,
    )

    synergy = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    synergy_html = models.TextField(
        editable=False,
        blank=True,
    )

    restriction = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    restriction_html = models.TextField(
        editable=False,
        blank=True,
    )

    untrained = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    untrained_html = models.TextField(
        editable=False,
        blank=True,
    )

    class Meta:
        unique_together = (("skill", "rulebook",))

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'description', 'check', 'action',
                                     'try_again', 'special', 'synergy', 'restriction', 'untrained')
        super(SkillVariant, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s variant (%s)" % (self.skill.name, self.rulebook.name)

    @models.permalink
    def get_absolute_url(self):
        return (
            'skill_variant_detail', (),
            {
                'rulebook_slug': self.rulebook.slug,
                'rulebook_id': self.rulebook.id,
                'skill_slug': self.skill.slug
            }
        )


class SpecialFeatPrerequisite(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
    )
    print_format = models.CharField(
        max_length=64,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name


class Feat(models.Model):
    rulebook = models.ForeignKey(
        Rulebook,
    )

    feat_categories = models.ManyToManyField(
        FeatCategory,
    )
    special_feat_prerequisites = models.ManyToManyField(
        SpecialFeatPrerequisite,
        through='FeatSpecialFeatPrerequisite',
    )

    name = models.CharField(
        max_length=64,
        db_index=True,
    )

    description = models.TextField(
        help_text='Textile enabled!',
    )
    benefit = models.TextField(
        help_text='Textile enabled!',
    )
    special = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    normal = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )

    page = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        max_length=64,
    )

    # textile cache
    description_html = models.TextField(
        editable=False,
        blank=True,
    )
    benefit_html = models.TextField(
        editable=False,
        blank=True,
    )
    special_html = models.TextField(
        editable=False,
        blank=True,
    )
    normal_html = models.TextField(
        editable=False,
        blank=True,
    )

    class Meta:
        unique_together = (("character_class", "rulebook",))

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'description', 'benefit', 'special', 'normal')
        super(Feat, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("name", "rulebook",))
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.feat_detail', (),
            {
                'feat_slug': self.slug,
                'feat_id': self.id,
                'rulebook_slug': self.rulebook.slug,
                'rulebook_id': self.rulebook.id,
            }
        )


class TextFeatPrerequisite(models.Model):
    feat = models.ForeignKey(
        Feat,
    )
    text = models.CharField(
        max_length=256,
    )

    class Meta:
        ordering = ['text']

    def __unicode__(self):
        return self.text


class FeatSpecialFeatPrerequisite(models.Model):
    feat = models.ForeignKey(
        Feat,
    )
    special_feat_prerequisite = models.ForeignKey(
        SpecialFeatPrerequisite,
    )
    value_1 = models.CharField(
        max_length=256,
        blank=True,
    )
    value_2 = models.CharField(
        max_length=256,
        blank=True,
    )

    def format_value(self):
        try:
            if self.value_2 is None or self.value_2 == '':
                return self.special_feat_prerequisite.print_format % self.value_1

            return self.special_feat_prerequisite.print_format % (
                self.value_1, self.value_2)
        except TypeError:
            return self.special_feat_prerequisite.print_format

    def __unicode__(self):
        return self.format_value()


class FeatRequiresFeat(models.Model):
    source_feat = models.ForeignKey(
        Feat,
        related_name='required_feats',
    )
    required_feat = models.ForeignKey(
        Feat,
        related_name='required_by_feats',
    )
    additional_text = models.CharField(
        max_length=64,
        blank=True,
    )


class FeatRequiresSkill(models.Model):
    feat = models.ForeignKey(
        Feat,
        related_name='required_skills',
    )
    skill = models.ForeignKey(
        Skill,
    )
    extra = models.CharField(
        blank=True,
        max_length=32
    )
    min_rank = models.PositiveSmallIntegerField()


class Language(models.Model):
    name = models.CharField(
        max_length=64,
    )

    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    description = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    description_html = models.TextField(
        editable=False,
        blank=True,
    )

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'description')
        super(Language, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.language_detail', (),
            {
                'language_slug': self.slug,
            }
        )


class RaceSize(models.Model):
    name = models.CharField(
        max_length=32,
        db_index=True,
    )
    order = models.PositiveSmallIntegerField()
    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ['order', ]

    def __unicode__(self):
        return self.name


SPACE_REACH_CHOICES = (
    (0, 0),
    (5, 5),
    (10, 10),
    (15, 15),
    (20, 20),
    (25, 25),
    (30, 30),
    (35, 35),
    (40, 40),
    (45, 45),
    (50, 50),
    (55, 55),
    (60, 60),
)


class RaceSpeedType(models.Model):
    name = models.CharField(
        max_length=32,
        db_index=True,
    )
    extra = models.CharField(
        max_length=32,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name', 'extra']

    def __unicode__(self):
        if self.extra:
            return "%s (%s)" % (self.name, self.extra)
        return self.name


class MonsterType(models.Model):
    name = models.CharField(
        max_length=32,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.monster_type_detail', (),
            {
                'slug': self.slug,
            }
        )


class MonsterSubtype(models.Model):
    name = models.CharField(
        max_length=32,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.monster_subtype_detail', (),
            {
                'slug': self.slug,
            }
        )


class Monster(models.Model):
    rulebook = models.ForeignKey(
        Rulebook,
    )
    name = models.CharField(
        max_length=32,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=32,
    )
    page = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    size = models.ForeignKey(
        RaceSize,
        null=True,
    )
    # noinspection PyShadowingBuiltins
    type = models.ForeignKey(
        MonsterType,
        help_text='Subtypes at the bottom of page',
    )
    subtypes = models.ManyToManyField(
        MonsterSubtype,
        blank=True,
    )

    hit_dice = models.CharField(
        max_length=32,
        help_text='Eg. "1d1+0 (1 hp)"',
    )
    initiative = models.SmallIntegerField(
    )
    armor_class = models.CharField(
        max_length=128,
        help_text='Only base AC, not Touch nor FlatFooted, eg. "32 (–1 size, +4 Dex, +19 natural)"',
    )
    touch_armor_class = models.SmallIntegerField(
        blank=True,
        null=True,
    )
    flat_footed_armor_class = models.SmallIntegerField(
        blank=True,
        null=True,
    )
    base_attack = models.SmallIntegerField(
    )
    grapple = models.SmallIntegerField(
    )
    attack = models.CharField(
        max_length=128,
        help_text='Eg. "+3 greatsword +23 melee (3d6+13/19–20) or slam +20 melee (2d8+10)"',
    )
    full_attack = models.CharField(
        max_length=128,
        help_text='Eg. "+3 greatsword +23/+18/+13 melee (3d6+13/19–20) or slam +20 melee (2d8+10)"',
    )
    space = models.PositiveSmallIntegerField(
        choices=SPACE_REACH_CHOICES,
    )
    reach = models.PositiveSmallIntegerField(
        choices=SPACE_REACH_CHOICES,
    )
    special_attacks = models.CharField(
        max_length=256,
        blank=True,
        help_text='Eg. "Spell-like abilities, spells"',
    )
    special_qualities = models.CharField(
        max_length=512,
        blank=True,
        help_text='Eg. "Damage reduction 10/evil, darkvision 60 ft., low-light vision, immunity to acid, cold, and '
                  'petrification, protective aura, regeneration 10, resistance to electricity 10 and fire 10, spell '
                  'resistance 30, tongues"',
    )
    fort_save = models.SmallIntegerField(
    )
    fort_save_extra = models.CharField(
        max_length=32,
        blank=True,
        help_text='Eg. "+18 against poison"',
    )
    reflex_save = models.SmallIntegerField(
    )
    reflex_save_extra = models.CharField(
        max_length=32,
        blank=True,
        help_text='Eg. "+18 against whatever"',
    )
    will_save = models.SmallIntegerField(
    )
    will_save_extra = models.CharField(
        max_length=32,
        blank=True,
        help_text='Eg. "+18 against illusions"',
    )

    # noinspection PyShadowingBuiltins
    str = models.SmallIntegerField(
    )
    dex = models.SmallIntegerField(
    )
    con = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text='Leave blank for undeads',
    )
    # noinspection PyShadowingBuiltins
    int = models.SmallIntegerField(
    )
    wis = models.SmallIntegerField(
    )
    cha = models.SmallIntegerField(
    )
    environment = models.CharField(
        max_length=128,
        blank=True,
        help_text='Eg. "Any good-aligned plane"',
    )
    organization = models.CharField(
        max_length=128,
        blank=True,
        help_text='Eg. "Solitary or pair"',
    )
    challenge_rating = models.PositiveSmallIntegerField(
    )
    treasure = models.CharField(
        max_length=128,
        blank=True,
        help_text='Eg. "No coins; double goods; standard items"',
    )
    alignment = models.CharField(
        max_length=64,
        blank=True,
        help_text='Eg. "Always good (any)"',
    )
    advancement = models.CharField(
        max_length=64,
        blank=True,
        help_text='Eg. "15–21 HD (Large); 22–42 HD (Huge)"',
    )
    level_adjustment = models.SmallIntegerField(
        blank=True,
        null=True,
    )
    # TODO hit die, ECL;  ECL = LA + HD

    description = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    description_html = models.TextField(
        editable=False,
        blank=True,
    )

    combat = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    combat_html = models.TextField(
        editable=False,
        blank=True,
    )

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'description', 'combat')
        super(Monster, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("name", "rulebook",))
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.monster_detail', (),
            {
                'monster_slug': self.slug,
                'monster_id': self.id,
                'rulebook_slug': self.rulebook.slug,
                'rulebook_id': self.rulebook.id,
            }
        )


class MonsterHasFeat(models.Model):
    monster = models.ForeignKey(
        Monster,
        related_name='feats',
    )
    feat = models.ForeignKey(
        Feat,
    )
    extra = models.CharField(
        blank=True,
        max_length=32
    )


class MonsterHasSkill(models.Model):
    monster = models.ForeignKey(
        Monster,
        related_name='skills',
    )
    skill = models.ForeignKey(
        Skill,
    )
    ranks = models.PositiveSmallIntegerField(
    )

    extra = models.CharField(
        blank=True,
        max_length=32
    )


class MonsterSpeed(models.Model):
    race = models.ForeignKey(
        Monster,
    )
    # noinspection PyShadowingBuiltins
    type = models.ForeignKey(
        RaceSpeedType,
        related_name='+',
    )
    speed = models.PositiveSmallIntegerField()


class RaceType(models.Model):
    class BaseAttackType:
        FIGHTER = 'FIG'
        CLERIC = 'CLR'
        WIZARD = 'WIZ'

    BASE_ATTACK_TYPE_CHOICES = (
        (BaseAttackType.FIGHTER, u'Fighter'),
        (BaseAttackType.CLERIC, u'Cleric'),
        (BaseAttackType.WIZARD, u'Wizard'),
    )

    class BaseSaveType:
        GOOD = 'GOOD'
        BAD = 'BAD'

    BASE_SAVE_TYPE_CHOICES = (
        (BaseSaveType.GOOD, u'Good'),
        (BaseSaveType.BAD, u'Bad'),
    )

    name = models.CharField(
        max_length=32,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    hit_die_size = models.PositiveSmallIntegerField(
    )
    base_attack_type = models.CharField(
        max_length=3,
        blank=False,
        null=False,
        choices=BASE_ATTACK_TYPE_CHOICES,
    )
    base_fort_save_type = models.CharField(
        max_length=4,
        blank=False,
        null=False,
        choices=BASE_SAVE_TYPE_CHOICES,
    )
    base_reflex_save_type = models.CharField(
        max_length=4,
        blank=False,
        null=False,
        choices=BASE_SAVE_TYPE_CHOICES,
    )
    base_will_save_type = models.CharField(
        max_length=4,
        blank=False,
        null=False,
        choices=BASE_SAVE_TYPE_CHOICES,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.race_type_detail', (),
            {
                'race_type_slug': self.slug,
            }
        )

    def baseAttack(self, level):
        if self.base_attack_type == RaceType.BaseAttackType.FIGHTER:
            return level
        if self.base_attack_type == RaceType.BaseAttackType.CLERIC:
            return int(level * 3 / 4.0)
        if self.base_attack_type == RaceType.BaseAttackType.WIZARD:
            return int(level / 2.0)

    def baseSave(self, level, saveType):
        if saveType == RaceType.BaseSaveType.GOOD:
            return 2 + int(level / 2.0)
        if saveType == RaceType.BaseSaveType.BAD:
            return int(level / 3.0)


class Race(models.Model):
    rulebook = models.ForeignKey(
        Rulebook,
    )
    name = models.CharField(
        max_length=32,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=32,
    )
    page = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    size = models.ForeignKey(
        RaceSize,
        null=True,
        blank=True,
    )
    # noinspection PyShadowingBuiltins
    str = models.SmallIntegerField(
        default=0,
    )
    dex = models.SmallIntegerField(
        default=0,
    )
    con = models.SmallIntegerField(
        default=0,
        blank=True,
        null=True,
    )
    # noinspection PyShadowingBuiltins
    int = models.SmallIntegerField(
        default=0,
    )
    wis = models.SmallIntegerField(
        default=0,
    )
    cha = models.SmallIntegerField(
        default=0,
    )
    level_adjustment = models.SmallIntegerField(
        default=0,
    )
    space = models.PositiveSmallIntegerField(
        choices=SPACE_REACH_CHOICES,
        blank=True,
        null=True,
    )
    reach = models.PositiveSmallIntegerField(
        choices=SPACE_REACH_CHOICES,
        blank=True,
        null=True,
    )

    natural_armor = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text='Only if there is any bonus! Omit for no bonus (do not write "0")',
    )

    automatic_languages = models.ManyToManyField(
        Language,
        blank=True,
        related_name='races_with_automatic',
    )
    bonus_languages = models.ManyToManyField(
        Language,
        blank=True,
        related_name='races_with_bonus',
    )

    race_type = models.ForeignKey(
        to=RaceType,
        blank=True,
        null=True,
        help_text='Select from list. Hit Die, Attack bonus and Saves are calculated automatically',
    )
    racial_hit_dice_count = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='Number of hit dice, for "6d8 Hit Dice" enter 6',
    )

    description = models.TextField(
        blank=True,
        help_text='Textile enabled! Do not enter Natural AC, Racial Feats, Racial HD nor Languages.',
    )
    description_html = models.TextField(
        editable=False,
        blank=True,
    )

    combat = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    combat_html = models.TextField(
        editable=False,
        blank=True,
    )

    racial_traits = models.TextField(
        blank=True,
        help_text='Textile enabled!',
    )
    racial_traits_html = models.TextField(
        editable=False,
        blank=True,
    )

    # noinspection PyMethodParameters,PyUnusedLocal
    def image_filename(instance, filename):
        return 'media/race/%d.jpg' % instance.id

    image = models.ImageField(
        upload_to=image_filename,
        blank=True,
        null=True,
        help_text='auto-resized to 500px * 500px max, jpeg only plz.',
    )

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'description', 'combat', 'racial_traits')
        super(Race, self).save(*args, **kwargs)

        # resize
        if self.image:
            filename = self.image.path
            image = Image.open(filename)
            assert isinstance(image, Image.Image)
            image.thumbnail((500, 500), Image.ANTIALIAS)
            image.save(filename)

    class Meta:
        unique_together = (("name", "rulebook",))
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.race_detail', (),
            {
                'race_slug': self.slug,
                'race_id': self.id,
                'rulebook_slug': self.rulebook.slug,
                'rulebook_id': self.rulebook.id,
            }
        )

    def racialBaseAttack(self):
        if self.race_type:
            return self.race_type.baseAttack(self.racial_hit_dice_count)
        return None

    def racialBaseFortSave(self):
        if self.race_type:
            return self.race_type.baseSave(self.racial_hit_dice_count, self.race_type.base_fort_save_type)
        return None

    def racialBaseReflexSave(self):
        if self.race_type:
            return self.race_type.baseSave(self.racial_hit_dice_count, self.race_type.base_reflex_save_type)
        return None

    def racialBaseWillSave(self):
        if self.race_type:
            return self.race_type.baseSave(self.racial_hit_dice_count, self.race_type.base_will_save_type)
        return None


class RaceSpeed(models.Model):
    race = models.ForeignKey(
        Race,
    )
    # noinspection PyShadowingBuiltins
    type = models.ForeignKey(
        RaceSpeedType,
        related_name='+',
    )
    speed = models.PositiveSmallIntegerField()


class RaceFavoredCharacterClass(models.Model):
    race = models.ForeignKey(
        Race,
        related_name='favored_classes',
    )
    character_class = models.ForeignKey(
        CharacterClass,
    )
    extra = models.CharField(
        blank=True,
        max_length=32,
    )


class ItemSlot(models.Model):
    name = models.CharField(
        max_length=64,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name


class ItemProperty(models.Model):
    name = models.CharField(
        max_length=64,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name


class ItemAuraType(models.Model):
    name = models.CharField(
        max_length=64,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name


class ItemActivationType(models.Model):
    name = models.CharField(
        max_length=64,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name


class Item(models.Model):
    class ItemType:
        MUNDANE = 'MUN'
        MAGIC = 'MAG'
        ENHANCEMENT = 'ENH'

    ITEM_TYPE = (
        (ItemType.MUNDANE, u'Mundane Item'),
        (ItemType.MAGIC, u'Magic Item'),
        (ItemType.ENHANCEMENT, u'Enhancement'),
    )

    # noinspection PyShadowingBuiltins
    type = models.CharField(
        max_length=3,
        blank=False,
        null=False,
        choices=ITEM_TYPE,
    )

    name = models.CharField(
        max_length=64,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )

    rulebook = models.ForeignKey(
        Rulebook,
    )
    page = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

    price_gp = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Price in gold pieces.',
    )
    price_bonus = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='Price as +X bonus (eg. Vorpal is +5 bonus).',
    )
    item_level = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='Used in Magic Item Compendium, NOT CASTER LEVEL!',
    )
    body_slot = models.ForeignKey(
        ItemSlot,
        blank=True,
        null=True,
        help_text='Only Mundane and Magic Items.',
    )
    # noinspection PyShadowingBuiltins
    property = models.ForeignKey(
        ItemProperty,
        blank=True,
        null=True,
        help_text='Only Armor and Magic Enhancements.'
    )
    caster_level = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='Not for Mundane Items.',
    )
    aura = models.ForeignKey(
        ItemAuraType,
        blank=True,
        null=True,
        help_text='Not for Mundane Items.',
    )
    aura_dc = models.CharField(
        blank=True,
        help_text='Not for Mundane Items.',
        max_length=16,
    )
    aura_schools = models.ManyToManyField(
        SpellSchool,
        blank=True,
        help_text='Not for Mundane Items.',
    )
    activation = models.ForeignKey(
        ItemActivationType,
        blank=True,
        null=True,
        help_text='Leave blank for —. Not for Mundane Items.',
    )
    weight = models.FloatField(
        blank=True,
        null=True,
        help_text='Leave blank for —. Not for Armor and Magic Enhancements.',
    )

    visual_description = models.TextField(
        blank=True,
        help_text='Automatically in italics!',
    )
    description = models.TextField(
        blank=False,
        help_text='Textile enabled!',
    )
    description_html = models.TextField(
        editable=False,
        blank=False,
    )

    cost_to_create = models.CharField(
        max_length=128,
        blank=True,
        help_text='Fill ONLY if you don\'t want cost to be calculated! (50% gold, 1/25 xp, 1/1000 days for regular, '
                  '"varies" for +x items). Use dash (-) to surpress this field.',
    )

    required_extra = models.CharField(
        max_length=64,
        blank=True,
        help_text='Anything extra in Prerequisites field. No textile!',
    )

    synergy_prerequisite = models.ForeignKey(
        'Item',
        blank=True,
        null=True,
        help_text='Only Armor and Magic Enhancements.',
        limit_choices_to={'type': ItemType.ENHANCEMENT},
    )

    # TODO descriptors, extra req

    required_feats = models.ManyToManyField(
        Feat,
        blank=True,
        limit_choices_to={'feat_categories__slug': 'item-creation'},
    )
    required_spells = models.ManyToManyField(
        Spell,
        blank=True,
    )

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # TODO remove params based on "only for"
        update_html_cache_attributes(self, 'description')
        super(Item, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.item_detail', (),
            {
                'item_slug': self.slug,
                'item_id': self.id,
                'rulebook_slug': self.rulebook.slug,
                'rulebook_id': self.rulebook.id,
            }
        )


class NewsEntry(models.Model):
    published = models.DateField(
        blank=False,
        null=False,
    )

    title = models.CharField(
        blank=False,
        null=False,
        max_length=64,
    )

    body = models.TextField(
        help_text='Textile enabled!',
    )

    body_html = models.TextField(
        editable=False,
    )

    enabled = models.BooleanField(
        blank=False,
        null=False,
        default=True,
    )

    class Meta:
        verbose_name_plural = "news entries"
        ordering = ['-published', ]

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.published)

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'body')
        super(NewsEntry, self).save(*args, **kwargs)


class StaticPage(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=32,
    )

    body = models.TextField(
        help_text='Textile enabled!',
    )

    body_html = models.TextField(
        editable=False,
    )

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'body')
        super(StaticPage, self).save(*args, **kwargs)


class Rule(models.Model):
    name = models.CharField(
        blank=False,
        max_length=64,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )

    body = models.TextField(
        help_text='Textile enabled!',
    )
    body_html = models.TextField(
        editable=False,
    )
    rulebook = models.ForeignKey(
        Rulebook,
        blank=False,
        null=False,
    )
    page_from = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    page_to = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.rulebook.name)

    def save(self, *args, **kwargs):
        update_html_cache_attributes(self, 'body')
        super(Rule, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return (
            'dndtools.dnd.views.rule_detail', (),
            {'rule_slug': self.slug,
             'rule_id': self.id,
             'rulebook_slug': self.rulebook.slug,
             'rulebook_id': self.rulebook.id,
            }
        )