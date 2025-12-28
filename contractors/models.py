from django.db import models


class Contractor(models.Model):
    code = models.IntegerField(verbose_name='код', unique=True)
    name = models.CharField(max_length=50, verbose_name='название')

    def __str__(self):
        return f'{self.code}-{self.name}'

    class Meta:
        verbose_name = 'контрагент'
        verbose_name_plural = 'контрагент'
        ordering = ['code']
