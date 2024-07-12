from django.urls import path

from.import views
from .views import search

urlpatterns=[

    path('',views.toLogin_view),
    path('index/',views.Login_view),
    path('toregister/',views.toregister_view),
    path('register/',views.register_view),
    path('home/', views.home_view),
    path('search/', views.search, name='search'),
    path('upload/', views.upload_food_view, name='upload_food'),
]