from django import forms
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.postgres.fields import (ArrayField, FloatRangeField,
                                            IntegerRangeField)
from django.core.validators import MinValueValidator, MaxValueValidator
from wagtail.admin.edit_handlers import (MultiFieldPanel, FieldRowPanel,
                                         FieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.
    Uses Django's Postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)


class Bat(models.Model):
    """
    Describes a model that has all the traits for a bat.

    This is consumed on the front-end to show species of bats to the user,
    as well as a way to tag what bats were seen at a particular House.
    """
    common_name = models.CharField(
        max_length=255, help_text="Name used in everyday life")
    scientific_name = models.CharField(
        max_length=255, help_text="Formal system used for naming species")

    RARITY_CHOICES = (('CO', 'Common'), ('SC', 'Seasonally Common'), ('RA',
                                                                      'Rare'))

    rarity = models.CharField(
        max_length=2,
        choices=RARITY_CHOICES,
        default='CO',
        help_text="How often the species is seen")

    HABIT_CHOICES = (('HI', 'Hibernates'), ('MI', 'Migrates'),
                     ('CR', 'Cave roosts'), ('TR', 'Tree roosts'))

    habits = ChoiceArrayField(
        models.CharField(max_length=2, choices=HABIT_CHOICES),
        blank=True,
        help_text="What the species tends to do in order to survive")

    size = FloatRangeField(help_text="Typical size in inches")
    pups = IntegerRangeField(help_text="Typical offspring per year")

    RISK_CHOICES = (('NT', 'Not threatened'), ('EN', 'Endangered'),
                    ('TH', 'Threatened'), ('SC', 'Special concern'))

    risk = ChoiceArrayField(
        models.CharField(max_length=2, choices=RISK_CHOICES),
        blank=True,
        help_text="Conservation status for the species")

    SCOPE_CHOICES = (('ST', 'State'), ('FE', 'Federally'))

    risk_scope = ChoiceArrayField(
        models.CharField(max_length=2, choices=SCOPE_CHOICES, null=True),
        blank=True,
        null=True,
        help_text="Whether or not this applies at the federal or state level")

    bat_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('common_name', classname="col12"),
            FieldPanel('scientific_name', classname="col12"),
        ],
                        heading="Identification",
                        classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('rarity', classname="col12"),
            FieldPanel(
                'habits',
                classname="col12",
                widget=forms.CheckboxSelectMultiple),
            FieldPanel(
                'risk', classname="col12",
                widget=forms.CheckboxSelectMultiple),
            FieldPanel(
                'risk_scope',
                classname="col12",
                widget=forms.CheckboxSelectMultiple),
        ],
                        heading="Information",
                        classname="collapsible"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('size', classname="col6"),
                FieldPanel('pups', classname="col6"),
            ])
        ],
                        heading="Characteristics",
                        classname="collapsible"),
        ImageChooserPanel('bat_image')
    ]

    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})"


class House(models.Model):
    """
    Describes a model that has administrative information of a bat house.

    Includes the information for current watcher, house location, and datetime
    information about the record.

    Since it's assumed that the bat house will not move towns nor change
    property types, they are included in here as well.
    """
    watcher = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        help_text="User that provides survey data for the bat house")
    location = models.PointField(
        help_text="Point that indicates where the bat house is located",
        verbose_name="geographical location")
    town_name = models.CharField(
        blank=True,
        max_length=255,
        help_text="Town where bat house is located",
        verbose_name="town location")
    property_type = models.CharField(
        default='OT',
        max_length=2,
        choices=(('ST', 'State'), ('TO', 'Town'), ('SC', 'School'),
                 ('LT', 'Land Trust'), ('PR', 'Private'), ('OT', 'Other')),
        help_text="Property type where bat house is located")
    other_property_type = models.CharField(
        max_length=255,
        blank=True,
        help_text="Property type if Other was selected")
    created = models.DateTimeField(
        auto_now_add=True, help_text="Date when House was created")
    updated = models.DateTimeField(
        auto_now=True, help_text="Date when House was updated")


