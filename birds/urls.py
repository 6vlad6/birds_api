from django.urls import path
from .views import *

urlpatterns = [
    path('', Birds.as_view(), name='birds-list'),
    path('<int:bird_id>/', BirdDetail.as_view(), name='bird-detail'),
    path('<int:bird_id>/seen-total/', BirdSeenTotal.as_view(), name='bird-seen-total'),

    path('bird-seens/', BirdSeens.as_view(), name='bird-seens-list'),
    path('bird-seens/<int:birdseen_id>/', BirdSeenDetail.as_view(), name='bird-seen-detail'),
]