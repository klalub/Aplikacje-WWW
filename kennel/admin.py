from django.contrib import admin
from .models import Breed, Dog, Litter, Puppy, Reservation


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_pattern']


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'breed', 'owner']
    list_filter = ['breed', 'gender']
    search_fields = ['name']


@admin.register(Litter)
class LitterAdmin(admin.ModelAdmin):
    list_display = ['mother', 'father', 'birth_date', 'number_of_puppies', 'is_planned']
    list_filter = ['is_planned']


@admin.register(Puppy)
class PuppyAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'status', 'litter']
    list_filter = ['status', 'gender']
    search_fields = ['name']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['puppy', 'user', 'date_reserved']
    list_filter = ['date_reserved']
