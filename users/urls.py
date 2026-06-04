from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, UserMeView, DoctorAnalyticsView, DoctorListView, GoogleAuthView
from .jwt import CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserMeView.as_view(), name='user_me'),
    path('analytics/', DoctorAnalyticsView.as_view(), name='doctor_analytics'),
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('google/', GoogleAuthView.as_view(), name='google_auth'),
]

