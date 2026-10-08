from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Place, Collection, Profile, PlaceImage, Review

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta: model = User; fields = ('username','email','password1','password2')

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name','category','location','description','cover','entry_fee','visiting_time','best_time','things_to_know','featured','trending','hidden_spot')
        widgets = {'description': forms.Textarea(attrs={'rows':5}), 'things_to_know': forms.Textarea(attrs={'rows':4})}

class CollectionForm(forms.ModelForm):
    class Meta: model = Collection; fields = ('name','description')

class ProfileForm(forms.ModelForm):
    class Meta: model = Profile; fields = ('bio','photo')

class GalleryForm(forms.ModelForm):
    class Meta: model = PlaceImage; fields = ('image',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')