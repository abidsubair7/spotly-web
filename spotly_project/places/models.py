from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=180, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self): return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Place(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='places')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='places')
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=180)
    description = models.TextField()
    cover = models.ImageField(upload_to='places/', blank=True)
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    visiting_time = models.CharField(max_length=100, blank=True)
    best_time = models.CharField(max_length=100, blank=True)
    things_to_know = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    hidden_spot = models.BooleanField(default=False)
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']
    def __str__(self): return self.name
    @property
    def average_rating(self):
        value = self.reviews.aggregate(avg=models.Avg('rating'))['avg']
        return round(value or 0, 1)
    @property
    def review_count(self): return self.reviews.count()

class PlaceImage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='place_gallery/')

class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['place','user'], name='unique_place_review')]

class SavedPlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_places')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='saved_by')
    class Meta: unique_together = ('user','place')

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=220, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class CollectionPlace(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    class Meta: unique_together = ('collection','place')
