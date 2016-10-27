from control_de_vapores.models import Movement, EmployeeQuadrille, ShippingMovement
from django.db.models import Sum


class NominaReporte(EmployeeQuadrille):
    class Meta:
        verbose_name_plural = 'Nomina'
        verbose_name = 'Nomina'
        proxy = True

    @property
    def carnet(self):
        return self.employee.licence

    @property
    def nombre(self):
        return self.employee.name

    @property
    def otros_pagos(self):
        return self.others_payments

    @property
    def avances(self):
        return self.advance

    @property
    def otros_descuentos(self):
        return self.others_deductions

    @property
    def total_descuentos(self):
        return (self.contribution +
                self.yola +
                self.mutual_aid +
                self.fee +
                self.fop +
                self.others_deductions + self.advance)

    @property
    def neto(self):
        return self.net_salary


class PagoEmpleadoReporte(EmployeeQuadrille):
    class Meta:
        verbose_name_plural = 'Pago de Empleado'
        verbose_name = 'Pago de Empleado'
        proxy = True

    def nombre_vapor(self):
        return self.quadrille.movement.vapor.name

    @property
    def fecha(self):
        return self.quadrille.movement.pay_date

    @property
    def s_bruto(self):
        return self.gross_salary

    @property
    def contri_s(self):
        return self.contribution

    @property
    def f_socorro(self):
        return self.mutual_aid

    @property
    def c_adic(self):
        return self.fee

    @property
    def avances(self):
        return self.advance

    @property
    def neto(self):
        return self.net_salary


class VaporPagadoReporte(Movement):
    class Meta:
        verbose_name_plural = 'Vapores Pagados'
        verbose_name = 'Vapores Pagados'
        proxy = True

    @property
    def num(self):
        return self.vapor_id

    @property
    def nombre(self):
        return self.vapor.name

    @property
    def fecha(self):
        return self.pay_date

    @property
    def pagado(self):
        total_pagado = 0
        for quadrille in self.quadrille_set.all():
            total_pagado += quadrille.employeequadrille_set.aggregate(Sum('net_salary')).get('net_salary__sum', 0)
        return total_pagado

    @property
    def avances(self):
        total_advance = 0
        for quadrille in self.quadrille_set.all():
            total_advance += quadrille.employeequadrille_set.aggregate(Sum('advance')).get('advance__sum', 0)
        return total_advance

    @property
    def pasado(self):
        total_pasado = 0
        for quadrille in self.quadrille_set.all():
            total_pasado += quadrille.employeequadrille_set.aggregate(Sum('past')).get('past__sum', 0)
        return total_pasado

    @property
    def directivo(self):
        return self.managers_pay_amount

    @property
    def nocivo(self):
        return self.harmful


class EntradaGeneralReporte(Movement):
    class Meta:
        verbose_name = 'Entrada General'
        verbose_name_plural = 'Entrada General'
        proxy = True

    @property
    def c_sindical(self):
        t = 0
        for e in self.quadrille_set.all():
            t += e.employeequadrille_set.aggregate(Sum('contribution')).get('contribution__sum', 0)
        return t

    @property
    def fondo_socorro(self):
        t = 0
        for e in self.quadrille_set.all():
            t += e.employeequadrille_set.aggregate(Sum('mutual_aid')).get('mutual_aid__sum', 0)
        return t

    @property
    def couta_adicional(self):
        t = 0
        for e in self.quadrille_set.all():
            t += e.employeequadrille_set.aggregate(Sum('fee')).get('fee__sum', 0)
        return t

    @property
    def hielo(self):
        return self.ice

    @property
    def prestaciones(self):
        t = 0
        for e in self.quadrille_set.all():
            t += e.employeequadrille_set.aggregate(Sum('net_salary')).get('net_salary__sum', 0)
        return t

    @property
    def yola(self):
        t = 0
        for e in self.quadrille_set.all():
            t += e.employeequadrille_set.aggregate(Sum('yola')).get('yola__sum', 0)
        return t

    @property
    def fop(self):
        t = 0
        for e in self.quadrille_set.all():
            t += e.employeequadrille_set.aggregate(Sum('fop')).get('fop__sum', 0)
        return t

    @property
    def total_dia(self):
        return (self.c_sindical + self.fondo_socorro + self.couta_adicional +
                self.hielo + self.prestaciones + self.fop)