class HouseEnvironmentFeatures(models.Model):
    """
    Describes a model that contains information about the environmental
    surroundings of the house. This includes habitats nearby, man-made
    structures, geography, noise nearby, light created, water sources,
    and sunlight.
    """
    house = models.OneToOneField(
        House, on_delete=models.CASCADE, primary_key=True)

    # Standing under the bat house and looking in all directions, select all...
    habitat_degradation = ArrayField(
        base_field=models.CharField(
            max_length=2,
            choices=(
                ('DU', 'Dumping'),
                ('ER', 'Erosion'),
                ('TR', 'Trash'),
                ('NO', 'None'),
                ('OT', 'Other'),
            )),
        help_text="Habitat degradation present around the bat house")
    other_habitat_degradation = models.CharField(
        max_length=255,
        blank=True,
        help_text="Habitat degradation if Other was selected")
    habitat_type = ArrayField(
        base_field=models.CharField(
            max_length=2,
            choices=(('DE', 'Development'), ('FE', 'Forest Edge'),
                     ('FG', 'Forest Gap'), ('FI', 'Field'), ('SR',
                                                             'Stream/River'),
                     ('WP', 'Wetland/Pond'), ('OT', 'Other'))),
        help_text="Type of environment around the bat house")
    other_habitat_type = models.CharField(
        max_length=255,
        blank=True,
        help_text="Habitat type if Other was selected")
    man_made_structure = ArrayField(
        base_field=models.CharField(
            max_length=2,
            choices=(
                ('BU', 'Building'),
                ('BR', 'Bridge'),
                ('DA', 'Dam'),
                ('DR', 'Dirt Road'),
                ('FE', 'Fence'),
                ('PR', 'Paved Roads'),
                ('TR', 'Trail'),
                ('NO', 'None'),
                ('OT', 'Other'),
            )),
        help_text="Man-made structures present around the bat house")
    other_man_made_structure = models.CharField(
        max_length=255,
        blank=True,
        help_text="Man-made structures present if Other was selected")
    nearby_geography = ArrayField(
        base_field=models.CharField(
            max_length=2,
            choices=(('VB', 'Valley or Bottomland Hillside'),
                     ('RI', 'Ridgetop'), ('PL', 'Plane (Flat Area)'))),
        help_text="Nearby geography of the area around the bat house")
    slope = models.CharField(
        max_length=1,
        choices=(
            ('F', 'Flat'),
            ('G', 'Gentle'),
            ('U', 'Undulating'),
            ('S', 'Steep'),
        ),
        help_text="Type of slope the bat house is on")
    tree_type = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(5)],
        help_text="Types of trees surrounding the bat house")

    # Noise information
    day_noise = models.CharField(
        max_length=1,
        choices=(
            ('L', 'Loud'),
            ('M', 'Medium'),
            ('Q', 'Quiet'),
        ),
        help_text="Noise around the bat house throughout the day")
    night_noise = models.CharField(
        max_length=1,
        choices=(
            ('L', 'Loud'),
            ('M', 'Medium'),
            ('Q', 'Quiet'),
        ),
        help_text="Noise around the bat house throughout the night")
    noise_disturbance = ArrayField(
        base_field=models.CharField(
            max_length=2,
            choices=(
                ('BI', 'Businesses/Industry'),
                ('CA', 'Cars'),
                ('PR', 'People/Residential'),
                ('NO', 'None'),
                ('OT', 'Other'),
            )),
        help_text="Noise disturbances around the bat house")
    other_noise_disturbance = models.CharField(
        max_length=255,
        blank=True,
        help_text="Noise disturbances if Other was selected")
    submitted = models.DateTimeField(auto_now_add=True)

    # Man-made light at night
    night_light_pollution_amount = models.CharField(
        max_length=1,
        choices=(('A', 'A lot'), ('M', 'Medium'), ('L', 'Low'), ('N', 'None')),
        help_text="Light pollution amount at night around the bat house")
    night_light_pollution_consistency = models.CharField(
        max_length=1,
        choices=(('T', 'Throughout'), ('I', 'Inconsistent')),
        help_text="Light pollution consistency at night around the bat house")

    # Water resources
    nearest_water_resources = models.CharField(
        max_length=2,
        choices=(
            ('CW', 'Coastal Wetland'),
            ('IW', 'Inland Wetland'),
            ('LA', 'Lake'),
            ('PO', 'Pond'),
            ('RI', 'River'),
            ('ST', 'Stream'),
            ('VP', 'Vernal Pool'),
            ('NO', 'None'),
            ('OT', 'Other'),
        ),
        help_text="Nearest water resource to the bat house")
    other_nearest_water_resource = models.CharField(
        max_length=255,
        blank=True,
        help_text="Water resource if Other was selected")
    water_resource_distance = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Distance to nearest water resource")
    water_resource_units = models.CharField(
        max_length=2,
        choices=(
            ('FT', 'Feet'),
            ('KM', 'Kilometers'),
            ('ME', 'Meters'),
            ('MI', 'Miles'),
        ),
        help_text="Units of distance to nearest water resource")

    # Sunlight on bat house
    morning_sunlight = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Amount of hours of morning sunlight the bat house receives")
    afternoon_sunlight = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Amount of hours of afternoon sunlight the bat house \
        receives")

    other_features = models.TextField(
        help_text="Other environmental features not covered")


