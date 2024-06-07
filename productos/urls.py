from django.urls import path
from . import views

urlpatterns = [
    # URLs de vistas normales
    # Crear la URL de la vista index
    path('', views.listar_productos, name='listar_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('<int:pk>/editar', views.editar_producto, name='editar_producto'),
    path('<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('exportar/csv/', views.exportar_productos_csv, name='exportar_productos_csv'),
    path('importar/csv/', views.importar_productos_csv, name='importar_productos_csv'),
]