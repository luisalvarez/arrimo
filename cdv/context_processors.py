from django.apps import apps
from django.contrib import admin
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils import six
from django.utils.text import capfirst
from control_de_vapores.models import Movement, Quadrille, Parameter
from parametros_generales.models import Inspector, Shipping, Vapor, Employee, Commodity, EmployeeHistory
from datos_familiares.models import Person, Relative, RelativeType

site = admin.site


def add_view(app_dict,
             app_label,
             verbose_name_plural,
             object_name,
             url):
    view_dict = {
        'name': capfirst(verbose_name_plural),
        'object_name': object_name,
        'perms': True,
        'admin_url': reverse(url, current_app=site.name),
        'add_url': reverse(url, current_app=site.name)
    }
    if app_label in app_dict:
        app_dict[app_label]['models'].append(view_dict)
    else:
        app_dict[app_label] = {
            'name': apps.get_app_config(app_label).verbose_name,
            'app_label': app_label,
            'app_url': reverse('admin:app_list', kwargs={'app_label': app_label}, current_app=site.name),
            'has_module_perms': True,
            'models': [view_dict],
        }


def admin_app_list(request):
    app_dict = {}
    add_view(app_dict, 'control_de_vapores', 'Registro Llegada', 'Registro LLegada', 'reg:reg_vap_arr',)
    add_view(app_dict, 'control_de_vapores', Movement._meta.verbose_name_plural,  Movement._meta.object_name,
             'admin:%s_%s_changelist' % ('control_de_vapores', Movement._meta.model_name))
    add_view(app_dict, 'control_de_vapores', Quadrille._meta.verbose_name_plural,  Quadrille._meta.object_name,
             'admin:%s_%s_changelist' % ('control_de_vapores', Quadrille._meta.model_name))
    add_view(app_dict, 'control_de_vapores', Parameter._meta.verbose_name_plural,  Parameter._meta.object_name,
             'admin:%s_%s_changelist' % ('control_de_vapores', Parameter._meta.model_name))

    add_view(app_dict, 'parametros_generales', Inspector._meta.verbose_name_plural,  Inspector._meta.object_name,
             'admin:%s_%s_changelist' % ('parametros_generales', Inspector._meta.model_name))
    add_view(app_dict, 'parametros_generales', Shipping._meta.verbose_name_plural,  Shipping._meta.object_name,
             'admin:%s_%s_changelist' % ('parametros_generales', Shipping._meta.model_name))
    add_view(app_dict, 'parametros_generales', Vapor._meta.verbose_name_plural,  Vapor._meta.object_name,
             'admin:%s_%s_changelist' % ('parametros_generales', Vapor._meta.model_name))
    add_view(app_dict, 'parametros_generales', Employee._meta.verbose_name_plural,  Employee._meta.object_name,
             'admin:%s_%s_changelist' % ('parametros_generales', Employee._meta.model_name))
    add_view(app_dict, 'parametros_generales', Commodity._meta.verbose_name_plural,  Commodity._meta.object_name,
             'admin:%s_%s_changelist' % ('parametros_generales', Commodity._meta.model_name))
    add_view(app_dict, 'parametros_generales', EmployeeHistory._meta.verbose_name_plural,  EmployeeHistory._meta.object_name,
             'admin:%s_%s_changelist' % ('parametros_generales', EmployeeHistory._meta.model_name))

    add_view(app_dict, 'datos_familiares', Person._meta.verbose_name_plural,  Person._meta.object_name,
             'admin:%s_%s_changelist' % ('datos_familiares', Person._meta.model_name))
    add_view(app_dict, 'datos_familiares', RelativeType._meta.verbose_name_plural,  RelativeType._meta.object_name,
             'admin:%s_%s_changelist' % ('datos_familiares', RelativeType._meta.model_name))
    add_view(app_dict, 'datos_familiares', Relative._meta.verbose_name_plural,  Relative._meta.object_name,
             'admin:%s_%s_changelist' % ('datos_familiares', Relative._meta.model_name))

    add_view(app_dict, 'reports', 'Reportes', 'Reportes', 'report:reportes')

    app_list = list(six.itervalues(app_dict))
    app_list.sort(key=lambda x: x['name'].lower())

    return {'adm_app_list': app_list}