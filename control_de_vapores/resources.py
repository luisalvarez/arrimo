from import_export import resources, fields, widgets
from control_de_vapores.models import Movement, Quadrille, EmployeeQuadrille

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class Resource(resources.ModelResource):
    class Meta:
        abstract = True


class MovementResource(Resource):
    class Meta:
        model = Movement
        import_id_fields = ('number',)
        fields = (
            'number',
            'vapor',
            'inspector__name',
            'shipping__name',
            'arrive_date',
            'contribucion',
            'socorro',
            'adicional',
            'hielo',
            'yola',
            'fop',
            'nocivos',
            'prestaciones',
            'total',
            'total_check'
        )


class QuadrilleResource(Resource):
    class Meta:
        model = Quadrille


class EmployeeQuadrilleResource(Resource):
    class Meta:
        model = EmployeeQuadrille

