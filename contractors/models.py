from django.db import models


class Supplier(models.Model):
    code = models.CharField(max_length=10, verbose_name='код')
    name = models.CharField(max_length=50, verbose_name='название')

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'поставщик'
        verbose_name_plural = 'поставщики'


class Client(models.Model):
    code = models.CharField(max_length=10, verbose_name='код')
    name = models.CharField(max_length=50, verbose_name='название')

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Order(models.Model):
    code = models.CharField(max_length=6, verbose_name='код')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
