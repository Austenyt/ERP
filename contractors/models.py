from django.db import models

from articles.models import Material, Warehouse


class Contractor(models.Model):
    code = models.IntegerField(verbose_name='код', unique=True)
    name = models.CharField(max_length=50, verbose_name='название')

    def __str__(self):
        return f'{self.code}-{self.name}'

    class Meta:
        verbose_name = 'контрагент'
        verbose_name_plural = 'контрагент'
        ordering = ['code']


class Order(models.Model):
    ORDER_STATUS = [
        ('draft', 'Черновик'),
        ('in_progress', 'В производстве'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    code = models.IntegerField(verbose_name='код', unique=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name='контрагент')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    target_warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, verbose_name='склад готовой продукции')

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class Supply(models.Model):
    code = models.IntegerField(verbose_name='код', unique=True)
    supplier = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, verbose_name='поставщик')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, verbose_name='склад')

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'поставка'
        verbose_name_plural = 'поставки'


class Shipping(models.Model):
    code = models.IntegerField(verbose_name='код', unique=True)
    client = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, verbose_name='клиент')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, verbose_name='склад')

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'отгрузка'
        verbose_name_plural = 'отгрузка'


class SupplyMaterial(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.DO_NOTHING, verbose_name='поставка')
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING, verbose_name='материалы')
    quantity = models.FloatField(verbose_name='количество')

    def __str__(self):
        return f'{self.supply.code} {self.material.article}'

    class Meta:
        verbose_name = 'связь поставка-материал'
        verbose_name_plural = 'связи поставка-материал'


class ShippingMaterial(models.Model):
    shipping = models.ForeignKey(Shipping, on_delete=models.DO_NOTHING, verbose_name='отгрузка')
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING, verbose_name='материалы')
    quantity = models.FloatField(verbose_name='количество')

    def __str__(self):
        return f'{self.shipping.code} {self.material.article}'

    class Meta:
        verbose_name = 'связь отгрузка-материал'
        verbose_name_plural = 'связи отгрузка-материал'


# class SupplierMaterial(models.Model):
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Поставщик')
#     material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Материал')
#
#     def __str__(self):
#         return f'{self.supplier.name} - {self.material.name}'
#
#     class Meta:
#         verbose_name = 'материал поставщика'
#         verbose_name_plural = 'материалы поставщиков'
#         unique_together = ('supplier', 'material')
