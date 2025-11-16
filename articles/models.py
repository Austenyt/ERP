from django.db import models


class Material(models.Model):
    article = models.IntegerField(verbose_name='артикул')
    name = models.CharField(max_length=50, verbose_name='наименование')
    unit = models.ForeignKey("Unit", on_delete=models.DO_NOTHING, verbose_name='единица измерения')
    price = models.FloatField(verbose_name='цена')

    def __str__(self):
        return f'{self.article} {self.name}'

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'


class BOM(models.Model):
    article = models.IntegerField(verbose_name='артикул')
    name = models.CharField(max_length=50, verbose_name='наименование')
    unit = models.ForeignKey("Unit", on_delete=models.DO_NOTHING, verbose_name='единица измерения')
    boms = models.ManyToManyField('self', through='BOMtoBOM', symmetrical=False)

    def __str__(self):
        return f'{self.article} {self.name}'

    class Meta:
        verbose_name = 'спецификация'
        verbose_name_plural = 'спецификация'

    @property
    def works(self):
        # return WarehouseBOM.objects.filter(warehouse=self)
        return Work.objects.filter(workbom__bom=self)

    @property
    def materials(self):
        # return WarehouseBOM.objects.filter(warehouse=self)
        return Material.objects.filter(materialbom__bom=self)

    # @property
    # def BOMs(self):
    #     # return WarehouseBOM.objects.filter(warehouse=self)
    #     return BOM.objects.filter(parent=self)


class Unit(models.Model):
    name = models.CharField(max_length=5, verbose_name='единица измерения')
    name_full = models.CharField(max_length=20, verbose_name='полное название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'единица измерения'
        verbose_name_plural = 'единицы измерения'


class Work(models.Model):
    code = models.IntegerField(verbose_name='код')
    name = models.CharField(max_length=50, verbose_name='название')
    price = models.FloatField(verbose_name='цена')

    def __str__(self):
        return f'{self.code} {self.name}'

    class Meta:
        verbose_name = 'работа'
        verbose_name_plural = 'работы'


class Warehouse(models.Model):
    code = models.IntegerField(verbose_name='код')
    name = models.CharField(max_length=50, verbose_name='название')

    def __str__(self):
        return f'{self.code} {self.name}'

    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'склады'

    def blah(self):
        return self.name * 10

    @property
    def BOMs(self):
        # return WarehouseBOM.objects.filter(warehouse=self)
        return BOM.objects.filter(warehousebom__warehouse=self)

    @property
    def count_boms(self):
        return len(self.BOMs)

    @property
    def materials(self):
        # return WarehouseBOM.objects.filter(warehouse=self)
        return Material.objects.filter(warehousematerial__warehouse=self)

    @property
    def count_materials(self):
        return len(self.materials)


class WarehouseMaterial(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, verbose_name='склад')
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING, verbose_name='материал')
    quantity = models.FloatField(verbose_name='количество')

    def __str__(self):
        return f'{self.warehouse.code} {self.material.article}'

    class Meta:
        verbose_name = 'связь склад-материал'
        verbose_name_plural = 'связи склад-материал'
        unique_together = ('warehouse', 'material')


class WarehouseBOM(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, verbose_name='склад')
    bom = models.ForeignKey(BOM, on_delete=models.DO_NOTHING, verbose_name='изделие')
    quantity = models.FloatField(verbose_name='количество')

    def __str__(self):
        return f'{self.warehouse.code} {self.bom.article}'

    class Meta:
        verbose_name = 'связь склад-изделие'
        verbose_name_plural = 'связи склад-изделие'


class MaterialBOM(models.Model):
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING, verbose_name='материал')
    bom = models.ForeignKey(BOM, on_delete=models.DO_NOTHING, verbose_name='изделие')
    quantity = models.FloatField(verbose_name='количество')

    def __str__(self):
        return f'{self.material.article} {self.bom.article}'

    class Meta:
        verbose_name = 'связь материал-изделие'
        verbose_name_plural = 'связи материал-изделие'


class WorkBOM(models.Model):
    work = models.ForeignKey(Work, on_delete=models.DO_NOTHING, verbose_name='работа')
    bom = models.ForeignKey(BOM, on_delete=models.DO_NOTHING, verbose_name='изделие')
    quantity = models.FloatField(verbose_name='количество')

    def __str__(self):
        return f'{self.work.code} {self.bom.article}'

    class Meta:
        verbose_name = 'связь работа-изделие'
        verbose_name_plural = 'связи работа-изделие'


class BOMtoBOM(models.Model):
    parent = models.ForeignKey(BOM, on_delete=models.DO_NOTHING, verbose_name='работа', related_name='childok')
    child = models.ForeignKey(BOM, on_delete=models.DO_NOTHING, verbose_name='изделие', related_name='parentok')
    quantity = models.FloatField(verbose_name='количество')

    def __str__(self):
        return f'{self.parent.article} {self.child.article}'

    class Meta:
        verbose_name = 'связь изделие-изделие'
        verbose_name_plural = 'связи изделие-изделие'


class MaterialUnit(models.Model):
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING, verbose_name='материал')
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, verbose_name='единица измерения')
    quantity = models.FloatField(verbose_name='количество')

    def __str__(self):
        return f'{self.material.article} {self.unit.name}'

    class Meta:
        verbose_name = 'связь материал-единица измерения'
        verbose_name_plural = 'связи материал-единица измерения'
