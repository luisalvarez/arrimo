import json
import datetime
from django.db.models import Q
from django.template.response import TemplateResponse
from django.contrib import admin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from control_de_vapores.models import Movement, EmployeeQuadrille, generate_number_nomina, \
    Vapor, Inspector, Shipping, Quadrille, Employee, generate_monthly_number_nomina
from django.db.models.loading import get_model
from django.db import connection
import json
from django.http import JsonResponse
from django.core import serializers

site = admin.site

query_graph = """
select
    if(EXTRACT(month FROM pay_date)=1,'Enero',
    if(EXTRACT(month FROM pay_date)=2,'Febrero',
    if(EXTRACT(month FROM pay_date)=3,'Marzo',
    if(EXTRACT(month FROM pay_date)=4,'Abril',
    if(EXTRACT(month FROM pay_date)=5,'Mayo',
    if(EXTRACT(month FROM pay_date)=6,'Junio',
    if(EXTRACT(month FROM pay_date)=7,'Julio',
    if(EXTRACT(month FROM pay_date)=8,'Agosto',
    if(EXTRACT(month FROM pay_date)=9,'Septiembre',
    if(EXTRACT(month FROM pay_date)=10,'Octubre',
    if(EXTRACT(month FROM pay_date)=11,'Noviembre',
    if(EXTRACT(month FROM pay_date)=12,'Diciembre',null)))))))))))) label,
    sum(qua_emp.contribution + qua_emp.yola + qua_emp.mutual_aid + qua_emp.fee + qua_emp.fop + qua_emp.others_deductions ) serie_1,
    sum((qua_emp.net_salary) +  qua_emp.advance) serie_2,
    (SELECT sum(mov1.managers_pay_amount) directivo
	FROM control_de_vapores_movement mov1
	WHERE Extract(month from mov1.pay_date) = Extract(month from mov.pay_date)) serie_3
from parametros_generales_employee emp,
	control_de_vapores_employeequadrille qua_emp,
    control_de_vapores_quadrille qua,
    control_de_vapores_movement mov,
    parametros_generales_inspector ins,
    parametros_generales_vapor vap,
    parametros_generales_shipping nav
where
	nav.number = mov.shipping_id and
	qua_emp.employee_id = emp.licence and
    qua.id = qua_emp.quadrille_id and
    qua.movement_id = mov.number and
    ins.number = mov.inspector_id and
    mov.vapor_id = vap.number and
    Extract(year from pay_date) = (select extract(year from max(pay_date)) from control_de_vapores_movement)
group by EXTRACT(month FROM pay_date)

"""


def graph(request):
    cursor = connection.cursor()
    cursor.execute(query_graph)
    labels = []
    series_1 = []
    series_2 = []
    series_3 = []
    for reg in cursor.fetchall():
        labels.append(reg[0])
        series_1.append(reg[1])
        series_2.append(reg[2])
        series_3.append(reg[3])
    response = {
        'labels': labels,
        'series_1': series_1,
        'series_2': series_2,
        'series_3': series_3
    }
    return JsonResponse(response)


def search(request):
    response = {'response': None, 'sucess': 0}
    r = []
    if request.GET.get('tipo', None) == 'inspector':
        for obj in Inspector.objects.filter(Q(name__icontains=request.GET['search']) | Q(number=request.GET['number'])):
            r.append({"number" :obj.number,"name":obj.name})        
        response = {
            'response':r,
            'success': 1}
    if request.GET.get('tipo', None) == 'vapor':
        for obj in  Vapor.objects.filter(Q(name__icontains=request.GET['search']) | Q(number=request.GET['number'])):
            r.append({"number" :obj.number,"name":obj.name})
        response = {
            'response': r,
            'success': 1}
    if request.GET.get('tipo', None) == 'shipping':
        for obj in Shipping.objects.filter(Q(name__icontains=request.GET['search']) | Q(number=request.GET['number'])):
            r.append({"number" :obj.number,"name":obj.name})
        response = {
            'response': r,  
            'success': 1}
    return JsonResponse(response, safe=False)


def reg_vapor_arr(request, template='reg_vap_arr.html', title="Registro de Llegada de Vapores"):
    import datetime

    context = dict(
        site.each_context(request),
        title=title,
        nominna_id=generate_number_nomina(),
        nomina_number=generate_monthly_number_nomina(),
        pay_date=datetime.date.today()
    )
    return TemplateResponse(request, template, context)


def get_name(request):
    if 'model' in request.GET and 'value' in request.GET:
        if request.GET['model'] == 'Employee':
            try:
                obj = get_model('parametros_generales', request.GET['model']).objects. \
                    filter(Q(short_licence=request.GET['value']) | Q(licence=request.GET['value']))[0]
                return HttpResponse(json.dumps({'name': obj.name, 'result': 1, 'model': request.GET['model']}, ),
                                    content_type="application/json")
            except Exception as e:
                HttpResponse(json.dumps({'name': str(e), 'result': 0, 'model': request.GET['model']}))
        else:
            try:
                obj = get_model('parametros_generales', request.GET['model']).objects.get(pk=request.GET['value'])
                return HttpResponse(json.dumps({'name': obj.name, 'result': 1, 'model': request.GET['model']}, ),
                                    content_type="application/json")
            except Exception as e:
                HttpResponse(json.dumps({'name': str(e), 'result': 0, 'model': request.GET['model']}))
    return HttpResponse(json.dumps({'name': 'no_param', 'result': 0}))


@csrf_exempt
def reg_vapor_arr_save(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        n_pay_date = datetime.datetime.strptime(data['arrive']['pagar'], '%d-%m-%Y')
        mov = Movement(
            alternative_number=generate_monthly_number_nomina(n_pay_date),
            number=generate_number_nomina(),
            arrive_date=datetime.datetime.strptime(data['arrive']['llegada'], '%d-%m-%Y').strftime('%Y-%m-%d'),
            pay_date=n_pay_date.strftime('%Y-%m-%d'),
            vapor=Vapor.objects.get(number=data['arrive']['cod_vapor']),
            inspector=Inspector.objects.get(number=data['arrive']['cod_inspector']),
            managers=data['arrive']['directivo'],
            used_yola=data['arrive']['used_yola'],
            shipping=Shipping.objects.get(number=data['arrive']['cod_naviera']),
            benefits=data['arrive']['prestaciones'],
            ice=data['arrive']['hielo'],
            others=data['arrive']['otros'],
            harmful=data['arrive']['nocivo'],
            additional=data['arrive']['adicional'],
            total_check=data['arrive']['cheque']
        )
        quadrille = Quadrille(movement=mov)
        mov.save()
        quadrille.save()
        for q in data['quadrille']:
            emp = Employee.objects.filter(Q(short_licence=q['carnet']) |
                                          Q(licence=q['carnet']))[0]
            emp_q = EmployeeQuadrille(
                quadrille=quadrille,
                employee=emp,
                advance=q['avance'],
                others_payments=q['otros_pagos'],
                others_deductions=q['otras_deducciones']
            )
            emp_q.save()
        mov.calculate()
        return HttpResponse(mov.number)
    except Exception as e:
        res = HttpResponse()
        res.status_code = 500
        res.reason_phrase = str(e)
        return res

