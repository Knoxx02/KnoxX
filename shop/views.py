from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, Brand
from django.core.paginator import Paginator


def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:8]
    new_products = Product.objects.filter(is_new=True)[:4]
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    products = Product.objects.all()
    
    # Filtering
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    if category:
        products = products.filter(category__slug=category)
    
    if brand:
        products = products.filter(brand__name=brand)
    
    if price_min:
        products = products.filter(price__gte=price_min)
    
    if price_max:
        products = products.filter(price__lte=price_max)
    
    # Sorting
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj.object_list,  # ใช้เฉพาะรายการในหน้านั้น
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    specs_lines = product.specs.splitlines()
    specs = []
    if product.specs:
        for line in product.specs.splitlines():
            parts = line.split(':')
            if len(parts) >= 2:
                specs.append((parts[0].strip(), parts[1].strip()))
    context = {
        'product': product,
        'specs': specs,
    }
    return render(request, 'shop/product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'shop/category_detail.html', context)


def search(request):
    query = request.GET.get('q')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    context = { 
        'products': products,
        'query': query,
    }
    return render(request, 'shop/search_results.html', context)


def compare(request):
    product_ids = request.GET.getlist('product_id')
    products = Product.objects.filter(id__in=product_ids)
    
    context = {
        'products': products,
    }
    return render(request, 'shop/compare.html', context)
