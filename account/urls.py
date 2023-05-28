from django.urls import path

from account.views import (
    SocialLoginView,
    normal_login, SignUpValidationView, SignUpEmailTokenSendView, SignUpEmailTokenValidationEndView,
)

app_name = 'account'


urlpatterns = [
    path('login/', normal_login, name='normal_login'),
    path('social-login/', SocialLoginView.as_view(), name='social_login'),
    path('sign-up-validation/', SignUpValidationView.as_view(), name='sign_up_validation'),
    path('sign-up-check/', SignUpEmailTokenSendView.as_view(), name='sign_up_check'),
    path('sign-up-validate-token', SignUpEmailTokenValidationEndView.as_view(), name='sign_up_one_time_token'),
]
