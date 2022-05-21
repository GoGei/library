from django.shortcuts import render


def library_home_view(request):
    return render(request, 'Public/library_home.html')
