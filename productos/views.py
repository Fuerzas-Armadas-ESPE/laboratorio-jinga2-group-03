from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm

productos = []

def listar_productos(request):
    # Consulta a la base de datos
    # Renderiza la plantilla listar.html
    
    productos = Producto.objects.all()
    return render(request, 'listar.html', {'productos': productos})


# Vista para crear producto
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'formulario.html', {'form': form})

# Vista para editar producto
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

# Vista para eliminar producto
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        # Si se confirma la eliminación, eliminar el producto
        if 'confirmar' in request.POST:
            producto.delete()
            return redirect('listar_productos')
        # Si se cancela la eliminación, redirigir de vuelta a la lista de productos
        elif 'cancelar' in request.POST:
            return redirect('listar_productos')
    return render(request, 'eliminar.html', {'producto': producto})