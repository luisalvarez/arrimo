from import_export import resources, fields, widgets
from parametros_generales.models import Commodity, Employee, Inspector, Shipping, Vapor, EmployeeHistory

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class Resource(resources.ModelResource):
    class Meta:
        abstract = True


    """def get_export_headers(self):
        headers = []
        for field in self.get_fields():
            headers.append(
                force_text(force_text(self.Meta.model._meta.get_field_by_name(field.column_name)[0].verbose_name.capitalize())
                    if self.Meta.model._meta.get_field_by_name(field.column_name)[0].verbose_name is not None
                    else force_text(field.column_name)))
        return headers
    """


class CommodityResource(Resource):
    class Meta:
        model = Commodity
        import_id_fields = ('code',)


class EmployeeResource(Resource):

    class Meta:
        model = Employee
        import_id_fields = ('licence',)


class EmployeeHistoryResource(Resource):

    class Meta:
        model = EmployeeHistory
        import_id_fields = ('licence',)


class InspectorResource(Resource):

    class Meta:
        model = Inspector
        import_id_fields = ('number',)


class ShippingResource(Resource):
    class Meta:
        model = Shipping
        import_id_fields = ('number',)


class VaporResource(Resource):
    class Meta:
        model = Vapor
        import_id_fields = ('number',)