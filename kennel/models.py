from django.db import models
from django.contrib.auth.models import User


# ️Model rasy psa (opcjonalny, ale fajny do filtrów)
class Breed(models.Model):
    name = models.CharField(max_length=100)
    color_pattern = models.CharField(max_length=100, blank=True, null=True)  # np. black-white, red-merle
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']  # sortuj alfabetycznie

    def __str__(self):
        return self.name


# Model pies (suki, reproduktory)
class Dog(models.Model):
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
    ]

    name = models.CharField(max_length=100)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    color = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    health_tests = models.TextField(blank=True, null=True)  # np. "CEA: clear, MDR1: carrier"
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_gender_display()})"


# Model miotu (Litter)
class Litter(models.Model):
    mother = models.ForeignKey(Dog, related_name='mother_litters', on_delete=models.CASCADE)
    father = models.ForeignKey(Dog, related_name='father_litters', on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    number_of_puppies = models.PositiveIntegerField(default=0)
    is_planned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-birth_date']

    def __str__(self):
        return f"Litter from {self.mother.name} & {self.father.name}"


# Model szczeniaka (Puppy)
class Puppy(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
    ]

    litter = models.ForeignKey(Litter, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=Dog.GENDER_CHOICES)
    color = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"


# Model rezerwacji (Reservation)
class Reservation(models.Model):
    puppy = models.ForeignKey(Puppy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reserved = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reservation for {self.puppy.name} by {self.user.username}"
