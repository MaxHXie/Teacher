from django.urls import path

from . import views
app_name = 'english'
urlpatterns = [
    path('', views.index, name='index'),
    path('payment', views.payment, name='payment'),
    path('payment_success', views.payment_success, name='payment_success')
]
