from django.shortcuts import render, get_object_or_404, redirect
from .models import Material, Category, Comment


# --- Список всех материалов + фильтрация по категории ---
def material_list(request):
    category_id = request.GET.get('category')

    if category_id:
        materials = Material.objects.filter(category_id=category_id)
    else:
        materials = Material.objects.all()

    categories = Category.objects.all()

    return render(request, 'materials/material_list.html', {
        'materials': materials,
        'categories': categories,
    })


# --- Просмотр одного материала и добавление комментариев ---
def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    comments = material.comments.all()

    if request.method == 'POST':
        author = request.POST.get('author')
        text = request.POST.get('text')
        if author and text:
            Comment.objects.create(material=material, author=author, text=text)
            return redirect('materials:material_detail', pk=pk)

    return render(request, 'materials/material_detail.html', {
        'material': material,
        'comments': comments,
    })


# --- Создание нового материала ---
def material_create(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        resource = request.POST.get('resource')
        category_id = request.POST.get('category')

        if title and description and category_id:
            category = get_object_or_404(Category, pk=category_id)
            Material.objects.create(
                title=title,
                description=description,
                resource=resource,
                category=category
            )
            return redirect('materials:material_list')

    return render(request, 'materials/material_form.html', {
        'categories': categories,
        'material': None  # Чтобы шаблон понял, что мы создаём новый материал
    })


# --- Редактирование существующего материала ---
def material_update(request, pk):
    material = get_object_or_404(Material, pk=pk)
    categories = Category.objects.all()

    if request.method == 'POST':
        material.title = request.POST.get('title')
        material.description = request.POST.get('description')
        material.resource = request.POST.get('resource')
        category_id = request.POST.get('category')
        if category_id:
            material.category = get_object_or_404(Category, pk=category_id)
        material.save()
        return redirect('materials:material_list')

    return render(request, 'materials/material_form.html', {
        'material': material,
        'categories': categories
    })


# --- Удаление материала ---
def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if request.method == 'POST':
        material.delete()
        return redirect('materials:material_list')

    return render(request, 'materials/material_delete_confirmation.html', {
        'material': material,
    })
