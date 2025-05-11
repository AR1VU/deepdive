from django.urls import path
from video_generator import views
from .views import signup_view, CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.input_form, name='input_form'),
    path('generate/', views.generate_video, name='generate_video'),
    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('account/', views.account_view, name='account'),
    path('buy-credits/', views.buy_credits, name='buy_credits'),
    path('buy-credits/success/', views.buy_credits_success, name='buy_credits_success'),
    path('buy-credits/cancel/', views.buy_credits_cancel, name='buy_credits_cancel'),
    path('buy-credits/failure/', views.buy_credits_failure, name='buy_credits_failure'),
]