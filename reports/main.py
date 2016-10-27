from django.contrib.admin.views.main import ChangeList


class VaporPayMovementChangeList(ChangeList):
    def _sum(self, property_name):
        total = 0
        for obj in self.result_list:
            total += 0 if getattr(obj, property_name) is None else getattr(obj, property_name)
        return total

    def total_advance(self):
        return self._sum('avance')

    def total_pagado(self):
        return self._sum('pagado')

    def total_pasado(self):
        return self._sum('pasado')

    def total_directivo(self):
        return self._sum('managers_pay_amount')

    def total_harmful(self):
        return self._sum('harmful')

    def total_others(self):
        return self._sum('others')

    def total_fop(self):
        return self._sum('fop')

    def total_socorro(self):
        return self._sum('socorro')

    def total_yola(self):
        return self._sum('yola')

    def total_total(self):
        return self._sum('total')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Resumen Vapores Pagados'


class NominaPayChangeList(ChangeList):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Nomina de Pago'

    def _sum(self, property_name):
        total = 0
        for obj in self.result_list:
            total += 0 if getattr(obj, property_name) is None else getattr(obj, property_name)
        return total

    def total_advance(self):
        return self._sum('avance')

    def total_pagado(self):
        return self._sum('pagado')

    def total_pasado(self):
        return self._sum('pasado')

    def total_directivo(self):
        return self._sum('managers_pay_amount')

    def total_harmful(self):
        return self._sum('harmful')

    def total_others(self):
        return self._sum('others')

    def total_fop(self):
        return self._sum('fop')

    def total_socorro(self):
        return self._sum('socorro')

    def total_yola(self):
        return self._sum('yola')

    def total_total(self):
        return self._sum('total')