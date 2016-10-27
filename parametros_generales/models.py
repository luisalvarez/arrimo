from django.db import models
from django.db.models import Max



def _auto_increment_inspector():
    return (Inspector.objects.all().aggregate(Max('number')).get('number__max', 0) or 0) + 1


class Inspector(models.Model):
    class Meta:
        verbose_name_plural = "Inspectores"
        verbose_name = 'Inspector'
    number = models.IntegerField('Numero', primary_key=True, default=_auto_increment_inspector)
    name = models.CharField('Nombre', max_length=200)
    status = models.BooleanField('¿Activo?', default=True)

    def __str__(self):
        return '%s-%s' % (self.number, self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Inspector, self).save(force_insert, force_update, using, update_fields)


def _auto_increment_shipping():
    return (Shipping.objects.all().aggregate(Max('number')).get('number__max', 0) or 0) + 1


class Shipping(models.Model):
    class Meta:
        verbose_name = 'Naviera'
        verbose_name_plural = 'Navieras'
    number = models.IntegerField('numero', primary_key=True, default=_auto_increment_shipping)
    name = models.CharField('nombre', max_length=200)
    contact = models.CharField('contacto', max_length=200, blank=True, null=True)
    telephone = models.CharField('telefono', max_length=20, blank=True, null=True)
    fax = models.CharField('fax', max_length=20, blank=True, null=True)
    status = models.BooleanField('¿Activo?', default=True)

    def __str__(self):
        return '%s' % (self.name,)


def _auto_increment_vapor():
    return (Vapor.objects.all().aggregate(Max('number')).get('number__max', 0) or 0) + 1


class Vapor(models.Model):
    class Meta:
        verbose_name = 'Vapor'
        verbose_name_plural = 'Vapores'

    number = models.IntegerField('Numero', primary_key=True,default=_auto_increment_vapor)
    name = models.CharField('Nombre', max_length=200)
    status = models.BooleanField('¿Activo?', default=True)

    def __str__(self):
        return '%s' % (self.name,)


class Employee(models.Model):
    class Meta:
        verbose_name = 'Miembros'
        verbose_name_plural = 'Miembros'
        ordering = ['name', 'licence', 'identification']

    MARITAL_STATUS_CHOICES = (
        ('C', 'Casado'),
        ('S', 'Soltero'),
        ('D', 'Divorciado'),
        ('V', 'Viudo')
    )
    TYPE_CHOICES = (
        ('D', 'Directo'),
        ('S', 'Sustituto'),
    )
    NATIONALITY_CHOICES = (
        ('DO', 'Dominicano'),
        ('EX', 'Extranjero')
    )
    licence = models.CharField('Carnet', primary_key=True, max_length=255)
    short_licence = models.CharField('Carnet Corto',max_length=255,blank=True, null=True)
    name = models.CharField('Nombre', max_length=200,blank=True, null=True)
    bird_date = models.DateField('nacimiento', max_length=200, blank=True, null=True)
    identification = models.CharField('Ident.:', max_length=200, unique=True, blank=True, null=True)
    address = models.TextField('direccion', blank=True, null=True)
    telephone = models.CharField('Telefono', max_length=20, blank=True, null=True)
    cellphone = models.CharField('Celular', max_length=20, blank=True, null=True)
    nationality = models.CharField('nacionalidad', max_length=2, choices=NATIONALITY_CHOICES, default='DO',blank=True, null=True)
    marital_status = models.CharField('estado civil', choices=MARITAL_STATUS_CHOICES, max_length=2, blank=True,
                                      null=True)
    status = models.BooleanField('¿Activo?', default=True)
    type = models.CharField('Tipo', choices=TYPE_CHOICES, max_length=200, default='D',blank=True, null=True)
    substitute = models.ForeignKey('self', verbose_name='Sustituto', blank=True, null=True,
                                   help_text='Persona que se encuentra sustituyendo a la titular del carnet',
                                   limit_choices_to={'type': 'S'})

    def save(self, *args, **kwargs):
        tmp_licence = self.licence
        idx = None
        for x in range(0, len(tmp_licence)):
            if x not in (0, 1):
                if tmp_licence[x] != '0':
                    idx = x
                    break
        self.short_licence = tmp_licence[0]+tmp_licence[idx:len(tmp_licence)]
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return '%s/%s' % (self.name, self.licence)


