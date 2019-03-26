from django.contrib.auth.models import User
from drf_extra_fields.fields import FloatRangeField, IntegerRangeField
from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from ..bathouse.models import Bat


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self._choices[obj]


class BatSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: Get current image to display an absolute path over API
    rarity = ChoiceField(choices=Bat.RARITY_CHOICES)
    habits = serializers.ListField(
        child=ChoiceField(choices=Bat.HABIT_CHOICES))
    size = FloatRangeField()
    pups = IntegerRangeField()
    risk = serializers.ListField(child=ChoiceField(choices=Bat.RISK_CHOICES))
    risk_scope = serializers.ListField(
        child=ChoiceField(choices=Bat.SCOPE_CHOICES))
    bat_image = ImageRenditionField('fill-200x200')

    class Meta:
        model = Bat
        fields = ('id', 'common_name', 'scientific_name', 'rarity', 'habits',
                  'size', 'pups', 'risk', 'risk_scope', 'bat_image')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')
