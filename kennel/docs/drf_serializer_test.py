from django.contrib.auth.models import User
from kennel.models import Breed, Dog, Litter, Puppy, Reservation
from kennel.serializers import DogSerializer, BreedSerializer, PuppySerializer, ReservationSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

u = User.objects.create_user(username='client1', password='test123')
b = Breed.objects.create(name='Border Collie', color_pattern='black-white')
d = Dog.objects.create(
    name='Aiko',
    breed=b,
    gender='F',
    date_of_birth='2023-06-01',
    color='black-white',
    owner=u
)

s = DogSerializer(d)
s.data
# spodziewane: dict z polami psa (id, name, breed, ...)

JSONRenderer().render(s.data)
# spodziewane: bajty JSON

payload = {'name': 'Aiko', 'breed': b.id, 'gender': 'F', 'date_of_birth': '2023-06-01',
           'color': 'red-merle', 'owner': u.id}
stream = io.BytesIO(JSONRenderer().render(payload))
data = JSONParser().parse(stream)

des = DogSerializer(instance=d, data=data)
des.is_valid()
des.errors  # puste jeśli OK
obj = des.save()  # update()
obj.color  # 'red-merle'

# przygotuj miot i szczeniaka
dad = Dog.objects.create(name='Blaze', breed=b, gender='M', date_of_birth='2022-05-10', color='black-white', owner=u)
l = Litter.objects.create(mother=d, father=dad, birth_date='2024-01-10', number_of_puppies=1, is_planned=False)

puppy_data = {'litter': l.id, 'name': 'Misu', 'gender': 'M', 'color': 'black', 'status': 'available'}
ps = PuppySerializer(data=puppy_data)
ps.is_valid()
ps.errors  # puste jeśli OK
p = ps.save()  # create()
PuppySerializer(p).data  # dane utworzonego szczeniaka

res_data = {'puppy': p.id, 'user': u.id, 'notes': 'Rezerwacja wstępna'}
rs = ReservationSerializer(data=res_data)
rs.is_valid()
rs.errors
res = rs.save()
ReservationSerializer(res).data

