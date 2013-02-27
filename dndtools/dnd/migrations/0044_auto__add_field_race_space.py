# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Race.space'
        db.add_column('dnd_race', 'space', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=5), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Race.space'
        db.delete_column('dnd_race', 'space')


    models = {
        'dnd.characterclass': {
            'Meta': {'ordering': "['name']", 'object_name': 'CharacterClass'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'prestige': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        'dnd.characterclassvariant': {
            'Meta': {'unique_together': "(('character_class', 'rulebook'),)", 'object_name': 'CharacterClassVariant'},
            'advancement': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'advancement_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'character_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.CharacterClass']"}),
            'class_features': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'class_skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dnd.Skill']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Rulebook']"}),
            'skill_points': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'dnd.dndedition': {
            'Meta': {'ordering': "['name']", 'object_name': 'DndEdition'},
            'core': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'dnd.domain': {
            'Meta': {'ordering': "['name']", 'object_name': 'Domain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        'dnd.feat': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'rulebook'),)", 'object_name': 'Feat'},
            'benefit': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feat_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dnd.FeatCategory']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'normal': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Rulebook']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'}),
            'special': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'special_feat_prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dnd.SpecialFeatPrerequisite']", 'through': "orm['dnd.FeatSpecialFeatPrerequisite']", 'symmetrical': 'False'})
        },
        'dnd.featcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'FeatCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'})
        },
        'dnd.featrequiresfeat': {
            'Meta': {'object_name': 'FeatRequiresFeat'},
            'additional_text': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'required_feat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'required_by_feats'", 'to': "orm['dnd.Feat']"}),
            'source_feat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'required_feats'", 'to': "orm['dnd.Feat']"})
        },
        'dnd.featrequiresskill': {
            'Meta': {'object_name': 'FeatRequiresSkill'},
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'feat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'required_skills'", 'to': "orm['dnd.Feat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Skill']"})
        },
        'dnd.featspecialfeatprerequisite': {
            'Meta': {'object_name': 'FeatSpecialFeatPrerequisite'},
            'feat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Feat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'special_feat_prerequisite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.SpecialFeatPrerequisite']"}),
            'value_1': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'value_2': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'dnd.race': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'rulebook'),)", 'object_name': 'Race'},
            'base_land_speed': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30'}),
            'cha': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'con': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'dex': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'level_adjustment': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Rulebook']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.RaceSize']", 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'db_index': 'True'}),
            'space': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'str': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'wis': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'dnd.racefavoredcharacterclass': {
            'Meta': {'object_name': 'RaceFavoredCharacterClass'},
            'character_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.CharacterClass']"}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'favored_classes'", 'to': "orm['dnd.Race']"})
        },
        'dnd.racesize': {
            'Meta': {'ordering': "['order']", 'object_name': 'RaceSize'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'dnd.rulebook': {
            'Meta': {'ordering': "['name']", 'object_name': 'Rulebook'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dnd_edition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.DndEdition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'official_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'published': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'dnd.skill': {
            'Meta': {'ordering': "['name']", 'object_name': 'Skill'},
            'armor_check_penalty': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'base_skill': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'required_by_feats': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dnd.Feat']", 'through': "orm['dnd.FeatRequiresSkill']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'trained_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'dnd.specialfeatprerequisite': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpecialFeatPrerequisite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'print_format': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
            'extra_components': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_breath_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'range': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'rulebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Rulebook']"}),
            'saving_throw': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.SpellSchool']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'}),
            'somatic_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spell_resistance': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'sub_school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.SpellSubSchool']", 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'true_name_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verbal_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'xp_component': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'dnd.spellclasslevel': {
            'Meta': {'ordering': "['spell', 'level']", 'unique_together': "(('character_class', 'spell'),)", 'object_name': 'SpellClassLevel'},
            'character_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.CharacterClass']"}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'spell': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Spell']"})
        },
        'dnd.spelldescriptor': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpellDescriptor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        'dnd.spelldomainlevel': {
            'Meta': {'ordering': "['spell', 'level']", 'unique_together': "(('domain', 'spell'),)", 'object_name': 'SpellDomainLevel'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Domain']"}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'spell': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Spell']"})
        },
        'dnd.spellschool': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpellSchool'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'})
        },
        'dnd.spellsubschool': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpellSubSchool'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'})
        },
        'dnd.textfeatprerequisite': {
            'Meta': {'ordering': "['text']", 'object_name': 'TextFeatPrerequisite'},
            'feat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dnd.Feat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['dnd']
