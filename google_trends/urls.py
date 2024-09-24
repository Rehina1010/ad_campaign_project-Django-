from django.urls import path
from .views import trends_view, PrivacyPolicyView, CookiePolicyView, TermsView

app_name = 'google_trends'

urlpatterns = [
    path('trends/', trends_view, name='trends'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('cookie-policy/', CookiePolicyView.as_view(), name='cookie_policy'),
    path('terms/', TermsView.as_view(), name='terms'),
]
