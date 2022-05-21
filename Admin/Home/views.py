from django.shortcuts import render


def admin_home_view(request):
    return render(request, 'Admin/admin_home.html')
