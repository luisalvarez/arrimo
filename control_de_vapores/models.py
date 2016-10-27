from django.db import models
from django.db.models import Sum
from django.db.models import Max
from parametros_generales.models import Vapor, Inspector, Shipping, Employee, Commodity
import decimal
import datetime
import datetime


class Parameter(models.Model):
    class Meta:
        verbose_name = 'Valor para el calculo de nomina'
        verbose_name_plural = 'Valores para el calculo de las nominas'

    contribution = models.DecimalField('Contribucion', decimal_places=2, max_digits=18, blank=True, null=True,
                                       default=0.00)
    mutual_aid = models.DecimalField('Socorro Mutuo', decimal_places=2, max_digits=18, blank=True, null=True,
                                     default=0.00)
    fee = models.DecimalField('Couta', decimal_places=2, max_digits=18, blank=True, null=True, default=0.00)
    yola = models.DecimalField('Yola', decimal_places=2, max_digits=18, blank=True, null=True, default=0.00)
    fop = models.DecimalField('FOP', decimal_places=2, max_digits=18, blank=True, null=True, default=0.00)
    date_create = models.DateField('Fecha Creado', auto_now=True)
    date_from = models.DateField('Fecha Desde', blank=True, null=True)
    date_to = models.DateField('Fecha Hasta', blank=True, null=True)
    is_default = models.NullBooleanField('Usar estos valores', null=True)

    def __str__(self):
        return "Contribucion: {}%, Socorro Mutuo: {}%, Couta: {}%, Yola: {}%, FOP: {}%; Desde: {} - Hasta: {}" \
            .format(self.contribution, self.mutual_aid, self.fee, self.yola, self.fop, self.date_from, self.date_to)


def generate_number_nomina():
    return (Movement.objects.all().aggregate(Max('number')).get('number__max', 0) or 0) + 1


def generate_monthly_number_nomina(date=datetime.date.today()):
    return (Movement.objects.filter(pay_date__month=date.month).aggregate(Max('alternative_number')).get(
        'alternative_number__max', 0) or 0) + 1


