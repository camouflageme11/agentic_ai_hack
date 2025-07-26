from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def listener(request):
    return render(request, 'listener.html')

def judge(request):
    return render(request, 'judge.html')

def scanner(request):
    return render(request, 'scanner.html')

def artist(request):
    return render(request, 'artist.html')  

def telescope(request):
    return render(request, 'telescope.html')

def guide(request):
    return render(request, 'guide.html')

def messenger(request):
    return render(request, 'messenger.html')