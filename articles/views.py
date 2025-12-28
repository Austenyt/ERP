from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from contractors.models import Contractor
from .models import *


# def list_warehouses(request):
#     warehouses_test = Warehouse.objects.all()
#
#     return render(request, 'all.html', {'warehouses': warehouses_test})


def index(request):
    return render(request, 'index.html')


def list_materials(request):
    search_query = request.GET.get('search', '')

    materials = Material.objects.all()
    boms = BOM.objects.all()

    if search_query:
        materials = materials.filter(
            Q(article__icontains=search_query) |
            Q(name__icontains=search_query)
        )
        boms = boms.filter(
            Q(article__icontains=search_query) |
            Q(name__icontains=search_query)
        )
    return render(request, 'materials.html', {
        'materials': materials,
        'boms': boms,
        'search_query': search_query
    })


def list_boms(request):
    search_query = request.GET.get('search', '')
    boms = BOM.objects.all()
    if search_query:
        boms = boms.filter(
            Q(article__icontains=search_query) |
            Q(name__icontains=search_query)
        )
    return render(request, 'boms.html', {'boms': boms, 'search_query': search_query})


def list_warehouses(request):
    warehouses = Warehouse.objects.all()  # Получить все склады
    return render(request, 'warehouses.html', {'warehouses': warehouses})


def list_works(request):
    works = Work.objects.all()
    return render(request, 'works.html', {'works': works})


def detail_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return render(request, 'detail_material.html', {'material': material})


def detail_bom(request, pk):
    bom = get_object_or_404(BOM, pk=pk)
    materials = MaterialBOM.objects.filter(bom=bom)
    context = {
        'bom': bom,
        'materials': materials,
    }
    return render(request, 'detail_bom.html', context)


def detail_warehouse(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    warehouse_materials = WarehouseMaterial.objects.filter(
        warehouse=warehouse
    ).select_related('material', 'material__unit')

    return render(request, 'detail_warehouse.html', {
        'warehouse': warehouse,
        'warehouse_materials': warehouse_materials
    })


def detail_work(request, pk):
    work = get_object_or_404(Work, pk=pk)
    return render(request, 'detail_work.html', {'work': work})


def create_material(request):
    last_material = Material.objects.order_by("-id").all()
    if last_material:
        last_material = last_material.first()
        article = last_material.article + 1
    else:
        article = 1000000
    if request.method == "POST":
        name = request.POST.get('name')
        unit = request.POST.get('unit')
        price = request.POST.get('price')
        supplier_id = request.POST.get('supplier')

        material = Material.objects.create(
            article=article,
            name=name,
            unit_id=unit,
            price=price,
            supplier=supplier_id,
        )
        return redirect('materials')

    units = Unit.objects.all()
    suppliers = Contractor.objects.all()
    return render(request, 'create_material.html', {
        'units': units,
        'article': article,
        'suppliers': suppliers
    })


def delete_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        return redirect('materials')
    return render(request, 'confirm_delete_material.html', {'material': material})


def create_bom(request):
    """Контроллер для создания спецификации"""

    # Получаем ID единицы измерения "шт"
    try:
        unit_st = Unit.objects.get(name='шт')
        unit_st_id = unit_st.id
    except Unit.DoesNotExist:
        # Если единица "шт" не найдена, создаем ее
        unit_st = Unit.objects.create(name='шт', name_full='Штука')
        unit_st_id = unit_st.id

    # Подготовка данных для формы
    materials = Material.objects.all()
    boms = BOM.objects.all()

    # GET запрос - показ формы
    if request.method == "GET":
        return render(request, 'create_bom.html', {
            'materials': materials,
            'boms': boms,
            'unit_st_id': unit_st_id,
        })

    # POST запрос - создание спецификации
    elif request.method == "POST":
        try:
            # === 1. Основные данные ===
            article = request.POST.get('article')
            name = request.POST.get('name')

            # Проверка обязательных полей
            if not all([article, name]):
                raise ValueError("Артикул и наименование обязательны для заполнения")

            # Проверка уникальности артикула
            if BOM.objects.filter(article=article).exists():
                raise ValueError("Спецификация с таким артикулом уже существует")

            # === 2. Создание основной спецификации ===
            # Используем фиксированную единицу измерения "шт"
            bom = BOM.objects.create(
                article=article,
                name=name,
                unit_id=unit_st_id,  # Всегда используем "шт"
            )

            # === 3. Обработка материалов ===
            materials_count = 0
            i = 0
            while True:
                material_key = f'materials[{i}][material_id]'
                quantity_key = f'materials[{i}][quantity]'

                if material_key not in request.POST:
                    break

                material_id = request.POST.get(material_key)
                quantity = request.POST.get(quantity_key)

                if material_id and quantity:
                    try:
                        quantity = float(quantity)
                        if quantity <= 0:
                            raise ValueError("Количество должно быть положительным числом")

                        MaterialBOM.objects.create(
                            bom=bom,
                            material_id=material_id,
                            quantity=quantity
                        )
                        materials_count += 1
                    except (ValueError, TypeError):
                        raise ValueError(f"Некорректное количество для материала")

                i += 1

            # === 4. Обработка вложенных спецификаций ===
            boms_count = 0
            i = 0
            while True:
                bom_key = f'boms[{i}][bom_id]'
                quantity_key = f'boms[{i}][quantity]'

                if bom_key not in request.POST:
                    break

                bom_id = request.POST.get(bom_key)
                quantity = request.POST.get(quantity_key)

                if bom_id and quantity:
                    try:
                        quantity = float(quantity)
                        if quantity <= 0:
                            raise ValueError("Количество должно быть положительным числом")

                        # Проверка на добавление самой себе
                        if int(bom_id) == bom.id:
                            raise ValueError("Нельзя добавлять спецификацию в саму себя")

                        BOMtoBOM.objects.create(
                            parent=bom,
                            child_id=bom_id,
                            quantity=quantity
                        )
                        boms_count += 1
                    except (ValueError, TypeError):
                        raise ValueError(f"Некорректное количество для спецификации")

                i += 1

            # === 5. Финальная проверка ===
            if materials_count == 0 and boms_count == 0:
                bom.delete()  # Удаляем пустую спецификацию
                raise ValueError("Добавьте хотя бы один материал или вложенную спецификацию")

            # === 6. Успешное завершение ===
            return redirect('boms')

        except Exception as e:
            # Обработка ошибок
            return render(request, 'create_bom.html', {
                'materials': materials,
                'boms': boms,
                'unit_st_id': unit_st_id,
                'error': str(e),
                'form_data': request.POST
            })


def create_work(request):
    if request.method == "POST":
        code = request.POST.get('code')
        name = request.POST.get('name')
        price = request.POST.get('price')

        work = Work.objects.create(
            code=code,
            name=name,
            price=price,
        )
        return redirect('works')
    return render(request, 'create_work.html')


def list_movements(request):
    search_query = request.GET.get('search', '')

    supplies = Supply.objects.all().select_related('supplier', 'warehouse')
    shippings = Shipping.objects.all().select_related('client', 'warehouse')

    if search_query:
        supplies = supplies.filter(
            Q(code__icontains=search_query) |
            Q(supplier__name__icontains=search_query) |
            Q(warehouse__name__icontains=search_query)
        )

        shippings = shippings.filter(
            Q(code__icontains=search_query) |
            Q(client__name__icontains=search_query) |
            Q(warehouse__name__icontains=search_query)
        )

    return render(request, 'movements.html', {
        'supplies': supplies,
        'shippings': shippings,
        'search_query': search_query
    })
