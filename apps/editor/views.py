from django.shortcuts import render


def editor_home(request):
    return render(request, 'editor/editor_home.html')


