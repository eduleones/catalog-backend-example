from django.urls import path

from shoes import views


urlpatterns = [
    path('', views.ShoesListCreateView.as_view(), name='shoes'),
    path('<int:pk>/', views.ShoesViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='shoes_viewset'),
    path('csv_import/', views.ShoesImport.as_view(), name='shoes_import'),
]
