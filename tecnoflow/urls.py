from django.contrib import admin
from django.urls import path
from productos.views import lista_productos, detalle_producto, agregar_al_carrito, ver_carrito, eliminar_del_carrito, actualizar_carrito
from productos.views import checkout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/<str:codigo>/', detalle_producto, name='detalle_producto'),
    path('agregar_carrito/<str:codigo>/', agregar_al_carrito, name='agregar_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/eliminar/<str:codigo>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/actualizar/', actualizar_carrito, name='actualizar_carrito'),
    path('checkout/', checkout, name='checkout'),
]

