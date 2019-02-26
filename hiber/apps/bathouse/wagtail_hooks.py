from wagtail.contrib.modeladmin.options import (ModelAdmin,
                                                modeladmin_register)

from hiber.apps.bathouse.models import Bat


class BatModelAdmin(ModelAdmin):
    model = Bat
    menu_label = 'Bats'
    menu_order = 000
    add_to_settings_menu = False
    exclude_from_explorer = False


modeladmin_register(BatModelAdmin)
