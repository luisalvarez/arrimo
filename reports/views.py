from django.core.serializers import json
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib import admin
from reports.reports import BaseJasperReport
import json

site = admin.site


def generate(request):
    params = request.GET.copy()
    params['reportUnit'] = params.get('reportunit', '')
    del params['reportunit']
    report = BaseJasperReport(request,  params)
    return HttpResponse(json.dumps({'url': report.get_url()}), content_type="application/json")


def download(request):
    report = BaseJasperReport(request, request.GET)
    return report.render_to_response()


def reports(request, template='reports.html', title="Reportes"):
    context = dict(
        site.each_context(request),
        title=title,
    )
    return TemplateResponse(request, template, context)
