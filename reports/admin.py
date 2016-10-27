from django.contrib import admin
from reports.models import NominaReporte, PagoEmpleadoReporte, VaporPagadoReporte, EntradaGeneralReporte
from reports.change_list import NominaChangeList, PagoEmpleadoChangeList, VaporPagadoChangeList, \
    EntradaGeneralChangeList
from reports.filters_spec import NominaFilter
from reports.actions import generate_report


class NominaReporteAdmin(admin.ModelAdmin):
    actions = [generate_report, ]
    change_list_template = 'change_list_reporte_nomina.html'
    list_display = ('carnet', 'nombre', 'otros_pagos',
                    'avances', 'otros_descuentos', 'total_descuentos',
                    'neto')
    list_filter = (NominaFilter,)

    def get_changelist(self, request, **kwargs):
        return NominaChangeList

    def __init__(self, *args, **kwargs):
        super(NominaReporteAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(NominaReporteAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class PagoEmpleadoAdmin(admin.ModelAdmin):
    change_list_template = 'change_list_reporte_pago_empleado.html'
    list_display = ('nombre_vapor', 'fecha', 's_bruto', 'contri_s',
                    'f_socorro', 'c_adic', 'yola', 'fop', 'avances',
                    'neto')

    def get_changelist(self, request, **kwargs):
        return PagoEmpleadoChangeList

    def __init__(self, *args, **kwargs):
        super(PagoEmpleadoAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(PagoEmpleadoAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class VaporPagadoAdmin(admin.ModelAdmin):
    change_list_template = 'change_list_reporte_vapor_pagado.html'
    list_display = ('num', 'nombre', 'fecha', 'pagado', 'avances', 'pasado', 'directivo')

    def __init__(self, *args, **kwargs):
        super(VaporPagadoAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def get_changelist(self, request, **kwargs):
        return VaporPagadoChangeList

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(VaporPagadoAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class EntradaGeneralAdmin(admin.ModelAdmin):
    change_list_template = 'change_list_reporte_entrada_general.html'
    list_display = ('c_sindical', 'fondo_socorro', 'couta_adicional',
                    'hielo', 'prestaciones', 'fop',
                    'total_dia')

    def __init__(self, *args, **kwargs):
        super(EntradaGeneralAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def get_changelist(self, request, **kwargs):
        return EntradaGeneralChangeList

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(EntradaGeneralAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(EntradaGeneralReporte, EntradaGeneralAdmin)
admin.site.register(NominaReporte, NominaReporteAdmin)
admin.site.register(PagoEmpleadoReporte, PagoEmpleadoAdmin)
admin.site.register(VaporPagadoReporte, VaporPagadoAdmin)
