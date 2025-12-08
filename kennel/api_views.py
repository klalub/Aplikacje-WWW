from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Breed, Dog, Puppy, Litter, Reservation
from .serializers import (
    BreedSerializer,
    DogSerializer,
    PuppySerializer,
    LitterSerializer,
    ReservationSerializer,
    UserRegisterSerializer,
)

# ------------- BREED ------------- #

@api_view(['GET', 'POST'])
def breed_list(request):
    """
    GET: lista wszystkich ras
    POST: dodanie nowej rasy
    """
    if request.method == 'GET':
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = BreedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def breed_detail(request, pk):
    """
    Operacje na pojedynczej rasie (Breed).
    """
    try:
        breed = Breed.objects.get(pk=pk)
    except Breed.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BreedSerializer(breed)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BreedSerializer(breed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        breed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def breed_search(request):
    """
    Lista ras, których nazwa zawiera zadany fragment ?q=...
    """
    query = request.GET.get('q', '')
    breeds = Breed.objects.filter(name__icontains=query)
    serializer = BreedSerializer(breeds, many=True)
    return Response(serializer.data)


# ------------- DOG ------------- #

@api_view(['GET', 'POST'])
def dog_list(request):
    """
    GET: lista wszystkich psów
    POST: dodanie nowego psa
    """
    if request.method == 'GET':
        dogs = Dog.objects.all()
        serializer = DogSerializer(dogs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = DogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def dog_detail(request, pk):
    """
    Operacje na pojedynczym psie (Dog).
    """
    try:
        dog = Dog.objects.get(pk=pk)
    except Dog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DogSerializer(dog)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DogSerializer(dog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        dog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def dog_search(request):
    """
    Lista psów, których imię zawiera zadany fragment ?q=...
    """
    query = request.GET.get('q', '')
    dogs = Dog.objects.filter(name__icontains=query)
    serializer = DogSerializer(dogs, many=True)
    return Response(serializer.data)

# ------------- LITTER ------------- #

@api_view(['GET', 'POST'])
def litter_list(request):
    """
    GET: lista wszystkich miotów
    POST: dodanie nowego miotu
    """
    if request.method == 'GET':
        litters = Litter.objects.all()
        serializer = LitterSerializer(litters, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = LitterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def litter_detail(request, pk):
    """
    Operacje na pojedynczym miocie (Litter).
    """
    try:
        litter = Litter.objects.get(pk=pk)
    except Litter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LitterSerializer(litter)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LitterSerializer(litter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Opcja bezpieczna: nie pozwalamy usunąć miotu, jeśli ma szczenięta
        if Puppy.objects.filter(litter=litter).exists():
            return Response(
                {"detail": "Nie można usunąć miotu, który ma przypisane szczenięta."},
                status=status.HTTP_400_BAD_REQUEST
            )

        litter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def litter_puppies(request, pk):
    """
    Lista szczeniąt należących do danego miotu.
    /api/litters/<pk>/puppies/
    """
    try:
        litter = Litter.objects.get(pk=pk)
    except Litter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    puppies = Puppy.objects.filter(litter=litter)
    serializer = PuppySerializer(puppies, many=True)
    return Response(serializer.data)

# ------------- PUPPY ------------- #

@api_view(['GET', 'POST'])
def puppy_list(request):
    """
    GET: lista szczeniąt
    POST: dodanie szczeniaka
    """
    if request.method == 'GET':
        puppies = Puppy.objects.all()
        serializer = PuppySerializer(puppies, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PuppySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def puppy_detail(request, pk):
    """
    Operacje na pojedynczym szczeniaku.
    """
    try:
        puppy = Puppy.objects.get(pk=pk)
    except Puppy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PuppySerializer(puppy)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PuppySerializer(puppy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        puppy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def puppy_search(request):
    """
    Lista szczeniąt, których imię zawiera zadany fragment ?q=...
    """
    query = request.GET.get('q', '')
    puppies = Puppy.objects.filter(name__icontains=query)
    serializer = PuppySerializer(puppies, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reservation_list(request):
    """
    GET: lista rezerwacji zalogowanego użytkownika
    POST: utworzenie nowej rezerwacji dla szczeniaka
    """
    if request.method == 'GET':
        if request.user.is_staff:
            qs = Reservation.objects.all()
        else:
            qs = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(qs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ReservationSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            reservation = serializer.save()
            return Response(
                ReservationSerializer(reservation).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------- RESERVATION ------------- #
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reservation_detail(request, pk):
    """
    DELETE: anulowanie rezerwacji (user może usuwać swoje, admin wszystkie).
    """
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # zwykły user może usunąć tylko swoją rezerwację
    if not request.user.is_staff and reservation.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    # przed usunięciem przywróć status szczeniaka na available
    puppy = reservation.puppy
    reservation.delete()
    puppy.status = 'available'
    puppy.save()

    return Response(status=status.HTTP_204_NO_CONTENT)

# ------------- AUTH ------------- #
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Rejestracja nowego użytkownika.
    """
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # tworzymy token od razu po rejestracji
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'id': user.id,
                'username': user.username,
                'token': token.key,
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_auth_token(request):
    """
    Logowanie: przyjmuje username + password, zwraca token.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'detail': 'Podaj username i password.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {'detail': 'Nieprawidłowe dane logowania.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not user.check_password(password):
        return Response(
            {'detail': 'Nieprawidłowe dane logowania.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})
