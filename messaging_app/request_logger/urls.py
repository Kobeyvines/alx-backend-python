from django.urls import path
from .views import test_logging

urlpatterns = [
    path('test-logging/', test_logging, name='test-logging'),
]
