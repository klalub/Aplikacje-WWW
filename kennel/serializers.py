from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Breed, Dog, Litter, Puppy, Reservation


# --------------- 1) PRZYKŁAD "ręcznego" Serializer (nie ModelSerializer) ---------------
class DogSerializer(serializers.Serializer):
    """Ręczny serializer – pokazuje create/update walidację i pola."""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    breed = serializers.PrimaryKeyRelatedField(queryset=Breed.objects.all(), allow_null=True, required=False)
    gender = serializers.ChoiceField(choices=Dog.GENDER_CHOICES)
    date_of_birth = serializers.DateField()
    color = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    health_tests = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        # tworzymy nowego psa na podstawie przefiltrowanych danych
        return Dog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # aktualizujemy istniejącego psa – tylko to, co przyszło w danych
        instance.name = validated_data.get('name', instance.name)
        instance.breed = validated_data.get('breed', instance.breed)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.color = validated_data.get('color', instance.color)
        instance.description = validated_data.get('description', instance.description)
        instance.health_tests = validated_data.get('health_tests', instance.health_tests)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance


# --------------- 2) Reszta modeli jako ModelSerializer (krócej i wygodniej) ---------------
class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name', 'color_pattern', 'description']
        read_only_fields = ['id']


class LitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Litter
        fields = ['id', 'mother', 'father', 'birth_date', 'number_of_puppies', 'is_planned']
        read_only_fields = ['id']


class PuppySerializer(serializers.ModelSerializer):
    class Meta:
        model = Puppy
        fields = ['id', 'litter', 'name', 'gender', 'color', 'description', 'status']
        read_only_fields = ['id']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'puppy', 'user', 'date_reserved', 'notes']
        read_only_fields = ['id', 'date_reserved']