class Movement(models.Model):
    class Meta:
        verbose_name = 'Llegada de vapor'
        verbose_name_plural = 'Llegada de vapores'
        unique_together = (('alternative_number', 'pay_date'),)

    STATUS = (
        ('C', 'Calculada'),
        ('A', 'Abierta'),
        ('N', 'Anulada')
    )

    number = models.IntegerField('Identificador', primary_key=True,
                                 help_text="Identificador unico de cada nomina",
                                 default=generate_number_nomina)
    alternative_number = models.IntegerField('#Nomina',help_text="Esta columna tiene el proximo numero de nomina mensual se genera de forma automatica",
                                             default=generate_monthly_number_nomina)
    arrive_date = models.DateField('Llegada')
    pay_date = models.DateField('Pagar en', default=datetime.datetime.now)
    vapor = models.ForeignKey(Vapor, verbose_name='Vapor', limit_choices_to={'status': True})
    inspector = models.ForeignKey(Inspector, verbose_name='Inspector', limit_choices_to={'status': True})
    managers = models.DecimalField('Directivos', max_digits=2, decimal_places=1)
    managers_pay_amount = models.DecimalField('Directivos', max_digits=18, decimal_places=2, default=0)
    managers_harmful = models.DecimalField('Nocivo Directivos', max_digits=18, decimal_places=2, default=0)
    used_yola = models.BooleanField('¿Usaron Yola?')
    shipping = models.ForeignKey(Shipping, verbose_name='Naviera', limit_choices_to={'status': True})
    benefits = models.DecimalField('Prestaciones', decimal_places=2, max_digits=18, blank=True, null=True, default=0,
                                   help_text='Indique lo que fuera pagado direcctamente por la administracion del '
                                             'vapor')
    ice = models.DecimalField('Hielo', decimal_places=2, max_digits=18, blank=True, null=True, default=0,
                              help_text='Indicar lo gastado en hielo')
    others = models.DecimalField('Otros', decimal_places=2, max_digits=18, blank=True, null=True, default=0,
                                 help_text='Ponga cualquier otra deduccion para el valor del cheque')
    harmful = models.DecimalField('Nocivos', decimal_places=2, max_digits=18, blank=True, null=True,
                                  help_text='El valor de esta campo será restado al total pagado por las navieras '
                                            'antes de calcular la nomina',
                                  default=0)
    additional = models.DecimalField('Adicional', decimal_places=2, max_digits=18, blank=True, null=True, default=0)
    total_check = models.DecimalField('Total Cheque', decimal_places=2, max_digits=18, null=True, blank=True, default=0,
                                      help_text="Valor del cheque pagado por la naviera")
    total_amount = models.DecimalField('Total', decimal_places=2, max_digits=18, null=True, blank=True, default=0,
                                       help_text="Esta columna se calcula automatica se guardara con la suma de todos "
                                                 "los pagos realizados por las navieras menos lo pagado de nocivo")
    parameter = models.ForeignKey(Parameter, null=True)


    def __str__(self):
        return '%s - %s' % (self.vapor, self.arrive_date)

    def calculate(self):
        self.status = 'C'
        self.parameter = Parameter.objects.filter(is_default=True, date_to=None).first()
        tmp_total_amount = self.total_check
        if tmp_total_amount is None:
            tmp_total_amount = 0
        self.total_amount = tmp_total_amount - (self.harmful + self.benefits + self.ice + self.additional + self.others)

        total_employees = 0
        for quadrille in self.quadrille_set.all():
            total_employees = total_employees + quadrille.employeequadrille_set.count()
        amount = self.total_amount / (total_employees + self.managers)
        harmful_amount = self.harmful / (total_employees + self.managers)
        self.managers_pay_amount = amount * self.managers
        self.managers_harmful = harmful_amount * self.managers
        for quadrille in self.quadrille_set.all():
            quadrille.calculate(amount, harmful_amount)

        self.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super(Movement, self).save(force_insert, force_update, using, update_fields)

    @property
    def contribucion(self):
        return self.total_amount

    @property
    def prestaciones(self):
        total = 0
        for quadrille in self.quadrille_set.all():
            total += (quadrille.employeequadrille_set.aggregate(Sum('net_salary')).get('net_salary__sum', 0) or 0)
        return total

    @property
    def fop(self):
        total = 0
        for quadrille in self.quadrille_set.all():
            total += (quadrille.employeequadrille_set.aggregate(Sum('fop')).get('fop__sum', 0) or 0)
        return total

    @property
    def socorro(self):
        total = 0
        for quadrille in self.quadrille_set.all():
            total += (quadrille.employeequadrille_set.aggregate(Sum('mutual_aid')).get('mutual_aid__sum', 0) or 0)
        return total

    @property
    def yola(self):
        total = 0
        for quadrille in self.quadrille_set.all():
            total += (quadrille.employeequadrille_set.aggregate(Sum('yola')).get('yola__sum', 0) or 0)
        return total

    @property
    def avance(self):
        total_advance = 0
        for quadrille in self.quadrille_set.all():
            total_advance += (quadrille.employeequadrille_set.aggregate(Sum('advance')).get('advance__sum', 0) or 0)
        return total_advance

    @property
    def pasado(self):
        total_advance = 0
        for quadrille in self.quadrille_set.all():
            total_advance += (quadrille.employeequadrille_set.aggregate(Sum('past')).get('past__sum', 0) or 0)
        return total_advance

    @property
    def pagado(self):
        return self.total_amount - self.managers_pay_amount

    @property
    def deducciones(self):
        return self.benefits + self.ice + self.harmful + self.additional

    @property
    def total(self):
        return self.total_amount + self.benefits + self.others + self.ice + self.harmful + self.additional

    @property
    def adicional(self):
        return self.additional

    @property
    def nocivos(self):
        return self.harmful

    @property
    def hielo(self):
        return self.ice


class ShippingMovement(models.Model):
    class Meta:
        verbose_name = 'Pago de Naviera'
        verbose_name_plural = 'Pagos de Navieras'
        unique_together = (('movement', 'shipping'),)

    movement = models.ForeignKey(Movement, verbose_name='Llegada de Vapor')
    shipping = models.ForeignKey(Shipping, verbose_name='Naviera', limit_choices_to={'status': True})
    amount = models.DecimalField('Monto', decimal_places=2, max_digits=18, default=0)

    def __str__(self):
        return '%s %s' % (self.shipping, self.amount)


class Quadrille(models.Model):
    class Meta:
        verbose_name = 'Cuadrilla'
        verbose_name_plural = 'Cuadrillas'

    movement = models.ForeignKey(Movement, verbose_name='Llegada Vapor',
                                 help_text='Seleccione la llegada de un vapor para crear la cuadrilla.')

    def calculate(self, amount, harmful_amount):
        for employee in self.employeequadrille_set.all():
            employee.calculate(amount, harmful_amount)

    @property
    def inspector(self):
        return self.movement.inspector

    @property
    def vapor(self):
        return self.movement.vapor

    @property
    def fecha_llegada(self):
        return self.movement.arrive_date

    def __str__(self):
        return '%s Cuadrilla %s' % (self.movement, self.id,)


