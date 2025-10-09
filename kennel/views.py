from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello from Border Collie Kennel 🐶 — BorderHeart — Works!")

