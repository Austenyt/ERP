# inventory/admin.py (или как называется твое приложение)
from django.contrib import admin
from .models import (
    Material, BOM, Unit, Work, Warehouse,
    WarehouseMaterial, WarehouseBOM, MaterialBOM,
    WorkBOM, BOMtoBOM
)


# Инлайны для связанных моделей (чтобы редактировать их в форме родителя)
class WarehouseMaterialInline(admin.TabularInline):  # Табличный инлайн для удобства
    model = WarehouseMaterial
    extra = 1  # Сколько пустых строк добавлять по умолчанию


class WarehouseBOMInline(admin.TabularInline):
    model = WarehouseBOM
    extra = 1


class MaterialBOMInline(admin.TabularInline):
    model = MaterialBOM
    extra = 1


class WorkBOMInline(admin.TabularInline):
    model = WorkBOM
    extra = 1


class BOMtoBOMInline(admin.TabularInline):
    model = BOMtoBOM
    fk_name = 'parent'  # Указываем, что это для родителя
    extra = 1


# Кастомизация для каждой модели
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'unit', 'price')  # Показываем ключевые поля
    list_filter = ('unit',)  # Фильтр по единице измерения
    search_fields = ('article', 'name')  # Поиск по артикулу и названию
    ordering = ('article',)
    inlines = [WarehouseMaterialInline, MaterialBOMInline]  # Инлайны для связей


@admin.register(BOM)
class BOMAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'unit')
    list_filter = ('unit',)
    search_fields = ('article', 'name')
    ordering = ('article',)
    inlines = [WarehouseBOMInline, MaterialBOMInline, WorkBOMInline, BOMtoBOMInline]  # Все связи с BOM


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_full')
    search_fields = ('name', 'name_full')
    ordering = ('name',)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price')
    search_fields = ('code', 'name')
    ordering = ('code',)
    inlines = [WorkBOMInline]


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)
    inlines = [WarehouseMaterialInline, WarehouseBOMInline]


# Простая регистрация для связующих моделей (без инлайнов, так как они уже в родителях)
admin.site.register(WarehouseMaterial)
admin.site.register(WarehouseBOM)
admin.site.register(MaterialBOM)
admin.site.register(WorkBOM)
admin.site.register(BOMtoBOM)
