from django.shortcuts import redirect, render 
from django.http import HttpResponse  
from django.urls import reverse

from rango.forms import CategoryForm, PageForm 
from .models import Category, Page 

 
def index(request):   
    category_list = Category.objects.order_by('-likes')[:5] # - denotes descending order 
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {} 
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list 
    context_dict['pages'] = page_list
    return render(request, 'rango/index.html', context=context_dict) 

def about(request):  
    return render(request , 'rango/about.html', {}) 

def show_category(request,category_name_slug):  
    context_dict = {} 
     
    try: 
        category = Category.objects.get(slug = category_name_slug) 
         
        pages = Page.objects.filter(category = category) 
         
        context_dict['pages'] = pages 
         
        context_dict['category'] = category 
         
    except Category.DoesNotExist:  
        context_dict['category'] = None
        context_dict['pages'] = None 

    return render(request, 'rango/category.html' , context_dict) 
    


def add_category(request): 

    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else: 
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

 
  
# GET and POST are HTTP requests, GET to request representation of a specified resource,  while POST to  
# submit data from the client to server 
# Hence POST data can be accessed with GET after saving 
 

  
def add_page(request , category_name_slug): 
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/') 

    form = PageForm() 

    if request.method == 'POST':
        form = PageForm(request.POST) 

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
 
  
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict) 

