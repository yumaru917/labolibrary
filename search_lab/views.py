from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})


def about_for_laboratory(request):
    return render(request, 'about_for_laboratory.html', {})


def disclaimer(request):
    return render(request, 'about/disclaimer.html', {})


def privacy_policy(request):
    return render(request, 'about/privacy_policy.html', {})


def terms_of_service(request):
    return render(request, 'about/terms_of_service.html', {})
