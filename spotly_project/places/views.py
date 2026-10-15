import json, os, secrets
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from .models import Place, Review, SavedPlace

def ensure_profile(user): Profile.objects.get_or_create(user=user)

def home(request):
    places = Place.objects.filter(approved=True).select_related('category','owner__profile').prefetch_related('reviews')
    return render(request,'places/home.html', {'featured':places.filter(featured=True)[:6], 'trending':places.filter(trending=True)[:6], 'recent':places[:8], 'categories':Category.objects.all()[:8]})

def explore(request):
    qs = Place.objects.filter(approved=True).select_related('category','owner__profile').prefetch_related('reviews')
    q, cat = request.GET.get('q','').strip(), request.GET.get('category','')
    if q: qs = qs.filter(Q(name__icontains=q)|Q(location__icontains=q)|Q(description__icontains=q))
    if cat: qs = qs.filter(category__slug=cat)
    return render(request,'places/explore.html', {'places':qs,'categories':Category.objects.all(),'q':q,'cat':cat})

def place_detail(request, pk):
    p = get_object_or_404(Place.objects.select_related('category','owner__profile').prefetch_related('images','reviews__user__profile'), pk=pk, approved=True)
    saved = request.user.is_authenticated and SavedPlace.objects.filter(user=request.user,place=p).exists()
    existing_review = Review.objects.filter(user=request.user, place=p).first() if request.user.is_authenticated else None
    review_form = ReviewForm(instance=existing_review)
    return render(request,'places/place_detail.html', {'place':p,'saved':saved,'review_form':review_form,'existing_review':existing_review})

def register(request):
    if request.method == 'POST':
        f=RegisterForm(request.POST)
        if f.is_valid(): user=f.save(); ensure_profile(user); login(request,user); messages.success(request,'Welcome to Spotly!'); return redirect('home')
    else: f=RegisterForm()
    return render(request,'places/register.html',{'form':f})

@login_required
@login_required
def review_place(request, pk):
    p = get_object_or_404(Place, pk=pk, approved=True)

    if request.method != 'POST':
        return redirect('place_detail', pk=pk)

    existing_review = Review.objects.filter(
        user=request.user,
        place=p
    ).first()

    f = ReviewForm(
        request.POST,
        instance=existing_review
    )

    if f.is_valid():
        review = f.save(commit=False)
        review.user = request.user
        review.place = p
        review.save()

        messages.success(
            request,
            'Your review has been saved.'
        )
    else:
        messages.error(
            request,
            'Please choose a rating from 1 to 5.'
        )

    return redirect('place_detail', pk=pk)

@login_required
def place_create(request):
    if request.method=='POST':
        f=PlaceForm(request.POST,request.FILES)
        if f.is_valid(): p=f.save(commit=False); p.owner=request.user; p.save(); return redirect('place_detail',p.pk)
    else: f=PlaceForm()
    return render(request,'places/form.html',{'form':f,'title':'Add a Spot','eyebrow':'CREATE'})

@login_required
def place_edit(request,pk):
    p=get_object_or_404(Place,pk=pk,owner=request.user)
    if request.method=='POST':
        f=PlaceForm(request.POST,request.FILES,instance=p)
        if f.is_valid(): f.save(); return redirect('place_detail',pk)
    else: f=PlaceForm(instance=p)
    return render(request,'places/form.html',{'form':f,'title':'Edit Spot','eyebrow':'UPDATE'})

@login_required
def place_delete(request,pk):
    p=get_object_or_404(Place,pk=pk,owner=request.user)
    if request.method=='POST': p.delete(); return redirect('explore')
    return render(request,'places/delete.html',{'object':p})

@login_required
def toggle_save(request,pk):
    p=get_object_or_404(Place,pk=pk)
    obj=SavedPlace.objects.filter(user=request.user,place=p)
    obj.delete() if obj.exists() else SavedPlace.objects.create(user=request.user,place=p)
    return redirect('place_detail', pk=pk)

@login_required
def collections(request):
    return render(request,'places/collections.html',{'collections':request.user.collections.annotate(count=Count('items')),'saved':request.user.saved_places.select_related('place')})

