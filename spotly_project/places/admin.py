from django.contrib import admin
from .models import *
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): list_display=('user','is_verified'); list_filter=('is_verified',); list_editable=('is_verified',); search_fields=('user__username','user__email')
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin): list_display=('name','owner','category','approved','featured','trending','hidden_spot'); list_filter=('approved','featured','trending','hidden_spot','category'); list_editable=('approved','featured','trending','hidden_spot'); search_fields=('name','location')
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin): list_display=('place','user','rating','created_at'); list_filter=('rating',); search_fields=('place__name','user__username')
admin.site.register(Category); admin.site.register(PlaceImage); admin.site.register(SavedPlace); admin.site.register(Collection); admin.site.register(CollectionPlace)
