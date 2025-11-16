from django.shortcuts import render, get_object_or_404, redirect

from contractors.models import Contractor


def list_contractors(request):
    contractors = Contractor.objects.all()
    return render(request, 'contractors.html', {'contractors': contractors})


def detail_contractor(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)
    return render(request, 'detail_contractor.html', {'contractor': contractor})


def create_contractor(request):
    last_contractor = Contractor.objects.order_by("-id").all()
    if last_contractor:
        last_contractor = last_contractor.first()
        code = last_contractor.code + 1
    else:
        code = 3000
    if request.method == "POST":
        name = request.POST.get('name')

        contractor = Contractor.objects.create(
            code=code,
            name=name,
        )
        return redirect('contractors')
    return render(request, 'create_contractor.html', {'code': code})
