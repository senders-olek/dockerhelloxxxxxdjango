from django.urls import path

from app.views import RCEView

urlpatterns = [
    # User authentication views
    path('rce/', RCEView.as_view(), name='rce'),

]