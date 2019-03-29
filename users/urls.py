from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [

    path('user/edit/', views.edit, name='edit'),

    path('user/<int:pk>/', views.viewmember, name='user'),
    path('user/me/', views.viewmember, {'pk': 'me'}, name='me'),

    path('user/update/', views.update, name='update'),

    path('user/allmembers/', views.allmembers, name='allmembers'),

    # TODO: Reimplement auth stuff using Django built-in auth views
    # https://docs.djangoproject.com/en/1.11/topics/auth/default/#built-in-auth-views
    path('login/done/', views.login_process, name='login-done'),
    path('login/', views.login_view, name='login'),

    path('signup/done/', views.signup_process, name='signup-done'),
    path('signup/', views.signup_view, name='signup'),

    path('logout/', views.logout_view, name='logout'),

    # url(r'^', include('django.contrib.auth.urls')),

    # TODO: Create our own so that they're prettier?
    path('change-password/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'),

    path('change-password/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),

    path('reset-password/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'),

    path('reset-password/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),

    path('reset-password/<slug:uidb64>/<slug:token>',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),

    path('reset-password/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
]
