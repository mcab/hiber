import collections
from django.utils import timezone
from drf_extra_fields.fields import FloatRangeField, IntegerRangeField
from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from ..bathouse.models import (Bat, House, HouseEnvironmentFeatures,
                               HousePhysicalFeatures, Observation)

OTHER = "OT"


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self._choices[obj]


class ConditionalRequiredMixin:
    """
    Adds flexibility to required fields by setting up
    `conditional_required_fields`

    For example:
    conditional_required_fields = [
        ('property_type', {
            'condition': OTHER,
            'required_fields': ['other_property_type']
        })
    ]

    If property_type == OTHER, then fields in required_fields are required.

    """
    REQUIRED_MSG = "Field is required due to {} being {}."
    conditional_required_fields = []

    def validate(self, attrs):
        attrs = super().validate(attrs)
        for master_field, conditions in self.conditional_required_fields:
            master_field_value = attrs.get(master_field)
            condition = conditions['condition']
            if not isinstance(condition, str) and isinstance(
                    condition, collections.Iterable):
                trigger = master_field_value in condition
            else:
                trigger = master_field_value == condition

            if trigger:
                additional_required_fields = conditions['required_fields']
                absent_fields = [
                    f for f in additional_required_fields
                    if attrs.get(f) is None
                ]
                if absent_fields:
                    error_dict = {
                        f: self.REQUIRED_MSG.format(master_field, condition)
                        for f in absent_fields
                    }
                    raise serializers.ValidationError(error_dict)
        return attrs


class BatSerializer(serializers.ModelSerializer):
    # TODO: Get current image to display an absolute path over API
    id = serializers.ReadOnlyField()
    rarity = ChoiceField(choices=Bat.RARITY_CHOICES)
    habits = serializers.ListField(child=ChoiceField(
        choices=Bat.HABIT_CHOICES))
    size = FloatRangeField()
    pups = IntegerRangeField()
    risk = serializers.ListField(child=ChoiceField(choices=Bat.RISK_CHOICES))
    risk_scope = serializers.ListField(child=ChoiceField(
        choices=Bat.SCOPE_CHOICES))
    bat_image = ImageRenditionField('fill-200x200')

    class Meta:
        model = Bat
        fields = ('id', 'common_name', 'scientific_name', 'rarity', 'habits',
                  'size', 'pups', 'risk', 'risk_scope', 'bat_image')


class HouseSerializer(ConditionalRequiredMixin, serializers.ModelSerializer):
    conditional_required_fields = [('property_type', {
        'condition': OTHER,
        'required_fields': ['other_property_type']
    })]
    id = serializers.ReadOnlyField()
    watcher = serializers.ReadOnlyField(source='watcher.username')
    location = PointField()
    property_type = ChoiceField(
        choices=House._meta.get_field('property_type').choices)
    created = serializers.DateTimeField(default=serializers.CreateOnlyDefault(
        timezone.now()),
                                        read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = House
        fields = ('__all__')
        read_only_fields = ('id', 'watcher', 'created', 'updated')


class HouseEnvironmentFeaturesSerializer(ConditionalRequiredMixin,
                                         serializers.ModelSerializer):
    conditional_required_fields = [
        ('habitat_degradation', {
            'condition': OTHER,
            'required_fields': ['other_habitat_degradation']
        }),
        ('habitat_type', {
            'condition': OTHER,
            'required_fields': ['other_habitat_type']
        }),
        ('man_made_structure', {
            'condition': OTHER,
            'required_fields': ['other_man_made_structure']
        }),
        ('noise_disturbance', {
            'condition': OTHER,
            'required_fields': ['other_noise_disturbance']
        }),
        ('nearest_water_resources', {
            'condition': OTHER,
            'required_fields': ['other_nearest_water_resource']
        })
    ]
    id = serializers.ReadOnlyField()
    house_id = serializers.ReadOnlyField()
    habitat_degradation = serializers.ListField(child=ChoiceField(
        choices=HouseEnvironmentFeatures.HABITAT_DEGRADATION_CHOICES))
    habitat_type = serializers.ListField(child=ChoiceField(
        choices=HouseEnvironmentFeatures.HABITAT_TYPE_CHOICES))
    man_made_structure = serializers.ListField(child=ChoiceField(
        choices=HouseEnvironmentFeatures.MAN_MADE_STRUCTURE_CHOICES))
    nearby_geography = serializers.ListField(child=ChoiceField(
        choices=HouseEnvironmentFeatures.NEARBY_GEOGRAPHY_CHOICES))
    slope = ChoiceField(
        choices=HouseEnvironmentFeatures._meta.get_field('slope').choices)
    day_noise = ChoiceField(
        choices=HouseEnvironmentFeatures._meta.get_field('day_noise').choices)
    night_noise = ChoiceField(choices=HouseEnvironmentFeatures._meta.get_field(
        'night_noise').choices)
    noise_disturbance = serializers.ListField(child=ChoiceField(
        choices=HouseEnvironmentFeatures.NOISE_DISTURBANCE_CHOICES))
    night_light_pollution_amount = ChoiceField(
        choices=HouseEnvironmentFeatures._meta.get_field(
            'night_light_pollution_amount').choices)
    night_light_pollution_consistency = ChoiceField(
        choices=HouseEnvironmentFeatures._meta.get_field(
            'night_light_pollution_consistency').choices)
    nearest_water_resources = ChoiceField(
        choices=HouseEnvironmentFeatures._meta.get_field(
            'nearest_water_resources').choices)
    water_resource_units = ChoiceField(
        choices=HouseEnvironmentFeatures._meta.get_field(
            'water_resource_units').choices)
    other_features = serializers.CharField(required=False)

    def create(self, validated_data):
        house = House.objects.get(pk=self.context["view"].kwargs["house_pk"])
        validated_data["house"] = house
        return HouseEnvironmentFeatures.objects.create(**validated_data)

    class Meta:
        model = HouseEnvironmentFeatures
        fields = ('__all__')


class HousePhysicalFeaturesSerializer(ConditionalRequiredMixin,
                                      serializers.ModelSerializer):
    conditional_required_fields = [('color', {
        'condition': OTHER,
        'required_fields': ['other_color']
    }),
                                   ('mounted_on', {
                                       'condition': OTHER,
                                       'required_fields': ['other_mounted_on']
                                   })]
    id = serializers.ReadOnlyField()
    house_id = serializers.ReadOnlyField()
    house_size = ChoiceField(
        choices=HousePhysicalFeatures._meta.get_field('house_size').choices)
    color = ChoiceField(
        choices=HousePhysicalFeatures._meta.get_field('color').choices)
    direction = ChoiceField(
        choices=HousePhysicalFeatures._meta.get_field('direction').choices)
    mounted_on = ChoiceField(
        choices=HousePhysicalFeatures._meta.get_field('mounted_on').choices)

    def create(self, validated_data):
        house = House.objects.get(pk=self.context["view"].kwargs["house_pk"])
        validated_data["house"] = house
        return HousePhysicalFeatures.objects.create(**validated_data)

    class Meta:
        model = HousePhysicalFeatures
        fields = ('__all__')


class ObservationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    house_id = serializers.ReadOnlyField()
    acoustic_monitor = ChoiceField(
        choices=Observation._meta.get_field('acoustic_monitor').choices)

    def create(self, validated_data):
        house = House.objects.get(pk=self.context["view"].kwargs["house_pk"])
        validated_data["house"] = house
        return Observation.objects.create(**validated_data)

    class Meta:
        model = Observation
        fields = ('__all__')
