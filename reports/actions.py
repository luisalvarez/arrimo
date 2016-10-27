
from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import get_deleted_objects, model_ngettext
from django.core.exceptions import PermissionDenied
from django.db import router
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from reports.views import generate


def generate_report(modeladmin, request, queryset):
    return generate(request, modeladmin.report(request).get_url())

generate_report.short_description = ugettext_lazy("Generar Reporte ")
