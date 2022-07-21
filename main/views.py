from itertools import product
from django.shortcuts import render,redirect
from .models import Product,Article,Tag,Profile
from django.core.paginator import Paginator
from .forms import NewUserForm,UserForm,ProfileForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# Create your views here.



def products(request):
    if request.method=='POST':
        product_id=request.POST.get('product_pk')
        product=Product.objects.get(id=product_id)
        request.user.profile.product.add(product)
        messages.success(request,(f"{product} Yoqtirganlaringiz ro'yxatiga qo'shildi."))
        return redirect('home')
    products=Product.objects.all()
    paginator=Paginator(products,3)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return  render(request=request,template_name='product.html',context={'page_obj':page_obj})    

def register(request):
    form=NewUserForm()
    if request.method=='POST':
        print(1, '\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
        form=NewUserForm(request.POST)
        if form.is_valid():
            print(2, '\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
            user=form.save()     
            messages.success(request,"registratsiyadan utdingiz")
            return redirect('login')
        messages.error(request,'login yoki parolingiz xato')    
    return render(request=request,template_name='register.html',context={'form':form})    

def loginview(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f'xush kelibsiz {username}')
                return redirect('home')
            else:
                messages.error(request,'login yoki parolingiz xato')
        else:
            password=form.cleaned_data.get('password')
            messages.error(request,'login yoki parollingiz xato')
    form=AuthenticationForm
    return render(request=request,template_name='login.html',context={'form':form})  

def logoutview(request):
    logout(request)
    messages.info(request,'siz tizimdan chiqdingiz')
    return redirect('home')

def blog(request,tag_page):
    if tag_page=='articles':
        tag=''
        blog=Article.objects.all().order_by('-article_published')   

    else:
        tag=Tag.objects.get(tag_slug=tag_page)
        blog=Article.objects.filter(article_tags=tag).order_by('-article_published')     
    paginator=Paginator(blog,3)
    blog_numer=request.GET.get('page')
    blog_obj=paginator.get_page(blog_numer)
    return render(request=request,template_name='blog.html',context={'blog_obj':blog_obj})   


def articleview(request,article_page):
    article=Article.objects.get(article_slug=article_page)
    return render(request=request,template_name='article.html',context={'article':article})


def homepage(request):
    if request.method=='POST':
        product_id=request.POST.get('product_pk')
        product=Product.objects.get(id=product_id)
        request.user.profile.product.add(product)
        messages.success(request,f"{product} Yoqtirganlaringiz ro'yxatiga qo'shildi.")
        return redirect('home')
    products=Product.objects.all()
    article=Article.objects.all().order_by('-article_published')[:3]
    tags=Article.objects.filter(article_tags__tag_name='simli')
    new_article=article.first()
    return render(request=request,template_name='home.html',context={'product':products,'article':article,'tags':tags,'new_article':new_article})

def userpage(request):
    
    if request.method=='POST':
        # product_id=request.POST.get('product_pk')
        # product=Product.objects.get(id=product_id)
        # for s in product.product_price:
        #     summ+=s
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=ProfileForm(request.POST,instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,('profilengiz muvafaqiyatli ozgartirildi'))
        elif profile_form.is_valid:
            profile_form.save()
            messages.success(request,("Yoqtirganlaringiz roʻyxati muvaffaqiyatli yangilandi")) 
        else:
            messages.success(request,("So‘rovni bajarib bo‘lmadi"))  
        return redirect('userpage')     
    user_form=UserForm(instance=request.user)
    profile_form=ProfileForm(instance=request.user.profile)
    return render(request=request,template_name='user.html',context={'user':request.user,'user_form':user_form,'profile_form':profile_form})
 
def price(request):
    product=request.user.profile.product.all()
    summ=0
    for s in product.product_price:
        summ+=s
        print(summ)
    return render(request=request,template_name='user.html',context={'summ':summ})    

    