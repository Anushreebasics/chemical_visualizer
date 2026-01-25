"""
URL configuration for chemical equipment visualizer project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from equipment.views import (
    EquipmentViewSet, UploadCSVView, DataSummaryView, 
    HistoryListView, GeneratePDFView, UserRegisterView, 
    UserLoginView, UserLogoutView
)

router = routers.DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename='equipment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/', UserRegisterView.as_view(), name='register'),
    path('api/auth/login/', UserLoginView.as_view(), name='login'),
    path('api/auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('api/upload-csv/', UploadCSVView.as_view(), name='upload-csv'),
    path('api/summary/', DataSummaryView.as_view(), name='summary'),
    path('api/history/', HistoryListView.as_view(), name='history'),
    path('api/generate-pdf/', GeneratePDFView.as_view(), name='generate-pdf'),
]