@login_required
def collection_create(request):
    if request.method=='POST':
        f=CollectionForm(request.POST)
        if f.is_valid(): c=f.save(commit=False); c.user=request.user; c.save(); return redirect('collections')
    else: f=CollectionForm()
    return render(request,'places/form.html',{'form':f,'title':'New Collection','eyebrow':'COLLECTION'})

@login_required
def collection_detail(request,pk): return render(request,'places/collection_detail.html',{'collection':get_object_or_404(Collection,pk=pk,user=request.user)})

@login_required
def collection_add_place(request, pk, place_id):
    collection = get_object_or_404(
        Collection,
        pk=pk,
        user=request.user
    )

    place = get_object_or_404(
        Place,
        pk=place_id,
        approved=True
    )

    CollectionPlace.objects.get_or_create(
        collection=collection,
        place=place
    )

    messages.success(
        request,
        f"{place.name} added to {collection.name} collection."
    )

    return redirect("collection_detail", pk=collection.pk)

@login_required
def profile(request):
    ensure_profile(request.user)
    prof = request.user.profile

    if request.method == 'POST':
        f = ProfileForm(
            request.POST,
            request.FILES,
            instance=prof
        )
        if f.is_valid():
            f.save()
            return redirect('profile')
    else:
        f = ProfileForm(instance=prof)

    places_count = Place.objects.filter(
        owner=request.user
    ).count()

    reviews_count = Review.objects.filter(
        user=request.user
    ).count()

    saved_count = SavedPlace.objects.filter(
        user=request.user
    ).count()

    context = {
        'form': f,
        'profile': prof,
        'places_count': places_count,
        'reviews_count': reviews_count,
        'saved_count': saved_count,
    }

    return render(request, 'places/profile.html', context)

def share_place(request, pk):
    p=get_object_or_404(Place,pk=pk,approved=True)
    return JsonResponse({'title':p.name,'text':f'Discover {p.name} on Spotly','url':request.build_absolute_uri(p.get_absolute_url()) if hasattr(p,'get_absolute_url') else request.build_absolute_uri(f'/place/{p.pk}/')})

def google_login(request):
    client_id=os.getenv('GOOGLE_CLIENT_ID','')
    if not client_id: messages.error(request,'Google Login is not configured yet. Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env.'); return redirect('login')
    state=secrets.token_urlsafe(32); request.session['google_oauth_state']=state
    params={'client_id':client_id,'redirect_uri':request.build_absolute_uri('/auth/google/callback/'),'response_type':'code','scope':'openid email profile','access_type':'online','state':state,'prompt':'select_account'}
    return redirect('https://accounts.google.com/o/oauth2/v2/auth?'+urlencode(params))

def google_callback(request):
    if request.GET.get('state') != request.session.pop('google_oauth_state',None): messages.error(request,'Google security check failed.'); return redirect('login')
    code=request.GET.get('code'); client_id=os.getenv('GOOGLE_CLIENT_ID',''); client_secret=os.getenv('GOOGLE_CLIENT_SECRET','')
    if not code or not client_id or not client_secret: messages.error(request,'Google Login configuration is incomplete.'); return redirect('login')
    data=urlencode({'code':code,'client_id':client_id,'client_secret':client_secret,'redirect_uri':request.build_absolute_uri('/auth/google/callback/'),'grant_type':'authorization_code'}).encode()
    try:
        token=json.loads(urlopen(Request('https://oauth2.googleapis.com/token',data=data,headers={'Content-Type':'application/x-www-form-urlencoded'}),timeout=10).read())
        info=json.loads(urlopen(Request('https://openidconnect.googleapis.com/v1/userinfo',headers={'Authorization':'Bearer '+token['access_token']}),timeout=10).read())
        email=info.get('email');
        if not email: raise ValueError('Google did not return an email address')
        user=User.objects.filter(email__iexact=email).first()
        if not user:
            base=(info.get('given_name') or email.split('@')[0]).replace(' ','').lower()[:20] or 'spotlyuser'; username=base; n=1
            while User.objects.filter(username=username).exists(): n+=1; username=f'{base}{n}'
            user=User.objects.create_user(username=username,email=email,first_name=info.get('given_name',''),last_name=info.get('family_name',''))
        ensure_profile(user); login(request,user); messages.success(request,'Signed in with Google.'); return redirect('home')
    except Exception as exc:
        messages.error(request,f'Google Login failed: {exc}'); return redirect('login')
