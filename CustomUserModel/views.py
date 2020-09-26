from django.shortcuts import render

# Create your views here.
def Index(request):
    return render(request, 'index.html',{'title':'This is Index Page :)'})