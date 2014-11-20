# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from dnd.models import (
    Spell, DndEdition, Rulebook, CharacterClass, Domain, SpellDescriptor,
    SpellSchool, SpellSubSchool, FeatCategory, Feat, CharacterClassVariant,
    Skill)



class DndEditionSitemap(Sitemap):
    def items(self):
        return DndEdition.objects.all()


class RulebookSitemap(Sitemap):
    def items(self):
        return Rulebook.objects.select_related('dnd_edition').all()


class CharacterClassSitemap(Sitemap):
    def items(self):
        return CharacterClass.objects.all()


class CharacterClassVariantSitemap(Sitemap):
    def items(self):
        return CharacterClassVariant.objects.select_related('rulebook').all()


class DomainSitemap(Sitemap):
    def items(self):
        return Domain.objects.all()


class SpellDescriptorSitemap(Sitemap):
    def items(self):
        return SpellDescriptor.objects.all()


class SpellSchoolSitemap(Sitemap):
    def items(self):
        return SpellSchool.objects.all()


class SpellSubSchoolSitemap(Sitemap):
    def items(self):
        return SpellSubSchool.objects.all()


class SpellSitemap(Sitemap):
    def items(self):
        return Spell.objects.select_related('rulebook').all()


class FeatCategorySitemap(Sitemap):
    def items(self):
        return FeatCategory.objects.all()


class SkillSitemap(Sitemap):
    def items(self):
        return Skill.objects.all()


class FeatSitemap(Sitemap):
    def items(self):
        return Feat.objects.select_related('rulebook',
                                           'rulebook__edition').all()


sitemaps = {
    'Rulebook': RulebookSitemap,
    'CharacterClass': CharacterClassSitemap,
    'CharacterClassVariant': CharacterClassVariantSitemap,
    'Domain': DomainSitemap,
    'SpellDescriptor': SpellDescriptorSitemap,
    'SpellSchool': SpellSchoolSitemap,
    'SpellSubSchool': SpellSubSchoolSitemap,
    'Spell': SpellSitemap,
    'FeatCategory': FeatCategorySitemap,
    'Feat': FeatSitemap,
    'Skill': SkillSitemap,
    }