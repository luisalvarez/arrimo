from django.contrib import admin
from datos_familiares.models import Relative, Person, RelativeType
from import_export.admin import ImportExportActionModelAdmin as ModelAdminImportExport


class RelativeAdminInline(admin.TabularInline):
    fields = ('name', 'relationship', 'is_dead', 'death_date')
    model = Relative
    extra = 0


class RelativeTypeAdmin(ModelAdminImportExport):
    list_display_links = ('name',)
    list_display = ('name',)
    search_fields = ('name',)


class RelativeAdmin(ModelAdminImportExport):
    list_display = ('name', 'relationship', 'person', 'is_dead', 'death_date')
    list_display_links = ('name', 'relationship', 'person', )
    list_filter = ('is_dead', 'relationship', 'death_date')
    raw_id_fields = ('person',)
    search_fields = ('person__licence','person__short_licence' , 'name', 'person__identification',)


class PersonAdmin(ModelAdminImportExport):

    list_display = ('licence', 'name', 'identification')
    list_display_links = ('licence', 'name', 'identification')
    search_fields = ('licence', 'name', 'identification', 'short_licence')
    inlines = [RelativeAdminInline]
    readonly_fields = ('licence', 'name')
    fieldsets = (
        ('Empleado', {
            'fields': ('licence', 'name')
        }),
    )


admin.site.register(Relative, RelativeAdmin)
admin.site.register(RelativeType, RelativeTypeAdmin)
admin.site.register(Person, PersonAdmin)
