# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DndEdition'
        db.create_table(u'dnd_dndedition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('system', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
            ('core', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'dnd', ['DndEdition'])

        # Adding model 'Rulebook'
        db.create_table(u'dnd_rulebook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dnd_edition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.DndEdition'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('abbr', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('official_url', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'dnd', ['Rulebook'])

        # Adding model 'CharacterClass'
        db.create_table(u'dnd_characterclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
            ('prestige', self.gf('django.db.models.fields.BooleanField')()),
            ('short_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('short_description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'dnd', ['CharacterClass'])

        # Adding model 'CharacterClassVariant'
        db.create_table(u'dnd_characterclassvariant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.CharacterClass'])),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('skill_points', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('requirements', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('requirements_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('required_bab', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('class_features', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('class_features_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('hit_die', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('alignment', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('starting_gold', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('advancement', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('advancement_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'dnd', ['CharacterClassVariant'])

        # Adding unique constraint on 'CharacterClassVariant', fields ['character_class', 'rulebook']
        db.create_unique(u'dnd_characterclassvariant', ['character_class_id', 'rulebook_id'])

        # Adding M2M table for field class_skills on 'CharacterClassVariant'
        m2m_table_name = db.shorten_name(u'dnd_characterclassvariant_class_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('characterclassvariant', models.ForeignKey(orm[u'dnd.characterclassvariant'], null=False)),
            ('skill', models.ForeignKey(orm[u'dnd.skill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['characterclassvariant_id', 'skill_id'])

        # Adding model 'CharacterClassVariantRequiresRace'
        db.create_table(u'dnd_characterclassvariantrequiresrace', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character_class_variant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='required_races', to=orm['dnd.CharacterClassVariant'])),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Race'])),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('text_before', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('text_after', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('remove_comma', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'dnd', ['CharacterClassVariantRequiresRace'])

        # Adding model 'CharacterClassVariantRequiresFeat'
        db.create_table(u'dnd_characterclassvariantrequiresfeat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character_class_variant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='required_feats', to=orm['dnd.CharacterClassVariant'])),
            ('feat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Feat'])),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('text_before', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('text_after', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('remove_comma', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'dnd', ['CharacterClassVariantRequiresFeat'])

        # Adding model 'CharacterClassVariantRequiresSkill'
        db.create_table(u'dnd_characterclassvariantrequiresskill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character_class_variant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='required_skills', to=orm['dnd.CharacterClassVariant'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Skill'])),
            ('ranks', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('text_before', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('text_after', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('remove_comma', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'dnd', ['CharacterClassVariantRequiresSkill'])

        # Adding model 'Deity'
        db.create_table(u'dnd_deity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('alignment', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('favored_weapon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Item'], null=True, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['Deity'])

        # Adding model 'Domain'
        db.create_table(u'dnd_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'dnd', ['Domain'])

        # Adding model 'DomainVariant'
        db.create_table(u'dnd_domainvariant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Domain'])),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('deities_text', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('requirement', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('granted_power', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('granted_power_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('granted_power_type', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['DomainVariant'])

        # Adding M2M table for field deities on 'DomainVariant'
        m2m_table_name = db.shorten_name(u'dnd_domainvariant_deities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('domainvariant', models.ForeignKey(orm[u'dnd.domainvariant'], null=False)),
            ('deity', models.ForeignKey(orm[u'dnd.deity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['domainvariant_id', 'deity_id'])

        # Adding M2M table for field other_deities on 'DomainVariant'
        m2m_table_name = db.shorten_name(u'dnd_domainvariant_other_deities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('domainvariant', models.ForeignKey(orm[u'dnd.domainvariant'], null=False)),
            ('deity', models.ForeignKey(orm[u'dnd.deity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['domainvariant_id', 'deity_id'])

        # Adding model 'SpellDescriptor'
        db.create_table(u'dnd_spelldescriptor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'dnd', ['SpellDescriptor'])

        # Adding model 'SpellSchool'
        db.create_table(u'dnd_spellschool', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
        ))
        db.send_create_signal(u'dnd', ['SpellSchool'])

        # Adding model 'SpellSubSchool'
        db.create_table(u'dnd_spellsubschool', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
        ))
        db.send_create_signal(u'dnd', ['SpellSubSchool'])

        # Adding model 'Spell'
        db.create_table(u'dnd_spell', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=64)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.SpellSchool'])),
            ('sub_school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.SpellSubSchool'], null=True, blank=True)),
            ('verbal_component', self.gf('django.db.models.fields.BooleanField')()),
            ('somatic_component', self.gf('django.db.models.fields.BooleanField')()),
            ('material_component', self.gf('django.db.models.fields.BooleanField')()),
            ('arcane_focus_component', self.gf('django.db.models.fields.BooleanField')()),
            ('divine_focus_component', self.gf('django.db.models.fields.BooleanField')()),
            ('xp_component', self.gf('django.db.models.fields.BooleanField')()),
            ('meta_breath_component', self.gf('django.db.models.fields.BooleanField')()),
            ('true_name_component', self.gf('django.db.models.fields.BooleanField')()),
            ('extra_components', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('casting_time', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('range', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('effect', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('saving_throw', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('spell_resistance', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('corrupt_component', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('corrupt_level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verified_author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('verified_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['Spell'])

        # Adding unique constraint on 'Spell', fields ['name', 'rulebook']
        db.create_unique(u'dnd_spell', ['name', 'rulebook_id'])

        # Adding M2M table for field descriptors on 'Spell'
        m2m_table_name = db.shorten_name(u'dnd_spell_descriptors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('spell', models.ForeignKey(orm[u'dnd.spell'], null=False)),
            ('spelldescriptor', models.ForeignKey(orm[u'dnd.spelldescriptor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['spell_id', 'spelldescriptor_id'])

        # Adding model 'SpellClassLevel'
        db.create_table(u'dnd_spellclasslevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.CharacterClass'])),
            ('spell', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Spell'])),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['SpellClassLevel'])

        # Adding unique constraint on 'SpellClassLevel', fields ['character_class', 'spell']
        db.create_unique(u'dnd_spellclasslevel', ['character_class_id', 'spell_id'])

        # Adding model 'SpellDomainLevel'
        db.create_table(u'dnd_spelldomainlevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Domain'])),
            ('spell', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Spell'])),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['SpellDomainLevel'])

        # Adding unique constraint on 'SpellDomainLevel', fields ['domain', 'spell']
        db.create_unique(u'dnd_spelldomainlevel', ['domain_id', 'spell_id'])

        # Adding model 'FeatCategory'
        db.create_table(u'dnd_featcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
        ))
        db.send_create_signal(u'dnd', ['FeatCategory'])

        # Adding model 'Skill'
        db.create_table(u'dnd_skill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('base_skill', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
            ('trained_only', self.gf('django.db.models.fields.BooleanField')()),
            ('armor_check_penalty', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'dnd', ['Skill'])

        # Adding model 'SkillVariant'
        db.create_table(u'dnd_skillvariant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Skill'])),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('check', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('check_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('action', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('action_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('try_again', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('try_again_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('special', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('special_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('synergy', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('synergy_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('restriction', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('restriction_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('untrained', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('untrained_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'dnd', ['SkillVariant'])

        # Adding unique constraint on 'SkillVariant', fields ['skill', 'rulebook']
        db.create_unique(u'dnd_skillvariant', ['skill_id', 'rulebook_id'])

        # Adding model 'SpecialFeatPrerequisite'
        db.create_table(u'dnd_specialfeatprerequisite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('print_format', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'dnd', ['SpecialFeatPrerequisite'])

        # Adding model 'Feat'
        db.create_table(u'dnd_feat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('benefit', self.gf('django.db.models.fields.TextField')()),
            ('special', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('normal', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=64)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('benefit_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('special_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('normal_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'dnd', ['Feat'])

        # Adding M2M table for field feat_categories on 'Feat'
        m2m_table_name = db.shorten_name(u'dnd_feat_feat_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feat', models.ForeignKey(orm[u'dnd.feat'], null=False)),
            ('featcategory', models.ForeignKey(orm[u'dnd.featcategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feat_id', 'featcategory_id'])

        # Adding model 'TextFeatPrerequisite'
        db.create_table(u'dnd_textfeatprerequisite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Feat'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'dnd', ['TextFeatPrerequisite'])

        # Adding model 'FeatSpecialFeatPrerequisite'
        db.create_table(u'dnd_featspecialfeatprerequisite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Feat'])),
            ('special_feat_prerequisite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.SpecialFeatPrerequisite'])),
            ('value_1', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('value_2', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['FeatSpecialFeatPrerequisite'])

        # Adding model 'FeatRequiresFeat'
        db.create_table(u'dnd_featrequiresfeat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_feat', self.gf('django.db.models.fields.related.ForeignKey')(related_name='required_feats', to=orm['dnd.Feat'])),
            ('required_feat', self.gf('django.db.models.fields.related.ForeignKey')(related_name='required_by_feats', to=orm['dnd.Feat'])),
            ('additional_text', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['FeatRequiresFeat'])

        # Adding model 'FeatRequiresSkill'
        db.create_table(u'dnd_featrequiresskill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feat', self.gf('django.db.models.fields.related.ForeignKey')(related_name='required_skills', to=orm['dnd.Feat'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Skill'])),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('min_rank', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'dnd', ['FeatRequiresSkill'])

        # Adding model 'Language'
        db.create_table(u'dnd_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'dnd', ['Language'])

        # Adding model 'RaceSize'
        db.create_table(u'dnd_racesize', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'dnd', ['RaceSize'])

        # Adding model 'RaceSpeedType'
        db.create_table(u'dnd_racespeedtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['RaceSpeedType'])

        # Adding model 'MonsterType'
        db.create_table(u'dnd_monstertype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
        ))
        db.send_create_signal(u'dnd', ['MonsterType'])

        # Adding model 'MonsterSubtype'
        db.create_table(u'dnd_monstersubtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
        ))
        db.send_create_signal(u'dnd', ['MonsterSubtype'])

        # Adding model 'Monster'
        db.create_table(u'dnd_monster', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=32)),
            ('page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.RaceSize'], null=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.MonsterType'])),
            ('hit_dice', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('initiative', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('armor_class', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('touch_armor_class', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('flat_footed_armor_class', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('base_attack', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('grapple', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('attack', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('full_attack', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('space', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('reach', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('special_attacks', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('special_qualities', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('fort_save', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('fort_save_extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('reflex_save', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('reflex_save_extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('will_save', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('will_save_extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('str', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('dex', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('con', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('int', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('wis', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('cha', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('environment', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('challenge_rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('treasure', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('alignment', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('advancement', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('level_adjustment', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('combat', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('combat_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'dnd', ['Monster'])

        # Adding unique constraint on 'Monster', fields ['name', 'rulebook']
        db.create_unique(u'dnd_monster', ['name', 'rulebook_id'])

        # Adding M2M table for field subtypes on 'Monster'
        m2m_table_name = db.shorten_name(u'dnd_monster_subtypes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monster', models.ForeignKey(orm[u'dnd.monster'], null=False)),
            ('monstersubtype', models.ForeignKey(orm[u'dnd.monstersubtype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['monster_id', 'monstersubtype_id'])

        # Adding model 'MonsterHasFeat'
        db.create_table(u'dnd_monsterhasfeat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feats', to=orm['dnd.Monster'])),
            ('feat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Feat'])),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['MonsterHasFeat'])

        # Adding model 'MonsterHasSkill'
        db.create_table(u'dnd_monsterhasskill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='skills', to=orm['dnd.Monster'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Skill'])),
            ('ranks', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['MonsterHasSkill'])

        # Adding model 'MonsterSpeed'
        db.create_table(u'dnd_monsterspeed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Monster'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['dnd.RaceSpeedType'])),
            ('speed', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'dnd', ['MonsterSpeed'])

        # Adding model 'RaceType'
        db.create_table(u'dnd_racetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
            ('hit_die_size', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('base_attack_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('base_fort_save_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('base_reflex_save_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('base_will_save_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'dnd', ['RaceType'])

        # Adding model 'Race'
        db.create_table(u'dnd_race', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=32)),
            ('page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.RaceSize'])),
            ('str', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('dex', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('con', self.gf('django.db.models.fields.SmallIntegerField')(default=0, null=True, blank=True)),
            ('int', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('wis', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('cha', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('level_adjustment', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('space', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('reach', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('natural_armor', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('race_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.RaceType'], null=True, blank=True)),
            ('racial_hit_dice_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('combat', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('combat_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('racial_traits', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('racial_traits_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['Race'])

        # Adding unique constraint on 'Race', fields ['name', 'rulebook']
        db.create_unique(u'dnd_race', ['name', 'rulebook_id'])

        # Adding M2M table for field automatic_languages on 'Race'
        m2m_table_name = db.shorten_name(u'dnd_race_automatic_languages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('race', models.ForeignKey(orm[u'dnd.race'], null=False)),
            ('language', models.ForeignKey(orm[u'dnd.language'], null=False))
        ))
        db.create_unique(m2m_table_name, ['race_id', 'language_id'])

        # Adding M2M table for field bonus_languages on 'Race'
        m2m_table_name = db.shorten_name(u'dnd_race_bonus_languages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('race', models.ForeignKey(orm[u'dnd.race'], null=False)),
            ('language', models.ForeignKey(orm[u'dnd.language'], null=False))
        ))
        db.create_unique(m2m_table_name, ['race_id', 'language_id'])

        # Adding model 'RaceSpeed'
        db.create_table(u'dnd_racespeed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Race'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['dnd.RaceSpeedType'])),
            ('speed', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'dnd', ['RaceSpeed'])

        # Adding model 'RaceFavoredCharacterClass'
        db.create_table(u'dnd_racefavoredcharacterclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(related_name='favored_classes', to=orm['dnd.Race'])),
            ('character_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.CharacterClass'])),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['RaceFavoredCharacterClass'])

        # Adding model 'ItemSlot'
        db.create_table(u'dnd_itemslot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'dnd', ['ItemSlot'])

        # Adding model 'ItemProperty'
        db.create_table(u'dnd_itemproperty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'dnd', ['ItemProperty'])

        # Adding model 'ItemAuraType'
        db.create_table(u'dnd_itemauratype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'dnd', ['ItemAuraType'])

        # Adding model 'ItemActivationType'
        db.create_table(u'dnd_itemactivationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'dnd', ['ItemActivationType'])

        # Adding model 'Item'
        db.create_table(u'dnd_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('price_gp', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('price_bonus', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('item_level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('body_slot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.ItemSlot'], null=True, blank=True)),
            ('property', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.ItemProperty'], null=True, blank=True)),
            ('caster_level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('aura', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.ItemAuraType'], null=True, blank=True)),
            ('aura_dc', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('activation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.ItemActivationType'], null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('visual_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('description_html', self.gf('django.db.models.fields.TextField')()),
            ('cost_to_create', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('required_extra', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('synergy_prerequisite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Item'], null=True, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['Item'])

        # Adding M2M table for field aura_schools on 'Item'
        m2m_table_name = db.shorten_name(u'dnd_item_aura_schools')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'dnd.item'], null=False)),
            ('spellschool', models.ForeignKey(orm[u'dnd.spellschool'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'spellschool_id'])

        # Adding M2M table for field required_feats on 'Item'
        m2m_table_name = db.shorten_name(u'dnd_item_required_feats')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'dnd.item'], null=False)),
            ('feat', models.ForeignKey(orm[u'dnd.feat'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'feat_id'])

        # Adding M2M table for field required_spells on 'Item'
        m2m_table_name = db.shorten_name(u'dnd_item_required_spells')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'dnd.item'], null=False)),
            ('spell', models.ForeignKey(orm[u'dnd.spell'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'spell_id'])

        # Adding model 'NewsEntry'
        db.create_table(u'dnd_newsentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('published', self.gf('django.db.models.fields.DateField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('body_html', self.gf('django.db.models.fields.TextField')()),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'dnd', ['NewsEntry'])

        # Adding model 'StaticPage'
        db.create_table(u'dnd_staticpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('body_html', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'dnd', ['StaticPage'])

        # Adding model 'Rule'
        db.create_table(u'dnd_rule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('body_html', self.gf('django.db.models.fields.TextField')()),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('page_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('page_to', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dnd', ['Rule'])


    def backwards(self, orm):
        # Removing unique constraint on 'Race', fields ['name', 'rulebook']
        db.delete_unique(u'dnd_race', ['name', 'rulebook_id'])

        # Removing unique constraint on 'Monster', fields ['name', 'rulebook']
        db.delete_unique(u'dnd_monster', ['name', 'rulebook_id'])

        # Removing unique constraint on 'SkillVariant', fields ['skill', 'rulebook']
        db.delete_unique(u'dnd_skillvariant', ['skill_id', 'rulebook_id'])

        # Removing unique constraint on 'SpellDomainLevel', fields ['domain', 'spell']
        db.delete_unique(u'dnd_spelldomainlevel', ['domain_id', 'spell_id'])

        # Removing unique constraint on 'SpellClassLevel', fields ['character_class', 'spell']
        db.delete_unique(u'dnd_spellclasslevel', ['character_class_id', 'spell_id'])

        # Removing unique constraint on 'Spell', fields ['name', 'rulebook']
        db.delete_unique(u'dnd_spell', ['name', 'rulebook_id'])

        # Removing unique constraint on 'CharacterClassVariant', fields ['character_class', 'rulebook']
        db.delete_unique(u'dnd_characterclassvariant', ['character_class_id', 'rulebook_id'])

        # Deleting model 'DndEdition'
        db.delete_table(u'dnd_dndedition')

        # Deleting model 'Rulebook'
        db.delete_table(u'dnd_rulebook')

        # Deleting model 'CharacterClass'
        db.delete_table(u'dnd_characterclass')

        # Deleting model 'CharacterClassVariant'
        db.delete_table(u'dnd_characterclassvariant')

        # Removing M2M table for field class_skills on 'CharacterClassVariant'
        db.delete_table(db.shorten_name(u'dnd_characterclassvariant_class_skills'))

        # Deleting model 'CharacterClassVariantRequiresRace'
        db.delete_table(u'dnd_characterclassvariantrequiresrace')

        # Deleting model 'CharacterClassVariantRequiresFeat'
        db.delete_table(u'dnd_characterclassvariantrequiresfeat')

        # Deleting model 'CharacterClassVariantRequiresSkill'
        db.delete_table(u'dnd_characterclassvariantrequiresskill')

        # Deleting model 'Deity'
        db.delete_table(u'dnd_deity')

        # Deleting model 'Domain'
        db.delete_table(u'dnd_domain')

        # Deleting model 'DomainVariant'
        db.delete_table(u'dnd_domainvariant')

        # Removing M2M table for field deities on 'DomainVariant'
        db.delete_table(db.shorten_name(u'dnd_domainvariant_deities'))

        # Removing M2M table for field other_deities on 'DomainVariant'
        db.delete_table(db.shorten_name(u'dnd_domainvariant_other_deities'))

        # Deleting model 'SpellDescriptor'
        db.delete_table(u'dnd_spelldescriptor')

        # Deleting model 'SpellSchool'
        db.delete_table(u'dnd_spellschool')

        # Deleting model 'SpellSubSchool'
        db.delete_table(u'dnd_spellsubschool')

        # Deleting model 'Spell'
        db.delete_table(u'dnd_spell')

        # Removing M2M table for field descriptors on 'Spell'
        db.delete_table(db.shorten_name(u'dnd_spell_descriptors'))

        # Deleting model 'SpellClassLevel'
        db.delete_table(u'dnd_spellclasslevel')

        # Deleting model 'SpellDomainLevel'
        db.delete_table(u'dnd_spelldomainlevel')

        # Deleting model 'FeatCategory'
        db.delete_table(u'dnd_featcategory')

        # Deleting model 'Skill'
        db.delete_table(u'dnd_skill')

        # Deleting model 'SkillVariant'
        db.delete_table(u'dnd_skillvariant')

        # Deleting model 'SpecialFeatPrerequisite'
        db.delete_table(u'dnd_specialfeatprerequisite')

        # Deleting model 'Feat'
        db.delete_table(u'dnd_feat')

        # Removing M2M table for field feat_categories on 'Feat'
        db.delete_table(db.shorten_name(u'dnd_feat_feat_categories'))

        # Deleting model 'TextFeatPrerequisite'
        db.delete_table(u'dnd_textfeatprerequisite')

        # Deleting model 'FeatSpecialFeatPrerequisite'
        db.delete_table(u'dnd_featspecialfeatprerequisite')

        # Deleting model 'FeatRequiresFeat'
        db.delete_table(u'dnd_featrequiresfeat')

        # Deleting model 'FeatRequiresSkill'
        db.delete_table(u'dnd_featrequiresskill')

        # Deleting model 'Language'
        db.delete_table(u'dnd_language')

        # Deleting model 'RaceSize'
        db.delete_table(u'dnd_racesize')

        # Deleting model 'RaceSpeedType'
        db.delete_table(u'dnd_racespeedtype')

        # Deleting model 'MonsterType'
        db.delete_table(u'dnd_monstertype')

        # Deleting model 'MonsterSubtype'
        db.delete_table(u'dnd_monstersubtype')

        # Deleting model 'Monster'
        db.delete_table(u'dnd_monster')

        # Removing M2M table for field subtypes on 'Monster'
        db.delete_table(db.shorten_name(u'dnd_monster_subtypes'))

        # Deleting model 'MonsterHasFeat'
        db.delete_table(u'dnd_monsterhasfeat')

        # Deleting model 'MonsterHasSkill'
        db.delete_table(u'dnd_monsterhasskill')

        # Deleting model 'MonsterSpeed'
        db.delete_table(u'dnd_monsterspeed')

        # Deleting model 'RaceType'
        db.delete_table(u'dnd_racetype')

        # Deleting model 'Race'
        db.delete_table(u'dnd_race')

        # Removing M2M table for field automatic_languages on 'Race'
        db.delete_table(db.shorten_name(u'dnd_race_automatic_languages'))

        # Removing M2M table for field bonus_languages on 'Race'
        db.delete_table(db.shorten_name(u'dnd_race_bonus_languages'))

        # Deleting model 'RaceSpeed'
        db.delete_table(u'dnd_racespeed')

        # Deleting model 'RaceFavoredCharacterClass'
        db.delete_table(u'dnd_racefavoredcharacterclass')

        # Deleting model 'ItemSlot'
        db.delete_table(u'dnd_itemslot')

        # Deleting model 'ItemProperty'
        db.delete_table(u'dnd_itemproperty')

        # Deleting model 'ItemAuraType'
        db.delete_table(u'dnd_itemauratype')

        # Deleting model 'ItemActivationType'
        db.delete_table(u'dnd_itemactivationtype')

        # Deleting model 'Item'
        db.delete_table(u'dnd_item')

        # Removing M2M table for field aura_schools on 'Item'
        db.delete_table(db.shorten_name(u'dnd_item_aura_schools'))

        # Removing M2M table for field required_feats on 'Item'
        db.delete_table(db.shorten_name(u'dnd_item_required_feats'))

        # Removing M2M table for field required_spells on 'Item'
        db.delete_table(db.shorten_name(u'dnd_item_required_spells'))

        # Deleting model 'NewsEntry'
        db.delete_table(u'dnd_newsentry')

        # Deleting model 'StaticPage'
        db.delete_table(u'dnd_staticpage')

        # Deleting model 'Rule'
        db.delete_table(u'dnd_rule')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dnd.characterclass': {
            'Meta': {'ordering': "['name']", 'object_name': 'CharacterClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'prestige': ('django.db.models.fields.BooleanField', [], {}),
            'short_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'short_description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'dnd.characterclassvariant': {
            'Meta': {'ordering': "['character_class__name']", 'unique_together': "(('character_class', 'rulebook'),)", 'object_name': 'CharacterClassVariant'},
            'advancement': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'advancement_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'alignment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'character_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.CharacterClass']"}),
            'class_features': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'class_features_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'class_skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.Skill']", 'symmetrical': 'False', 'blank': 'True'}),
            'hit_die': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'required_bab': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'requirements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'requirements_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Rulebook']"}),
            'skill_points': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'starting_gold': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        u'dnd.characterclassvariantrequiresfeat': {
            'Meta': {'object_name': 'CharacterClassVariantRequiresFeat'},
            'character_class_variant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'required_feats'", 'to': u"orm['dnd.CharacterClassVariant']"}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'feat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Feat']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remove_comma': ('django.db.models.fields.BooleanField', [], {}),
            'text_after': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'text_before': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'dnd.characterclassvariantrequiresrace': {
            'Meta': {'object_name': 'CharacterClassVariantRequiresRace'},
            'character_class_variant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'required_races'", 'to': u"orm['dnd.CharacterClassVariant']"}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Race']"}),
            'remove_comma': ('django.db.models.fields.BooleanField', [], {}),
            'text_after': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'text_before': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'dnd.characterclassvariantrequiresskill': {
            'Meta': {'object_name': 'CharacterClassVariantRequiresSkill'},
            'character_class_variant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'required_skills'", 'to': u"orm['dnd.CharacterClassVariant']"}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ranks': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'remove_comma': ('django.db.models.fields.BooleanField', [], {}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Skill']"}),
            'text_after': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'text_before': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'dnd.deity': {
            'Meta': {'ordering': "['name']", 'object_name': 'Deity'},
            'alignment': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'favored_weapon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Item']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'dnd.dndedition': {
            'Meta': {'ordering': "['name']", 'object_name': 'DndEdition'},
            'core': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'dnd.domain': {
            'Meta': {'ordering': "['name']", 'object_name': 'Domain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'dnd.domainvariant': {
            'Meta': {'object_name': 'DomainVariant'},
            'deities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'primary_domains'", 'blank': 'True', 'to': u"orm['dnd.Deity']"}),
            'deities_text': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Domain']"}),
            'granted_power': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'granted_power_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'granted_power_type': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_deities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'other_domains'", 'blank': 'True', 'to': u"orm['dnd.Deity']"}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'requirement': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Rulebook']"})
        },
        u'dnd.feat': {
            'Meta': {'ordering': "['name']", 'object_name': 'Feat'},
            'benefit': ('django.db.models.fields.TextField', [], {}),
            'benefit_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'feat_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.FeatCategory']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'normal': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'normal_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Rulebook']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64'}),
            'special': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'special_feat_prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.SpecialFeatPrerequisite']", 'through': u"orm['dnd.FeatSpecialFeatPrerequisite']", 'symmetrical': 'False'}),
            'special_html': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'dnd.featcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'FeatCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'dnd.featrequiresfeat': {
            'Meta': {'object_name': 'FeatRequiresFeat'},
            'additional_text': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'required_feat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'required_by_feats'", 'to': u"orm['dnd.Feat']"}),
            'source_feat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'required_feats'", 'to': u"orm['dnd.Feat']"})
        },
        u'dnd.featrequiresskill': {
            'Meta': {'object_name': 'FeatRequiresSkill'},
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'feat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'required_skills'", 'to': u"orm['dnd.Feat']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Skill']"})
        },
        u'dnd.featspecialfeatprerequisite': {
            'Meta': {'object_name': 'FeatSpecialFeatPrerequisite'},
            'feat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Feat']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'special_feat_prerequisite': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.SpecialFeatPrerequisite']"}),
            'value_1': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'value_2': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'dnd.item': {
            'Meta': {'ordering': "['name']", 'object_name': 'Item'},
            'activation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.ItemActivationType']", 'null': 'True', 'blank': 'True'}),
            'aura': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.ItemAuraType']", 'null': 'True', 'blank': 'True'}),
            'aura_dc': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'aura_schools': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.SpellSchool']", 'symmetrical': 'False', 'blank': 'True'}),
            'body_slot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.ItemSlot']", 'null': 'True', 'blank': 'True'}),
            'caster_level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cost_to_create': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_bonus': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_gp': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'property': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.ItemProperty']", 'null': 'True', 'blank': 'True'}),
            'required_extra': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'required_feats': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.Feat']", 'symmetrical': 'False', 'blank': 'True'}),
            'required_spells': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.Spell']", 'symmetrical': 'False', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Rulebook']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'synergy_prerequisite': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Item']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'visual_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dnd.itemactivationtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ItemActivationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'dnd.itemauratype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ItemAuraType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'dnd.itemproperty': {
            'Meta': {'ordering': "['name']", 'object_name': 'ItemProperty'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'dnd.itemslot': {
            'Meta': {'ordering': "['name']", 'object_name': 'ItemSlot'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'dnd.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'dnd.monster': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'rulebook'),)", 'object_name': 'Monster'},
            'advancement': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'alignment': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'armor_class': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'attack': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'base_attack': ('django.db.models.fields.SmallIntegerField', [], {}),
            'cha': ('django.db.models.fields.SmallIntegerField', [], {}),
            'challenge_rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'combat': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'combat_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'con': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dex': ('django.db.models.fields.SmallIntegerField', [], {}),
            'environment': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'flat_footed_armor_class': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fort_save': ('django.db.models.fields.SmallIntegerField', [], {}),
            'fort_save_extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'full_attack': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'grapple': ('django.db.models.fields.SmallIntegerField', [], {}),
            'hit_dice': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative': ('django.db.models.fields.SmallIntegerField', [], {}),
            'int': ('django.db.models.fields.SmallIntegerField', [], {}),
            'level_adjustment': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reach': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'reflex_save': ('django.db.models.fields.SmallIntegerField', [], {}),
            'reflex_save_extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Rulebook']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.RaceSize']", 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'space': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'special_attacks': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'special_qualities': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'str': ('django.db.models.fields.SmallIntegerField', [], {}),
            'subtypes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.MonsterSubtype']", 'symmetrical': 'False', 'blank': 'True'}),
            'touch_armor_class': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'treasure': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.MonsterType']"}),
            'will_save': ('django.db.models.fields.SmallIntegerField', [], {}),
            'will_save_extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'wis': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'dnd.monsterhasfeat': {
            'Meta': {'object_name': 'MonsterHasFeat'},
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'feat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Feat']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feats'", 'to': u"orm['dnd.Monster']"})
        },
        u'dnd.monsterhasskill': {
            'Meta': {'object_name': 'MonsterHasSkill'},
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skills'", 'to': u"orm['dnd.Monster']"}),
            'ranks': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Skill']"})
        },
        u'dnd.monsterspeed': {
            'Meta': {'object_name': 'MonsterSpeed'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Monster']"}),
            'speed': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['dnd.RaceSpeedType']"})
        },
        u'dnd.monstersubtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'MonsterSubtype'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'dnd.monstertype': {
            'Meta': {'ordering': "['name']", 'object_name': 'MonsterType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'dnd.newsentry': {
            'Meta': {'ordering': "['-published']", 'object_name': 'NewsEntry'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_html': ('django.db.models.fields.TextField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'dnd.race': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'rulebook'),)", 'object_name': 'Race'},
            'automatic_languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'races_with_automatic'", 'blank': 'True', 'to': u"orm['dnd.Language']"}),
            'bonus_languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'races_with_bonus'", 'blank': 'True', 'to': u"orm['dnd.Language']"}),
            'cha': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'combat': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'combat_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'con': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dex': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'int': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'level_adjustment': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'natural_armor': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'race_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.RaceType']", 'null': 'True', 'blank': 'True'}),
            'racial_hit_dice_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'racial_traits': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'racial_traits_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reach': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Rulebook']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.RaceSize']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'space': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'str': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'wis': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        u'dnd.racefavoredcharacterclass': {
            'Meta': {'object_name': 'RaceFavoredCharacterClass'},
            'character_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.CharacterClass']"}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'favored_classes'", 'to': u"orm['dnd.Race']"})
        },
        u'dnd.racesize': {
            'Meta': {'ordering': "['order']", 'object_name': 'RaceSize'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'dnd.racespeed': {
            'Meta': {'object_name': 'RaceSpeed'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Race']"}),
            'speed': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['dnd.RaceSpeedType']"})
        },
        u'dnd.racespeedtype': {
            'Meta': {'ordering': "['name', 'extra']", 'object_name': 'RaceSpeedType'},
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        u'dnd.racetype': {
            'Meta': {'ordering': "['name']", 'object_name': 'RaceType'},
            'base_attack_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'base_fort_save_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'base_reflex_save_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'base_will_save_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'hit_die_size': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'dnd.rule': {
            'Meta': {'object_name': 'Rule'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_html': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'page_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'page_to': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Rulebook']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'dnd.rulebook': {
            'Meta': {'ordering': "['name']", 'object_name': 'Rulebook'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dnd_edition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.DndEdition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'official_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'published': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        u'dnd.skill': {
            'Meta': {'ordering': "['name']", 'object_name': 'Skill'},
            'armor_check_penalty': ('django.db.models.fields.BooleanField', [], {}),
            'base_skill': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'required_by_feats': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.Feat']", 'through': u"orm['dnd.FeatRequiresSkill']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'trained_only': ('django.db.models.fields.BooleanField', [], {})
        },
        u'dnd.skillvariant': {
            'Meta': {'unique_together': "(('skill', 'rulebook'),)", 'object_name': 'SkillVariant'},
            'action': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'action_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'check': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'check_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'restriction': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'restriction_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Rulebook']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Skill']"}),
            'special': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'special_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'synergy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'synergy_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'try_again': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'try_again_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'untrained': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'untrained_html': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'dnd.specialfeatprerequisite': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpecialFeatPrerequisite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'print_format': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'dnd.spell': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'rulebook'),)", 'object_name': 'Spell'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'arcane_focus_component': ('django.db.models.fields.BooleanField', [], {}),
            'area': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'casting_time': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'class_levels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.CharacterClass']", 'through': u"orm['dnd.SpellClassLevel']", 'symmetrical': 'False'}),
            'corrupt_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'corrupt_level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'descriptors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.SpellDescriptor']", 'symmetrical': 'False', 'blank': 'True'}),
            'divine_focus_component': ('django.db.models.fields.BooleanField', [], {}),
            'domain_levels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dnd.Domain']", 'through': u"orm['dnd.SpellDomainLevel']", 'symmetrical': 'False'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'extra_components': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_component': ('django.db.models.fields.BooleanField', [], {}),
            'meta_breath_component': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'range': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Rulebook']"}),
            'saving_throw': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.SpellSchool']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64'}),
            'somatic_component': ('django.db.models.fields.BooleanField', [], {}),
            'spell_resistance': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'sub_school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.SpellSubSchool']", 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'true_name_component': ('django.db.models.fields.BooleanField', [], {}),
            'verbal_component': ('django.db.models.fields.BooleanField', [], {}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verified_author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'verified_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'xp_component': ('django.db.models.fields.BooleanField', [], {})
        },
        u'dnd.spellclasslevel': {
            'Meta': {'ordering': "['spell', 'level']", 'unique_together': "(('character_class', 'spell'),)", 'object_name': 'SpellClassLevel'},
            'character_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.CharacterClass']"}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'spell': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Spell']"})
        },
        u'dnd.spelldescriptor': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpellDescriptor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'dnd.spelldomainlevel': {
            'Meta': {'ordering': "['spell', 'level']", 'unique_together': "(('domain', 'spell'),)", 'object_name': 'SpellDomainLevel'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Domain']"}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'spell': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Spell']"})
        },
        u'dnd.spellschool': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpellSchool'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'dnd.spellsubschool': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpellSubSchool'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'dnd.staticpage': {
            'Meta': {'object_name': 'StaticPage'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_html': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'dnd.textfeatprerequisite': {
            'Meta': {'ordering': "['text']", 'object_name': 'TextFeatPrerequisite'},
            'feat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dnd.Feat']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['dnd']