def _auto_increment_commodity():
    return (Commodity.objects.count() or 0) + 1


class Commodity(models.Model):
    class Meta:
        verbose_name = 'Mercancia'
        verbose_name_plural = 'Mercancias'
    code = models.CharField('Codigo', max_length=200, primary_key=True, default=_auto_increment_commodity)
    name = models.CharField('Nombre', max_length=200)
    status = models.BooleanField('¿Activa?', default=True)
    export_price = models.DecimalField('Exportacion', decimal_places=2, max_digits=18, null=True, blank=True, help_text='Precio que se tomara por defecto en la exportación')
    transit_price = models.DecimalField('Transito', decimal_places=2, max_digits=18, null=True, blank=True, help_text='Precio que se tomara por defecto en el transito')
    import_price = models.DecimalField('Importacion', decimal_places=2, max_digits=18, null=True, blank=True, help_text='Precio que se tomara por defecto en la importación ')

    def __str__(self):
        return '%s-%s' % (self.code, self.name)


class EmployeeHistory(models.Model):
    class Meta:
        verbose_name = 'Histórico de Miembro'
        verbose_name_plural = 'Histórico de Miembros'
        ordering = ['name', 'licence', 'identification']

    MARITAL_STATUS_CHOICES = (
        ('C', 'Casado'),
        ('S', 'Soltero'),
        ('D', 'Divorciado'),
        ('V', 'Viudo')
    )
    TYPE_CHOICES = (
        ('D', 'Directo'),
        ('S', 'Sustituto'),
    )
    NATIONALITY_CHOICES = (
        ('DO', 'Dominicano'),
        ('EX', 'Extranjero')
    )
    post_date = models.DateField('Archivado en', auto_now_add=True)
    licence = models.CharField('Carnet', max_length=255)
    short_licence = models.CharField('Carnet Corto', max_length=255,blank=True, null=True)
    name = models.CharField('Nombre', max_length=200, blank=True, null=True)
    bird_date = models.DateField('nacimiento', max_length=200, blank=True, null=True)
    identification = models.CharField('Ident.:', max_length=200, blank=True, null=True)
    address = models.TextField('direccion', blank=True, null=True)
    telephone = models.CharField('Telefono', max_length=20, blank=True, null=True)
    cellphone = models.CharField('Celular', max_length=20, blank=True, null=True)
    nationality = models.CharField('nacionalidad', max_length=2, choices=NATIONALITY_CHOICES, default='DO',blank=True, null=True)
    marital_status = models.CharField('estado civil', choices=MARITAL_STATUS_CHOICES, max_length=2, blank=True,
                                      null=True)
    status = models.BooleanField('¿Activo?', default=True)
    type = models.CharField('Tipo', choices=TYPE_CHOICES, max_length=200, default='D',blank=True, null=True)

    def __str__(self):
        return '%s/%s' % (self.name, self.licence)

from datos_familiares.models import RelativeType


class RelativeHistory(models.Model):
    class Meta:
        verbose_name = 'Miembro de la familia'
        verbose_name_plural = 'Miembros de la familia'

    name = models.CharField('Nombre', max_length=200)
    relationship = models.ForeignKey(RelativeType, verbose_name='Parentesco', default=1)
    employee = models.ForeignKey(EmployeeHistory, verbose_name='Miembro')
    is_dead = models.BooleanField('Defunción')
    death_date = models.DateField('Fecha de defunción', blank=True, null=True)

    def __str__(self):
        return '%s,%s de %s' % (self.name, self.relationship, self.employee,)