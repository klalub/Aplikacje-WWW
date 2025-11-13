from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Breed, Dog, Puppy
from .serializers import BreedSerializer, DogSerializer, PuppySerializer


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
