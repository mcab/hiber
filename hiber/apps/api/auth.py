from django.urls import path
from djoser import views
from .views import AuthView

urlpatterns = [
    path('', AuthView.as_view()),
    path('users/me', views.UserView.as_view(), name='user'),
    path('users/create', views.UserCreateView.as_view(), name='user-create'),
    path('users/delete', views.UserDeleteView.as_view(), name='user-delete'),
    path('users/activate',
         views.ActivationView.as_view(),
         name='user-activate'),
    path('users/activate/resend',
         views.ResendActivationView.as_view(),
         name='user-activate-resend'),
    path('password', views.SetPasswordView.as_view(), name='set-password'),
    path('password/reset',
         views.PasswordResetView.as_view(),
         name='reset-password'),
    path('password/reset/confirm',
         views.PasswordResetConfirmView.as_view(),
         name='reset-password-confirm'),
    path('token/create', views.TokenCreateView.as_view(), name='token-create'),
    path('token/destroy',
         views.TokenDestroyView.as_view(),
         name='token-destroy'),
    path('token/login', views.TokenCreateView.as_view(), name='login'),
    path('token/logout', views.TokenDestroyView.as_view(), name='logout'),
]
