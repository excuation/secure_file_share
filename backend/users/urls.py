from django.urls import path
from .views import DynamicRoleSignupView
from .views import VerifyEmailView,OpsLoginView,ClientLoginView

urlpatterns = [
   path('signup/', DynamicRoleSignupView.as_view(), name='dynamic-signup'),
     path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
     path('ops-login/', OpsLoginView.as_view(), name='ops-login'),
     path('client-login/', ClientLoginView.as_view(), name='client-login'),
]
