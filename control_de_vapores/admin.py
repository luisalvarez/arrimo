from datetime import datetime

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from import_export.admin import ImportExportActionModelAdmin as ModelAdminImportExport
from control_de_vapores.models import Movement, ShippingMovement, Cargo, Quadrille, EmployeeQuadrille, Parameter
from control_de_vapores.resources import QuadrilleResource, MovementResource, EmployeeQuadrilleResource
from control_de_vapores.forms import MovementForm, ParameterForm, EmployeeQuadrilleForm
from control_de_vapores.filters import DateRangeFilter


class ParameterAdmin(admin.ModelAdmin):
    form = ParameterForm
    list_display = ('date_from', 'date_to', 'is_default', 'contribution', 'mutual_aid', 'fee', 'yola', 'fop',)
    list_display_links = ('contribution', 'mutual_aid', 'fee', 'yola', 'fop', 'date_from', 'date_to', 'is_default')
    list_filter = ('date_to', 'date_from', 'is_default')
    actions = ['make_default_parameter']

    def make_default_parameter(self, request, queryset):
        if queryset.all().count() == 1:
            Parameter.objects.filter(is_default=True).update(is_default=False, date_to=datetime.now())
            queryset.update(is_default=True, date_from=datetime.now(), date_to=None)
            self.message_user(request, "Valores selecionados, la nomina la prozima nomina se calculara con estos valores")
        else:
            self.message_user(request, "No se puede selecionar mas de un registro para esta accion")

    make_default_parameter.short_description = "Selecionar estos parametros para calcular las nominas"


class ShippingMovementAdminInline(admin.TabularInline):
    raw_id_fields = ('shipping',)
    model = ShippingMovement
    extra = 0


class CargoAdminInline(admin.TabularInline):
    model = Cargo
    raw_id_fields = ('commodity',)
    extra = 0


class MovementAdmin(ModelAdminImportExport):
    change_form_template = r'change_form.html'
    change_list_template = r'change_list.html'
    fieldsets = (
        (None, {
            'fields': ('number', 'alternative_number', 'arrive_date', 'pay_date', 'vapor', 'inspector', 'managers', 'used_yola',
                       'shipping', 'benefits', 'ice', 'others', 'harmful', 'additional', 'total_check',
                       'total_amount')}),)
    form = MovementForm
    readonly_fields = ('status', 'total_amount')
    save_on_top = True
    resource_class = MovementResource
    raw_id_fields = ('vapor', 'inspector', 'shipping')
    list_display = (
        'alternative_number',
        'pay_date',
        'number',
        'vapor',
        'arrive_date',
        'contribucion',
        'socorro',
        'adicional',
        'hielo',
        'yola',
        'fop',
        'nocivos',
        'prestaciones',
        'pasado',
        'total'
    )
    list_display_links = ('number', 'alternative_number', 'pay_date' ,'arrive_date', 'vapor',)
    search_fields = ('arrive_date', 'vapor__name', 'inspector__name', 'shipping__name', 'number')
    list_filter = (('arrive_date', DateRangeFilter),
                   'used_yola',
                   'managers',)

    inlines = [CargoAdminInline]

    def get_changelist(self, request, **kwargs):
        from control_de_vapores.main import MovementChangeList
        return MovementChangeList

    def response_change(self, request, obj):
        opts = self.model._meta
        msg_dict = {'name': force_text(opts.verbose_name), 'obj': force_text(obj)}
        preserved_filters = self.get_preserved_filters(request)
        if '_calculate' in request.POST:
            obj.calculate()
            msg = 'El %(name)s "%(obj)s" ha sido calculada ' % msg_dict
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)
        return super(MovementAdmin, self).response_change(request, obj)


class EmployeeQuadrilleAdmin(admin.ModelAdmin):
    resource_class = EmployeeQuadrilleResource
    raw_id_fields = ('employee', 'quadrille')
    list_display = ('quadrille', 'employee', 'advance', 'others_payments', 'others_deductions',
                    'contribution', 'yola', 'mutual_aid', 'fee', 'fop', 'past', 'gross_salary',
                    'net_salary')
    search_fields = ('quadrille__movement__id', 'employee__name')
    list_filter = ('quadrille__movement__arrive_date', 'employee__name', )


class EmployeeQuadrilleInline(admin.TabularInline):
    model = EmployeeQuadrille
    form = EmployeeQuadrilleForm
    raw_id_fields = ('employee',)
    extra = 1


class QuadrilleAdmin(ModelAdminImportExport):
    resource_class = QuadrilleResource
    raw_id_fields = ('movement',)
    list_display = ('__str__', 'fecha_llegada', 'vapor', 'inspector')
    inlines = [EmployeeQuadrilleInline, ]
    search_fields = ('id', 'movement__vapor__name', 'movement__inspector__name', 'movement__arrive_date')
    list_filter = ('movement__vapor', 'movement__inspector', 'movement__arrive_date')


admin.site.register(Movement, MovementAdmin)
admin.site.register(Quadrille, QuadrilleAdmin)
admin.site.register(Parameter, ParameterAdmin)