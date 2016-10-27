from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.contrib import admin
from parametros_generales.models import Commodity, Employee, Inspector, Shipping, Vapor, EmployeeHistory, \
    RelativeHistory
from datos_familiares.models import Relative
from parametros_generales.forms import EmployeeForm
from import_export.admin import ImportExportActionModelAdmin as ModelAdminImportExport
from parametros_generales import resources
from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from django.core import urlresolvers


class CommodityAdmin(ModelAdminImportExport):
    list_display = ('code', 'name', 'status')
    search_fields = ('code', 'name', 'export_price', 'transit_price', 'import_price')
    list_display_links = ('code', 'name')
    list_filter = ('status',)
    fieldsets = (
        (None, {
            'fields': ('code', 'name', 'status')
        }),
        ('Precios por Toneladas', {
            'fields': ('export_price', 'transit_price', 'import_price')
        })
    )
    resource_class = resources.CommodityResource


def assign_substitute(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    app_label = opts.app_label
    obj = queryset.all()[0]

    if 'apply' in request.POST:
        modeladmin.message_user(request,
                                "%s ha sido movido al historico de empleado, favor complete los campos para el carnet # %s" %
                                (obj.name, obj.licence), messages.SUCCESS)
        emp_his = EmployeeHistory(
            licence=obj.licence,
            short_licence=obj.short_licence,
            name=obj.name,
            bird_date=obj.bird_date,
            identification=obj.identification,
            address=obj.address,
            telephone=obj.telephone,
            cellphone=obj.cellphone,
            nationality=obj.nationality,
            marital_status=obj.marital_status,
            status=obj.status,
            type=obj.type
        )
        emp_his.save()
        for re in Relative.objects.filter(person__licence=obj.licence):
            re_hi = RelativeHistory(name=re.name, relationship=re.relationship, is_dead=re.is_dead,
                                    death_date=re.death_date,employee=emp_his)
            re_hi.save()
            re.delete()
        obj.name = None
        obj.bird_date = None
        obj.identification = None
        obj.address = None
        obj.telephone = None
        obj.cellphone = None
        obj.save()
        return redirect(urlresolvers.reverse("admin:parametros_generales_employee_change", args={obj.licence}))

    if len(queryset) > 1:
        modeladmin.message_user(request, "No se puede selecionar mas de un registro para esta accion")
        return None
    if len(queryset) == 0:
        modeladmin.message_user(request, "Debe selecionar al menos un registros para realizar la accion")
        return None

    context = dict(
        modeladmin.admin_site.each_context(request),
        title=_("Proceso de sustitucion"),
        queryset=queryset,
        opts=opts,
        action_checkbox_name=helpers.ACTION_CHECKBOX_NAME,
        obj=obj,
    )
    return TemplateResponse(request, modeladmin.assign_substitute_template, context)


assign_substitute.short_description = 'Asignar sustituto'


class EmployeeAdmin(ModelAdminImportExport):
    assign_substitute_template = 'assign_substitute_template.html'
    resource_class = resources.EmployeeResource
    form = EmployeeForm
    fieldsets = (
        ('Datos Operativos', {
            'fields': ('status',)
        }),
        ('Datos Generales', {
            'fields': ('licence', 'name', 'bird_date', 'identification', 'nationality', 'marital_status')
        }),
        ('Datos de Contacto', {
            'fields': ('address', 'telephone', 'cellphone', )
        }),
    )
    list_display = ('licence', 'name', 'identification', 'telephone', 'cellphone', 'status',
                    'marital_status')
    list_display_links = ('licence', 'name', 'identification',)
    search_fields = ('short_licence', 'name', 'identification', 'telephone', 'cellphone', 'licence')
    list_filter = ('status', 'marital_status')
    actions = [assign_substitute, ]


class InspectorAdmin(ModelAdminImportExport):
    resource_class = resources.InspectorResource
    list_display = ('number', 'name', 'status')
    list_display_links = ('number', 'name')
    search_fields = ('number', 'name',)
    list_filter = ('status',)


class ShippingAdmin(ModelAdminImportExport):
    resource_class = resources.ShippingResource
    list_display = ('number', 'name', 'status', 'contact', 'telephone', 'fax')
    list_display_links = ('number', 'name')
    search_fields = ('number', 'name', 'contact', 'telephone', 'fax')
    list_filter = ('status',)


class VaporAdmin(ModelAdminImportExport):
    resource_class = resources.VaporResource
    list_display = ('number', 'name', 'status')
    list_display_links = ('number', 'name')
    search_fields = ('number', 'name')
    list_filter = ('status',)


class RelativeHistoryAdminInline(admin.TabularInline):
    fields = ('name', 'relationship', 'is_dead', 'death_date')
    model = RelativeHistory
    extra = 0


class EmployeeHistoryAdmin(ModelAdminImportExport):
    assign_substitute_template = 'assign_substitute_template.html'
    resource_class = resources.EmployeeResource
    form = EmployeeForm
    fieldsets = (
        ('Datos Operativos', {
            'fields': ('status',)
        }),
        ('Datos Generales', {
            'fields': ( 'licence', 'name', 'bird_date', 'identification', 'nationality', 'marital_status')
        }),
        ('Datos de Contacto', {
            'fields': ('address', 'telephone', 'cellphone', )
        }),
    )
    list_display = ('post_date', 'licence', 'name', 'identification', 'telephone', 'cellphone', 'status',
                    'marital_status')
    list_display_links = ('licence', 'name', 'identification',)
    search_fields = ('short_licence', 'name', 'identification', 'telephone', 'cellphone', 'licence')
    list_filter = ('status', 'marital_status')
    inlines = [RelativeHistoryAdminInline,]

admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeHistory, EmployeeHistoryAdmin)
admin.site.register(Inspector, InspectorAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Vapor, VaporAdmin)