import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Breed, Dog, Litter, Puppy, Reservation
from datetime import date


# --------------- 1) PRZYKŁAD "ręcznego" Serializer (nie ModelSerializer) ---------------
class DogSerializer(serializers.Serializer):
    """Ręczny serializer – pokazuje create/update, walidację i pola."""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    breed = serializers.PrimaryKeyRelatedField(
        queryset=Breed.objects.all(),
        allow_null=True,
        required=False
    )
    gender = serializers.ChoiceField(choices=Dog.GENDER_CHOICES)
    date_of_birth = serializers.DateField()
    color = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    health_tests = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    # WALIDACJA POLA: name – tylko litery + spacje
    def validate_name(self, value):
        if not all(ch.isalpha() or ch.isspace() for ch in value):
            raise serializers.ValidationError("Imię psa może zawierać tylko litery i spacje.")
        return value

    # WALIDACJA POLA: date_of_birth – nie z przyszłości
    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError("Data urodzenia nie może być z przyszłości.")
        return value

    def create(self, validated_data):
        return Dog.objects.create(**validated_data)

    def update(self, instance, validated_data):
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

    # WALIDACJA OBIEKTU – sprawdzamy relację mother/father
    def validate(self, data):
        mother = data.get('mother')
        father = data.get('father')

        if mother == father:
            raise serializers.ValidationError("Matka i ojciec nie mogą być tym samym psem.")

        if mother and father and mother.gender == father.gender:
            raise serializers.ValidationError("Matka i ojciec muszą mieć różną płeć.")

        return data



class PuppySerializer(serializers.ModelSerializer):
    class Meta:
        model = Puppy
        fields = ['id', 'litter', 'name', 'gender', 'color', 'description', 'status']
        read_only_fields = ['id']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'puppy', 'user', 'date_reserved', 'notes']
        read_only_fields = ['id', 'date_reserved', 'user']

    def validate_puppy(self, value):
        # jeśli szczeniak już ma rezerwację -> błąd
        if Reservation.objects.filter(puppy=value).exists():
            raise serializers.ValidationError("Ten szczeniak jest już zarezerwowany.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user

        # jeszcze raz bezpieczeństwo – gdyby ktoś ominął validate_puppy
        puppy = validated_data['puppy']
        if Reservation.objects.filter(puppy=puppy).exists():
            raise serializers.ValidationError(
                {"puppy": "Ten szczeniak jest już zarezerwowany."}
            )

        reservation = super().create(validated_data)

        # opcjonalnie: zmień status szczeniaka na "reserved"
        puppy.status = 'reserved'
        puppy.save()

        return reservation


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer do rejestracji nowych użytkowników."""
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        # używam create_user, żeby hasło było zahashowane
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

