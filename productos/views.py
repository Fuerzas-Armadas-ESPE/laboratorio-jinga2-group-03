import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Producto
from .forms import ProductoForm
from django.db.models import Q


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


def exportar_productos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Precio', 'Cantidad'])
    productos = Producto.objects.all()
    for producto in productos:
        writer.writerow([producto.id, producto.nombre, producto.precio, producto.cantidad])
    return response

def importar_productos_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        
        # Verificar que hay al menos dos filas en el archivo CSV
        if len(decoded_file) < 2:
            return HttpResponse("El archivo CSV no contiene suficientes filas para importar.")
        
        reader = csv.reader(decoded_file)
        next(reader)  # Saltar la fila de encabezados
        
        # Lista para almacenar nombres de productos del CSV
        productos_csv = set()
        
        for row in reader:
            if len(row) >= 4:  # Verificar si hay suficientes elementos en la fila
                nombre_producto = row[1]
                productos_csv.add(nombre_producto)
                
                # Buscar el producto por su nombre
                producto, _ = Producto.objects.get_or_create(
                    nombre=nombre_producto,
                    defaults={
                        'precio': row[2],
                        'cantidad': row[3]
                    }
                )
                # Si el producto ya existe, actualizar sus detalles
                if not _:
                    producto.precio = row[2]
                    producto.cantidad = row[3]
                    producto.save()
        
        # Eliminar los productos que no están en el archivo CSV
        productos_a_eliminar = Producto.objects.filter(~Q(nombre__in=productos_csv))
        productos_a_eliminar.delete()
                    
        return redirect('listar_productos')
    return render(request, 'importar_productos.html')