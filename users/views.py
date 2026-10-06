from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('users:profile')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:profile')
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:profile')
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile_views(request):
    return render(request, 'users/profile.html', {'user': request.user})


# ИСПРАВЛЕНО: убрал лишний запрос к базе. request.user и так уже объект User.
@login_required
def account_details(request):
    return render(request, 'users/partials/account_details.html', {'user': request.user})


# ИСПРАВЛЕНО: теперь возвращает форму редактирования, а не просмотр профиля.
@login_required
def edit_account_details(request):
    form = CustomUserUpdateForm(instance=request.user)
    # ИСПРАВЛЕНО: правильное имя шаблона
    return render(request, 'users/partials/edit_account_form.html', {'form': form})


@login_required
def update_account_details(request):
    user = request.user

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            # Просто сохраняем форму. Не нужно commit=False, clean() и save() по отдельности.
            user = form.save()
            # Возвращаем обновлённые данные профиля (для HTMX)
            return render(request, 'users/partials/account_details.html', {'user': user})
        else:
            # Если форма с ошибками — возвращаем её обратно.
            # ВНИМАНИЕ: шаблон должен называться edit_account_form.html, а не edit_account_form.html
            return render(request, 'users/partials/edit_account_form.html', {'form': form})

    # Если кто-то зашёл по GET на этот URL — просто показываем данные профиля
    return render(request, 'users/partials/account_details.html', {'user': user})


# ИСПРАВЛЕНО: убрал двойное двоеточие :: и сделал редирект на логин после выхода.
def logout_view(request):
    logout(request)
    return redirect('users:login')