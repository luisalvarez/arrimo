from django.db import models
from parametros_generales.models import Employee


class Person(Employee):
    class Meta:
        verbose_name_plural = 'Familiares'
        verbose_name = 'conjunto de familiares de'
        proxy = True


class RelativeType(models.Model):
    class Meta:
        verbose_name = 'Tipo de pariente'
        verbose_name_plural = 'Tipos de parientes'

    name = models.CharField('Nombre', max_length=200, help_text='Ejemplo: padre, madre, abuela, etc', unique=True)

    def __str__(self):
        return '%s' % (self.name,)


class Relative(models.Model):
    class Meta:
        verbose_name = 'Miembro de la familia'
        verbose_name_plural = 'Miembros de la familia'

    name = models.CharField('Nombre', max_length=200)
    relationship = models.ForeignKey(RelativeType, verbose_name='Parentesco', default=1)
    person = models.ForeignKey(Person, verbose_name='Miembro')
    is_dead = models.BooleanField('Defunción')
    death_date = models.DateField('Fecha de defunción', blank=True, null=True)

    def __str__(self):
        return '%s,%s de %s' % (self.name, self.relationship, self.person,)