class HousePhysicalFeatures(models.Model):
    """
    Describes a model that has all information regarding the physical
    characteristics of the bat house, including size, amount of chambers, etc.
    """

    house = models.OneToOneField(
        House, on_delete=models.CASCADE, primary_key=True)
    house_size = models.CharField(
        max_length=1,
        choices=(
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
        ),
        help_text="Approximate size of the bat house")
    color = models.CharField(
        max_length=2,
        choices=(
            ('BL', 'Black'),
            ('DB', 'Dark brown'),
            ('MB', 'Medium brown'),
            ('LB', 'Light brown'),
            ('TB', 'Tan/Beige'),
            ('NW', 'Natural wood'),
            ('WH', 'White'),
            ('OT', 'Other'),
        ),
        help_text="Color of bat house")
    other_color = models.CharField(
        blank=True,
        max_length=255,
        help_text="Color of bat house if Other is specified")
    chambers = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of chambers in bat house")
    direction = models.CharField(
        max_length=2,
        choices=(
            ('NO', 'North'),
            ('NE', 'Northeast'),
            ('EA', 'East'),
            ('SE', 'Southeast'),
            ('SO', 'South'),
            ('SW', 'Southwest'),
            ('WE', 'West'),
            ('NW', 'Northwest'),
        ),
        help_text="Direction which bat house is facing")
    mounted_on = models.CharField(
        max_length=2,
        choices=(
            ('BB', 'Back to back'),
            ('BD', 'Building'),
            ('PI', 'Pole by itself'),
            ('PI', 'Pole with another bat house'),
            ('TR', 'Tree'),
            ('OT', 'Other'),
        ),
        help_text="Item which bat house is mounted to")
    other_mounted_on = models.CharField(
        blank=True,
        max_length=255,
        help_text="Mount type if Other is specified")
    ground_height = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Height above the ground surface (in feet)")
    installed = models.DateField(
        help_text="Date when the bat house was installed")


class Observation(models.Model):
    """
    Describes a model that a user will submit about observations for the
    presence of bats in their bat house.
    """

    house = models.OneToOneField(
        House, on_delete=models.CASCADE, primary_key=True)

    checked = models.DateTimeField(
        help_text="Date and when the bat house was checked")
    present = models.BooleanField(
        verbose_name="bat presence",
        help_text="True if bats were there, False otherwise")
    occupants = models.IntegerField(
        blank=True, help_text="Amount of bats present in the bat house")
    acoustic_monitor = models.CharField(
        max_length=1,
        choices=(('Y', 'Yes'), ('N', 'No'), ('U', 'Unsure')),
        help_text="Has a bat biologist came to setup acoustic monitoring around \
            the bat house?")
    notes = models.TextField(
        blank=True, help_text="Other notes about observations")
