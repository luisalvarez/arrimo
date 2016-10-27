from django.contrib.admin import SimpleListFilter
from control_de_vapores.models import Movement


class NominaFilter(SimpleListFilter):
    title = 'Nomina'
    parameter_name = 'nomina'


    def lookups(self, request, model_admin):
        return [(m.id, m.id) for m in Movement.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(quadrille__movement__id=self.value())
        else:
            return queryset
