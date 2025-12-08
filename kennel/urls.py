from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # stara strona powitalna:
    path('', views.home, name='home'),

    # ---- AUTH ----
    path('api/auth/register/', api_views.register_user, name='register'),
    path('api/auth/login/', api_views.obtain_auth_token, name='login'),

    # ---- API RESERVATIONS ----
    path('api/reservations/', api_views.reservation_list, name='reservation-list'),
    path('api/reservations/<int:pk>/', api_views.reservation_detail, name='reservation-detail'),

    # ---- API BREED ----
    path('api/breeds/', api_views.breed_list, name='breed-list'),
    path('api/breeds/<int:pk>/', api_views.breed_detail, name='breed-detail'),
    path('api/breeds/search/', api_views.breed_search, name='breed-search'),

    # ---- API DOG ----
    path('api/dogs/', api_views.dog_list, name='dog-list'),
    path('api/dogs/<int:pk>/', api_views.dog_detail, name='dog-detail'),
    path('api/dogs/search/', api_views.dog_search, name='dog-search'),

    # ---- API LITTER ----
    path('api/litters/', api_views.litter_list, name='litter-list'),
    path('api/litters/<int:pk>/', api_views.litter_detail, name='litter-detail'),
    path('api/litters/<int:pk>/puppies/', api_views.litter_puppies, name='litter-puppies'),

    # ---- API PUPPY ----
    path('api/puppies/', api_views.puppy_list, name='puppy-list'),
    path('api/puppies/<int:pk>/', api_views.puppy_detail, name='puppy-detail'),
    path('api/puppies/search/', api_views.puppy_search, name='puppy-search'),
]
