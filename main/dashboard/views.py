from django.shortcuts import render, redirect
from main.models import Cart, Product
from main import models
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from main.models import User
from main.models import Product, Cart

def user_create(request):
    if request.method == 'POST':
        return redirect('dashboard:user_list')  
    else:
        return render(request, 'user_create.html')

def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'user_detail.html', {'user': user})

def user_update(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        return redirect('dashboard:user_list')
    else:
        return render(request, 'user_update.html', {'user': user})

def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        return redirect('dashboard:user_list')  
    else:
        return render(request, 'user_delete.html', {'user': user})



def index(request):
    context = {}
    return render(request, 'dashboard/index.html', context)

# ---------CATEGORY-------------


def category_list(request):
    queryset = models.Category.objects.all()
    context = {
        'queryset':queryset
        }
    return render(request, 'dashboard/category/list.html', context)


def category_create(request):
    if request.method == 'POST':
        models.Category.objects.create(
            name = request.POST['name']
        )
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/category/create.html')


def category_update(request, code):
    queryset = models.Category.objects.get(code=code)
    queryset.name = request.POST['name']
    queryset.save()
    return redirect('dashboard:category_list')


def category_delete(request, code):
    queryset = models.Category.objects.get(id=id)
    queryset.delete()
    return redirect('dashboard:category_list')

# ---------PRODUCT----------------

def product_list(request):
    categorys = models.Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id and category_id != '0' :
        queryset = models.Product.objects.filter(category__id=category_id)
    else:
        queryset = models.Product.objects.all()
    context = {
        'queryset':queryset,
        'categorys':categorys
    }
    return render(request, 'dashboard/product/list.html', context)


def product_detail(request, id):
    queryset = models.Product.objects.get(id=id)
    images = models.ProductImg.objects.filter(product=queryset)
    reviews = models.Review.objects.filter(product=queryset)
    ratings = range(5,0,-1)
    videos = models.ProductVideo.objects.filter(product=queryset)
    context = {
          'queryset':queryset,
          'images':images,
          'reviews':reviews,
          'ratings':ratings,
          'videos':videos
    }
    return render(request, 'dashboard/product/detail.html', context)
    

def product_create(request):
    categorys = models.Category.objects.all()
    context = {'categorys':categorys}
    if request.method == 'POST':
        delivery = True if request.POST.get('delivery') else False
        product = models.Product.objects.create(
            category_id = request.POST.get('category_id'),
            name = request.POST.get('name'),
            body = request.POST.get('body'),
            price = request.POST.get('price'),
            banner_img = request.FILES.get('banner_img'),
            quantity = request.POST.get('quantity'),
            delivery = delivery
        )
    if request.FILES.getlist('product_img'):
        for img in request.FILES.getlist('product_img'):
            models.ProductImg.objects.create(
                product = product,
                img = img
        )
    if request.FILES.getlist('product_video'):
        for video in request.FILES.getlist('product_video'):
            models.ProductVideo.objects.create(
                product = product,
                video = video
        )
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/create.html', context)


def product_update(request, id):

    images = models.ProductImg.objects.filter(product_id=id)
    videos = models.ProductVideo.objects.filter(product_id=id)
    categories = models.Category.objects.all()
    product = models.Product.objects.get(id=id)

    if request.method == 'POST':
        if request.FILES.get('banner_img'):
            product.banner_img = request.FILES.get('banner_img')
        delivery = True if request.POST.get('delivery') else False
        product.category_id = request.POST.get('category_id')
        product.name = request.POST.get('name')
        product.body = request.POST.get('body')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.delivery = delivery
        product.save()
    
    if request.FILES.getlist('product_img'):
        for img in request.FILES.getlist('product_img'):
            models.ProductImg.objects.create(
                product = product,
                img = img
        )
    if request.FILES.getlist('product_video'):
        for video in request.FILES.getlist('product_video'):
            models.ProductVideo.objects.create(
                product = product,
                video = video
        )
        return redirect('dashboard:product_update',product.id)
    
    context = {
          'images':images,
          'videos':videos,
          'categories':categories,
          'product':product

    }
    return render(request,'dashboard/product/update.html',context=context)

def product_delete(request, id):
    product = models.Product.objects.get(id=id)
    product.delete()
    return redirect('dashboard:product_list')

def product_img_delete(request, id):
    product_img = models.ProductImg.objects.get(id=id)
    product_img.delete()
    return redirect('dashboard:product_update',product_img.product_id)

def product_video_delete(request, id):
    product_video = models.ProductVideo.objects.get(id=id)
    product_video.delete()
    return redirect('dashboard:product_update',product_video.product_id)

def cart_detail(request, code):
    try:
        cart = Cart.objects.get(code=code)
    except Cart.DoesNotExist:
        raise Http404("Cart does not exist")
    return render(request, 'cart_detail.html', {'cart': cart})