from django.core.management.base import BaseCommand
from places.models import Category,Place
from django.contrib.auth.models import User
from django.utils.text import slugify
class Command(BaseCommand):
 def handle(self,*args,**kwargs):
  cats=['Mountains','Beaches','Cafes','Waterfalls','Photography','Hidden Spots']
  for n in cats: Category.objects.get_or_create(name=n,defaults={'slug':slugify(n)})
  u,_=User.objects.get_or_create(username='spotlydemo'); u.set_password('spotly123'); u.save()
  for name,cat,loc in [('Munnar View Point','Mountains','Munnar, Kerala'),('Vagamon Pine Forest','Photography','Vagamon, Kerala'),('Kappad Beach','Beaches','Kozhikode, Kerala')]:
   c=Category.objects.get(name=cat); Place.objects.get_or_create(name=name,owner=u,category=c,defaults={'location':loc,'description':'A beautiful place to explore and save on Spotly.','featured':True,'trending':True})
  self.stdout.write(self.style.SUCCESS('Demo data ready. Login: spotlydemo / spotly123'))
