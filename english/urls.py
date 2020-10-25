from django.urls import path

from . import views
app_name = 'english'
urlpatterns = [
    path('', views.index, name='index'),
    path('correction', views.correction, name='correction'),
    path('payment_success_backend', views.payment_success_backend, name='payment_success_backend'),
    path('payment_result', views.payment_result, name='payment_result'),
    path('terms_of_service', views.terms_of_service, name='terms_of_service'),
]
