from django.urls import path

from . import views
app_name = 'english'
urlpatterns = [
    path('', views.index, name='index'),
    path('correction', views.correction, name='correction'),
    path('payment_success_backend', views.payment_success_backend, name='payment_success_backend'),
    path('payment_result', views.payment_result, name='payment_result'),
    path('terms_of_service', views.terms_of_service, name='terms_of_service'),
    path('profile', views.profile, name='profile'),
    path('market', views.market, name='market'),
    path('post_answer', views.post_answer, name='post_answer'),
    path('winner', views.winner, name='winner'),
    path('get_coins', views.get_coins, name='get_coins'),
    path('read_notifications', views.read_notifications, name='read_notifications'),
]
