# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DndEdition'
        db.create_table('dnd_dndedition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('system', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=40, db_index=True)),
        ))
        db.send_create_signal('dnd', ['DndEdition'])

        # Adding model 'Rulebook'
        db.create_table('dnd_rulebook', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dnd_edition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.DndEdition'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('abbr', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('img_url', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('official_url', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=72, db_index=True)),
        ))
        db.send_create_signal('dnd', ['Rulebook'])

        # Adding model 'CharacterClass'
        db.create_table('dnd_characterclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('page', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=72, db_index=True)),
            ('prestige', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('dnd', ['CharacterClass'])

        # Adding unique constraint on 'CharacterClass', fields ['name', 'rulebook']
        db.create_unique('dnd_characterclass', ['name', 'rulebook_id'])

        # Adding model 'Domain'
        db.create_table('dnd_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('page', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=72, db_index=True)),
        ))
        db.send_create_signal('dnd', ['Domain'])

        # Adding unique constraint on 'Domain', fields ['name', 'rulebook']
        db.create_unique('dnd_domain', ['name', 'rulebook_id'])

        # Adding model 'SpellDescriptor'
        db.create_table('dnd_spelldescriptor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=72, db_index=True)),
        ))
        db.send_create_signal('dnd', ['SpellDescriptor'])

        # Adding model 'SpellSchool'
        db.create_table('dnd_spellschool', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=40, db_index=True)),
        ))
        db.send_create_signal('dnd', ['SpellSchool'])

        # Adding model 'SpellSubSchool'
        db.create_table('dnd_spellsubschool', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=40, db_index=True)),
        ))
        db.send_create_signal('dnd', ['SpellSubSchool'])

        # Adding model 'Spell'
        db.create_table('dnd_spell', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rulebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Rulebook'])),
            ('page', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.SpellSchool'])),
            ('sub_school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.SpellSubSchool'], null=True, blank=True)),
            ('verbal_component', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('somatic_component', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('material_component', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('arcane_focus_component', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('divine_focus_component', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('xp_component', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('casting_time', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('range', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('effect', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('saving_throw', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('spell_resistance', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=72, db_index=True)),
        ))
        db.send_create_signal('dnd', ['Spell'])

        # Adding unique constraint on 'Spell', fields ['name', 'rulebook']
        db.create_unique('dnd_spell', ['name', 'rulebook_id'])

        # Adding M2M table for field descriptors on 'Spell'
        db.create_table('dnd_spell_descriptors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('spell', models.ForeignKey(orm['dnd.spell'], null=False)),
            ('spelldescriptor', models.ForeignKey(orm['dnd.spelldescriptor'], null=False))
        ))
        db.create_unique('dnd_spell_descriptors', ['spell_id', 'spelldescriptor_id'])

        # Adding model 'SpellClassLevel'
        db.create_table('dnd_spellclasslevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.CharacterClass'])),
            ('spell', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Spell'])),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('dnd', ['SpellClassLevel'])

        # Adding unique constraint on 'SpellClassLevel', fields ['character_class', 'spell']
        db.create_unique('dnd_spellclasslevel', ['character_class_id', 'spell_id'])

        # Adding model 'SpellDomainLevel'
        db.create_table('dnd_spelldomainlevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Domain'])),
            ('spell', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dnd.Spell'])),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('dnd', ['SpellDomainLevel'])

        # Adding unique constraint on 'SpellDomainLevel', fields ['domain', 'spell']
        db.create_unique('dnd_spelldomainlevel', ['domain_id', 'spell_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'SpellDomainLevel', fields ['domain', 'spell']
        db.delete_unique('dnd_spelldomainlevel', ['domain_id', 'spell_id'])

        # Removing unique constraint on 'SpellClassLevel', fields ['character_class', 'spell']
        db.delete_unique('dnd_spellclasslevel', ['character_class_id', 'spell_id'])

        # Removing unique constraint on 'Spell', fields ['name', 'rulebook']
        db.delete_unique('dnd_spell', ['name', 'rulebook_id'])

        # Removing unique constraint on 'Domain', fields ['name', 'rulebook']
        db.delete_unique('dnd_domain', ['name', 'rulebook_id'])

        # Removing unique constraint on 'CharacterClass', fields ['name', 'rulebook']
        db.delete_unique('dnd_characterclass', ['name', 'rulebook_id'])

        # Deleting model 'DndEdition'
        db.delete_table('dnd_dndedition')

        # Deleting model 'Rulebook'
        db.delete_table('dnd_rulebook')

        # Deleting model 'CharacterClass'
        db.delete_table('dnd_characterclass')

        # Deleting model 'Domain'
        db.delete_table('dnd_domain')

        # Deleting model 'SpellDescriptor'
        db.delete_table('dnd_spelldescriptor')

        # Deleting model 'SpellSchool'
        db.delete_table('dnd_spellschool')

        # Deleting model 'SpellSubSchool'
        db.delete_table('dnd_spellsubschool')

        # Deleting model 'Spell'
        db.delete_table('dnd_spell')

        # Removing M2M table for field descriptors on 'Spell'
        db.delete_table('dnd_spell_descriptors')

        # Deleting model 'SpellClassLevel'
        db.delete_table('dnd_spellclasslevel')

        # Deleting model 'SpellDomainLevel'
        db.delete_table('dnd_spelldomainlevel')


    models = {
        'dnd.characterclass': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'rulebook'),)", 'object_name': 'CharacterClass'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'prestige': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Rulebook']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '72', 'db_index': 'True'})
        },
        'dnd.dndedition': {
            'Meta': {'ordering': "['name']", 'object_name': 'DndEdition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'db_index': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'dnd.domain': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'rulebook'),)", 'object_name': 'Domain'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Rulebook']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '72', 'db_index': 'True'})
        },
        'dnd.rulebook': {
            'Meta': {'ordering': "['name']", 'object_name': 'Rulebook'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dnd_edition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.DndEdition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'official_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '72', 'db_index': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'dnd.spell': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'rulebook'),)", 'object_name': 'Spell'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'arcane_focus_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'area': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'casting_time': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'class_levels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dnd.CharacterClass']", 'through': "orm['dnd.SpellClassLevel']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'descriptors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dnd.SpellDescriptor']", 'symmetrical': 'False', 'blank': 'True'}),
            'divine_focus_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'domain_levels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dnd.Domain']", 'through': "orm['dnd.SpellDomainLevel']", 'symmetrical': 'False'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'range': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Rulebook']"}),
            'saving_throw': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.SpellSchool']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '72', 'db_index': 'True'}),
            'somatic_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spell_resistance': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'sub_school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.SpellSubSchool']", 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'verbal_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'xp_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'dnd.spellclasslevel': {
            'Meta': {'ordering': "['spell', 'level']", 'unique_together': "(('character_class', 'spell'),)", 'object_name': 'SpellClassLevel'},
            'character_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.CharacterClass']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'spell': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Spell']"})
        },
        'dnd.spelldescriptor': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpellDescriptor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '72', 'db_index': 'True'})
        },
        'dnd.spelldomainlevel': {
            'Meta': {'ordering': "['spell', 'level']", 'unique_together': "(('domain', 'spell'),)", 'object_name': 'SpellDomainLevel'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Domain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'spell': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Spell']"})
        },
        'dnd.spellschool': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpellSchool'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'db_index': 'True'})
        },
        'dnd.spellsubschool': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpellSubSchool'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'db_index': 'True'})
        }
    }

    complete_apps = ['dnd']
