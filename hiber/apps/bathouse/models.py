from django import forms
from django.db import models
from django.contrib.postgres.fields import (ArrayField, FloatRangeField,
                                            IntegerRangeField)
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
