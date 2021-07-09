from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('upload', views.upload_beat, name='upload'),
    path('delete/<int:beat_id>', views.delete, name='delete'),
    path('user/<int:user_id>', views.profile, name='user'),
    path('edit/<int:beat_id>', views.edit, name='edit'),
    path('edit_user/<int:user_id>', views.edit_user, name='edit_user'),
    path('edit_password/<int:user_id>', views.edit_password, name='edit_password'),
    path('details/<int:beat_id>', views.view_details, name='details'),
    path('like/<int:beat_id>', views.like, name='like'),
    path('unlike/<int:beat_id>', views.unlike, name='unlike'),
    path('hip_hop', views.hip_hop, name='hip_hop'),
    path('rhythm_and_blues', views.ryb, name='R&B'),
    path('samples', views.sample, name='samples'),

]