class EmployeeQuadrille(models.Model):
    class Meta:
        verbose_name = 'Miembros de la cuadrilla'
        verbose_name_plural = 'Miembros de la Cuadrilla'
        unique_together = (('quadrille', 'employee',),)

    quadrille = models.ForeignKey(Quadrille, verbose_name='Cuadrilla')
    employee = models.ForeignKey(Employee, verbose_name='Empleado',
                                 limit_choices_to={'status': True, 'substitute__isnull': True})
    advance = models.DecimalField('Avance', decimal_places=2, max_digits=18, default=0)
    others_payments = models.DecimalField('Otros pagos', decimal_places=2, max_digits=18, blank=True, null=True,
                                          default=0.00)
    others_deductions = models.DecimalField('Otros deducciones', decimal_places=2, max_digits=18, blank=True, null=True,
                                            default=0.00)
    contribution = models.DecimalField('Contribuccion', decimal_places=2, max_digits=18, blank=True, null=True,
                                       default=0.00)
    yola = models.DecimalField('Yola', decimal_places=2, max_digits=18, blank=True, null=True, default=0.00)
    mutual_aid = models.DecimalField('Socorro Mutuo', decimal_places=2, max_digits=18, blank=True, null=True,
                                     default=0.00)
    fee = models.DecimalField('Couta', decimal_places=2, max_digits=18, blank=True, null=True, default=0.00)
    fop = models.DecimalField('FOP', decimal_places=2, max_digits=18, blank=True, null=True, default=0.00)
    past = models.DecimalField('Pasado', decimal_places=2, max_digits=18, blank=True, null=True, default=0.00)
    gross_salary = models.DecimalField('Sueldo Bruto', decimal_places=2, max_digits=18, blank=True, null=True,
                                       default=0.00)
    net_salary = models.DecimalField('Sueldo Neto', decimal_places=2, max_digits=18, blank=True, null=True,
                                     default=0.00)
    harmful = models.DecimalField('Nocivo', decimal_places=2, max_digits=18, blank=True, null=True,
                                  default=0.00)

    def calculate(self, amount, harmful_amount):
        parameter = self.quadrille.movement.parameter
        self.gross_salary = amount
        if parameter is not None:
            self.yola = ((amount * parameter.yola) / 100) if self.quadrille.movement.used_yola else 0
            self.fee = (amount * parameter.fee) / 100
            self.contribution = (amount * parameter.contribution) / 100
            self.fop = (amount * parameter.fop) / 100
            self.mutual_aid = (amount * parameter.mutual_aid) / 100
        else:
            self.yola = ((amount * 2) / 100) if self.quadrille.movement.used_yola else 0
            self.fee = (amount * 15) / 100
            self.contribution = (amount * 6) / 100
            self.fop = (amount * 5) / 100
            self.mutual_aid = (amount * 7) / 100
        self.harmful = harmful_amount
        self.net_salary = decimal.Decimal(self.gross_salary + self.harmful) - (
            decimal.Decimal(self.fee) + decimal.Decimal(self.contribution) + decimal.Decimal(
                self.yola) + decimal.Decimal(
                self.fop) + decimal.Decimal(self.mutual_aid))
        self.past = decimal.Decimal(self.net_salary) - decimal.Decimal(self.advance)
        if self.past < 0:
            self.net_salary = 0
            self.past *= -1
        else:
            self.past = 0
            self.net_salary = self.net_salary - self.advance
        self.save()

    def __str__(self):
        return '%s' % (self.employee,)


class Cargo(models.Model):
    class Meta:
        verbose_name = 'Carga'
        verbose_name_plural = 'Carga'
        unique_together = (('movement', 'commodity', 'type'),)

    TYPE_CHOICES = (
        ('E', 'Exportacion'),
        ('I', 'Importacion'),
        ('T', 'Transito')
    )
    movement = models.ForeignKey(Movement, verbose_name='Llegada de vapor')
    commodity = models.ForeignKey(Commodity, verbose_name='Mercancia', limit_choices_to={'status': True})
    type = models.CharField('Tipo', max_length=1, choices=TYPE_CHOICES)
    price = models.DecimalField('Precio', blank=True, default=0, null=True, decimal_places=2, max_digits=18,
                                help_text='Si no suministra valor para este campo, se tomara el precio dependiendo del tipo de carga. Ejemplo: si se deja en blanco y se pone de tipo exportación se tomara el precio definido para la exportación.')
    tons = models.DecimalField('Toneladas', decimal_places=2, max_digits=18)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.price is None or self.price == 0:
            self.price = self.get_default_price()
        return super(Cargo, self).save(force_insert, force_update, using, update_fields)

    def get_default_price(self):
        switcher = {
            'E': self.commodity.export_price,
            'I': self.commodity.import_price,
            'T': self.commodity.transit_price
        }
        return switcher.get(self.type, 0.)

    def __str__(self):
        return '%s toneladas para %s de %s por el monto de %s' % (self.tons, self.type, self.commodity, self.price)



