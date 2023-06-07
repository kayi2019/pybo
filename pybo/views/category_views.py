from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import CategoryForm
from ..models import Category




@login_required(login_url='common:login')  # login_url='common:login' 처럼 로그인 URL을 지정할 수 있다.
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('pybo:index')
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'pybo/category_form.html', context)

@login_required(login_url='common:login')
def category_modify(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.user != category.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:index')
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('pybo:index')
    else:
        form = CategoryForm(instance=category)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if not request.user.is_superuser:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:index')
    category.delete()
    return redirect('pybo:index')