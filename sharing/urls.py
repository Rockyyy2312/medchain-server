from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenerateShareTokenView, AccessSharedRecordsView, AccessRequestViewSet, AccessGrantViewSet, GrantedPatientRecordsView

router = DefaultRouter()
router.register(r'requests', AccessRequestViewSet, basename='access-requests')
router.register(r'grants', AccessGrantViewSet, basename='access-grants')

urlpatterns = [
    path('generate/', GenerateShareTokenView.as_view(), name='share_generate'),
    path('<str:token>/', AccessSharedRecordsView.as_view(), name='share_access'),
    path('access/', include(router.urls)),
    path('access/grants/<uuid:patient_id>/records/', GrantedPatientRecordsView.as_view(), name='granted_records'),
]
