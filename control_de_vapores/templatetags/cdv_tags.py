from django import template
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.templatetags.admin_list import result_headers, result_hidden_fields, results

register = template.Library()


@register.inclusion_tag("change_list_results_entrada_generales.html")
def result_list_entrada_general(cl):
    """
    Displays the headers and data list together
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': list(results(cl))}


@register.inclusion_tag("change_list_results_pago_empleados.html")
def result_list_pago_empleado(cl):
    """
    Displays the headers and data list together
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': list(results(cl))}


@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__


@register.filter('is_radio')
def is_radio(field):
    return isinstance(field.field.field.widget, forms.RadioSelect)


@register.filter('is_date')
def is_date(field):
    return isinstance(field.field.field.widget, AdminDateWidget)


@register.filter(name='add_class')
def add_css(field, css):
    return field.as_widget(attrs={"class": css, "placeholder": field.label})


@register.inclusion_tag('submit_line.html', takes_context=True)
def submit_row_movement(context):
    """
    Displays the row of buttons for delete and save.
    """
    is_calculate = False
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    ctx = {
        'opts': opts,
        'show_delete_link': (
            not is_popup and context['has_delete_permission'] and
            change and context.get('show_delete', True)
        ),
        'show_calculate_button': (
            change
        ),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': (
            context['has_add_permission'] and not is_popup and
            (not save_as or context['add'])
        ),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True,
        'preserved_filters': context.get('preserved_filters'),
        'is_calculate': is_calculate,
    }
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx