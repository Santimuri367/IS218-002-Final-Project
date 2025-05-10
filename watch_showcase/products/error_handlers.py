from django.shortcuts import render
# Handler for 404 error
def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)
# Handler for 500 error
def handler500(request):
    return render(request, 'errors/500.html', status=500)
# Handler for 403 error
def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)