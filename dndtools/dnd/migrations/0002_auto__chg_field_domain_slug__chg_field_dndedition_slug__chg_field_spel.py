# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Domain.slug'
        db.alter_column('dnd_domain', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=64))

        # Changing field 'DndEdition.slug'
        db.alter_column('dnd_dndedition', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=32))

        # Changing field 'Spell.slug'
        db.alter_column('dnd_spell', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=64))

        # Changing field 'CharacterClass.slug'
        db.alter_column('dnd_characterclass', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=64))

        # Changing field 'Rulebook.slug'
        db.alter_column('dnd_rulebook', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=64))

        # Changing field 'SpellSubSchool.slug'
        db.alter_column('dnd_spellsubschool', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=32))

        # Changing field 'SpellSchool.slug'
        db.alter_column('dnd_spellschool', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=32))

        # Changing field 'SpellDescriptor.slug'
        db.alter_column('dnd_spelldescriptor', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=64))


    def backwards(self, orm):
        
        # Changing field 'Domain.slug'
        db.alter_column('dnd_domain', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=72))

        # Changing field 'DndEdition.slug'
        db.alter_column('dnd_dndedition', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=40))

        # Changing field 'Spell.slug'
        db.alter_column('dnd_spell', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=72))

        # Changing field 'CharacterClass.slug'
        db.alter_column('dnd_characterclass', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=72))

        # Changing field 'Rulebook.slug'
        db.alter_column('dnd_rulebook', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=72))

        # Changing field 'SpellSubSchool.slug'
        db.alter_column('dnd_spellsubschool', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=40))

        # Changing field 'SpellSchool.slug'
        db.alter_column('dnd_spellschool', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=40))

        # Changing field 'SpellDescriptor.slug'
        db.alter_column('dnd_spelldescriptor', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=72))


    models = {
        'dnd.characterclass': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'rulebook'),)", 'object_name': 'CharacterClass'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'prestige': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Rulebook']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'})
        },
        'dnd.dndedition': {
            'Meta': {'ordering': "['name']", 'object_name': 'DndEdition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'db_index': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'dnd.domain': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'rulebook'),)", 'object_name': 'Domain'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Rulebook']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'db_index': 'True'})
        },
        'dnd.spellsubschool': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpellSubSchool'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'db_index': 'True'})
        }
    }

    complete_apps = ['dnd']
