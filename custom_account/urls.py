from django.urls import path

from custom_account.views import (
    SocialLoginView,
    LoginView,
    LogoutView,
    SignUpValidationView,
    SignUpEmailTokenSendView,
    SignUpEmailTokenValidationEndView,
)

app_name = 'custom_account'


urlpatterns = [
    path('login/', LoginView.as_view(), name='normal_login'),
    path('logout/', LogoutView.as_view(), name='normal_logout'),
    path('social-login/', SocialLoginView.as_view(), name='social_login'),
    path('sign-up-validation/', SignUpValidationView.as_view(), name='sign_up_validation'),
    path('sign-up-check/', SignUpEmailTokenSendView.as_view(), name='sign_up_check'),
    path('sign-up-validate-token/', SignUpEmailTokenValidationEndView.as_view(), name='sign_up_one_time_token'),
]
