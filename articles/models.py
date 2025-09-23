from django.db import models


class Material(models.Model):
    article = models.IntegerField(verbose_name='артикул')
    name = models.CharField(max_length=50, verbose_name='наименование')
    unit = models.CharField(max_length=3, verbose_name='единица измерения')
    price = models.FloatField(verbose_name='цена')

    def __str__(self):
        return f'{self.article}'

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'


class Product(models.Model):
    article = models.IntegerField(verbose_name='артикул')
    name = models.CharField(max_length=50, verbose_name='наименование')
    unit = models.CharField(max_length=3, verbose_name='единица измерения')
    price = models.FloatField(verbose_name='цена')

    def __str__(self):
        return f'{self.article}'

    class Meta:
        verbose_name = 'изделие'
        verbose_name_plural = 'изделия'


class BOM(models.Model):
    article = models.IntegerField(verbose_name='артикул')
    name = models.CharField(max_length=50, verbose_name='наименование')
    unit = models.CharField(max_length=3, verbose_name='единица измерения')

    def __str__(self):
        return f'{self.article}'

    class Meta:
        verbose_name = 'спецификация'
        verbose_name_plural = 'спецификация'


class Work(models.Model):
    code = models.IntegerField(verbose_name='код')
    name = models.CharField(max_length=50, verbose_name='название')
    price = models.FloatField(verbose_name='цена')

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'работа'
        verbose_name_plural = 'работы'


class Warehouse(models.Model):
    code = models.IntegerField(verbose_name='код')
    name = models.CharField(max_length=50, verbose_name='название')

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'склады'


class WarehouseMaterial(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='склад')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='материал')

    def __str__(self):
        return f'{self.warehouse.code} {self.material.article}'

    class Meta:
        verbose_name = 'связь склад-материал'
        verbose_name_plural = 'связи склад-материал'


class WarehouseProduct(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='склад')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='изделие')

    def __str__(self):
        return f'{self.warehouse.code} {self.product.article}'

    class Meta:
        verbose_name = 'связь склад-изделие'
        verbose_name_plural = 'связи склад-изделие'


class MaterialProduct(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='материал')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='изделие')

    def __str__(self):
        return f'{self.material.article} {self.product.article}'

    class Meta:
        verbose_name = 'связь материал-изделие'
        verbose_name_plural = 'связи материал-изделие'
