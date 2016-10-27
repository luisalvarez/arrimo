from django.contrib.admin.views.main import ChangeList


def _sum(rs, property_name):
        total = 0
        for obj in rs:
            total += 0 if getattr(obj, property_name) is None else getattr(obj, property_name)
        return total

class NominaChangeList(ChangeList):
    def _sum(self, property_name):
        total = 0
        for obj in self.result_list:
            total += 0 if getattr(obj, property_name) is None else getattr(obj, property_name)
        return total

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Nomina'


class PagoEmpleadoChangeList(ChangeList):

    def total_s_bruto(self):
        return _sum(self.result_list, 's_bruto')

    def total_contri_s(self):
        return _sum(self.result_list, 'contri_s')

    def total_f_socorro(self):
        return _sum(self.result_list, 'f_socorro')

    def total_c_adic(self):
        return _sum(self.result_list, 'c_adic')

    def total_avances(self):
        return _sum(self.result_list, 'avances')

    def total_neto(self):
        return _sum(self.result_list, 'neto')

    def total_fop(self):
        return _sum(self.result_list, 'fop')

    def total_yola(self):
        return _sum(self.result_list, 'yola')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Pago Empleado'


class VaporPagadoChangeList(ChangeList):
    def _sum(self, property_name):
        total = 0
        for obj in self.result_list:
            total += 0 if getattr(obj, property_name) is None else getattr(obj, property_name)
        return total

    def total_nocivo(self):
        return self._sum('nocivo')

    def total_pagado(self):
        return self._sum('pagado')

    def total_avances(self):
        return self._sum('avances')

    def total_directivo(self):
        return self._sum('directivo')

    def total_pasado(self):
        return self._sum('pasado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Vapores Pagados'


class EntradaGeneralChangeList(ChangeList):
    def _sum(self, property_name):
        total = 0
        for obj in self.result_list:
            total += 0 if getattr(obj, property_name) is None else getattr(obj, property_name)
        return total

    def total_c_sindical(self):
        return self._sum('c_sindical')

    def total_fondo_socorro(self):
        return self._sum('fondo_socorro')

    def total_couta_adicional(self):
        return self._sum('couta_adicional')

    def total_hielo(self):
        return self._sum('hielo')

    def total_prestaciones(self):
        return self._sum('prestaciones')

    def total_yola(self):
        return self._sum('yola')

    def total_fop(self):
        return self._sum('fop')

    def total_total_dia(self):
        return self._sum('total_dia')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Entrada General'