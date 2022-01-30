import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')  # setting the enviroment variable of project's settings.py
 
import django 
django.setup()   # importing django settings for the project
from rango.models import Category,Page # will only work if we imported the project settings
 
def populate(): 
    python_pages = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/','views':10},
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/','views':12},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/','views':11} ]

    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/','views':15},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/','views':17},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/','views':160} ]

    other_pages = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/','views':170},
        {'title':'Flask',
        'url':'http://flask.pocoo.org','views':180} ]

    cats = {'Python': {'pages': python_pages,'views':128,'likes':64},
        'Django': {'pages': django_pages,'views':64,'likes':32},
        'Other Frameworks': {'pages': other_pages,'views':32,'likes':16} }  
           

        
    for cat, cat_data in cats.items():     # adds a category + pages to each category using functions defined below
        c = add_cat(cat,cat_data['views'],cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'] , p['views'])


    for c in Category.objects.all():      # prints all the pages within each category
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}') 

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title , views = views )[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name,views = views,likes = likes)[0]
    c.save()
    return c 
         
if __name__ == '__main__':    #execution starts here - will only run when the module is standalone, so importing will not run this code
    print('Starting Rango population script...')  
    populate()
 
