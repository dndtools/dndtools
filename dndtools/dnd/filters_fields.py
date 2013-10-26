from django.db.models import Q
import django_filters2


class FeatMultiPrerequisiteFieldFilter(django_filters2.CharFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(
                Q(special_feat_prerequisites__print_format__icontains=value) |
                Q(textfeatprerequisite__text__icontains=value) |
                Q(required_skills__skill__name__icontains=value) |
                Q(required_feats__required_feat__name__icontains=value)
            )
        return qs