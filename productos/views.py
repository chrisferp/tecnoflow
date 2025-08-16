from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Producto

def lista_productos(request):
    query = request.GET.get('q')
    order = request.GET.get('order', 'name')
    productos_list = Producto.objects.all()
    if query:
        productos_list = productos_list.filter(Q(detalle__icontains=query) | Q(codigo__icontains=query))

    if order == 'price_asc':
        productos_list = productos_list.order_by('precio')
    elif order == 'price_desc':
        productos_list = productos_list.order_by('-precio')
    else:
        productos_list = productos_list.order_by('detalle')

    paginator = Paginator(productos_list, 24)
    page_number = request.GET.get('page', 1)

    try:
        productos = paginator.page(page_number)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    return render(request, 'productos/lista_productos.html', {
        'productos': productos,
        'query': query,
        'order': order
    })

def detalle_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

# ---------------------
# Funciones para carrito
# ---------------------
def agregar_al_carrito(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    carrito = request.session.get('carrito', {})

    if codigo in carrito:
        carrito[codigo]['cantidad'] += 1
    else:
        carrito[codigo] = {
            'detalle': producto.detalle,
            'precio': float(producto.precio),
            'cantidad': 1,
            'imagen': producto.imagen
        }

    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render(request, 'productos/carrito.html', {'carrito': carrito, 'total': total})

def eliminar_del_carrito(request, codigo):
    carrito = request.session.get('carrito', {})
    if codigo in carrito:
        del carrito[codigo]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def actualizar_carrito(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        cantidad = int(request.POST.get("cantidad", 1))
        carrito = request.session.get("carrito", {})

        if codigo in carrito:
            carrito[codigo]['cantidad'] = cantidad
            request.session['carrito'] = carrito
            total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
            subtotal = carrito[codigo]['precio'] * cantidad
            return JsonResponse({"status": "ok", "total": total, "subtotal": subtotal})
        
        return JsonResponse({"status": "error", "message": "Producto no encontrado"})
    
    return JsonResponse({"status": "error", "message": "Petición inválida"})
def checkout(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    if request.method == "POST":
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        crear_usuario = request.POST.get('crear_usuario')
        if crear_usuario and email:
            password = request.POST.get('password') or User.objects.make_random_password()
            user, created = User.objects.get_or_create(
                username=email,
                defaults={'email': email, 'first_name': nombre}
            )
            if created:
                user.set_password(password)
                user.save()
            login(request, user)
            request.session['carrito'] = {}
            return redirect('completar_registro')

        request.session['carrito'] = {}
        return render(request, 'productos/checkout_exito.html', {'total': total})

    return render(request, 'productos/checkout.html', {'carrito': carrito, 'total': total})


@login_required
def completar_registro(request):
    if request.method == 'POST':
        return redirect('lista_productos')
    return render(request, 'productos/completar_registro.html')
