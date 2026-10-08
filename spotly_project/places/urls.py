from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns=[
 path('',views.home,name='home'), path('explore/',views.explore,name='explore'), path('place/<int:pk>/',views.place_detail,name='place_detail'),
 path('register/',views.register,name='register'), path('login/',auth_views.LoginView.as_view(template_name='places/login.html'),name='login'),
 path('logout/',auth_views.LogoutView.as_view(next_page='home'),name='logout'), path('password-reset/',auth_views.PasswordResetView.as_view(template_name='places/password_reset.html',email_template_name='places/password_reset_email.txt',success_url='/password-reset/done/'),name='password_reset'),
 path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='places/password_reset_done.html'),name='password_reset_done'),
 path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='places/password_reset_confirm.html',success_url='/reset/done/'),name='password_reset_confirm'),
 path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='places/password_reset_complete.html'),name='password_reset_complete'),
 path('auth/google/',views.google_login,name='google_login'), path('auth/google/callback/',views.google_callback,name='google_callback'),
 path('place/<int:pk>/review/',views.review_place,name='review_place'), path('place/<int:pk>/share/',views.share_place,name='share_place'),
 path('place/add/',views.place_create,name='place_create'), path('place/<int:pk>/edit/',views.place_edit,name='place_edit'), path('place/<int:pk>/delete/',views.place_delete,name='place_delete'), path('place/<int:pk>/save/',views.toggle_save,name='toggle_save'),
 path('collections/',views.collections,name='collections'), path('collections/add/',views.collection_create,name='collection_create'), path('collections/<int:pk>/',views.collection_detail,name='collection_detail'), path('collections/<int:pk>/add/<int:place_id>/',views.collection_add_place,name='collection_add_place'), path('profile/',views.profile,name='profile')]
