from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView,DetailView,ListView,View
from django.urls import reverse_lazy
from customer.forms import RegistrationForm,LoginForm,EditProfileForm,ProductForm,ProductImageForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from customer.models import Userprofile,Categories
from customer.models import Categories,Products,Productimages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]



class SignUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"account created successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"account creation failed ")
        return super().form_invalid(form)



class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                messages.error(request,"Invalid credentials")
                return render(request,"login.html",{"form":form})


@method_decorator(decs,name="dispatch")
class HomeIndexView(ListView):
    template_name="home.html"
    model=Productimages
    context_object_name="product"
    
    def get_queryset(self):
        return Products.objects.all().exclude(owner=self.request.user)
     

   


@method_decorator(decs,name="dispatch")
class ProfileView(TemplateView):
    template_name="profile.html"
    # def get(self,request,*args,**kwargs):
    #     usr=request.user
    #     up=Userprofile.objects.get(user=usr)
    #     return render(request,"profile.html",{"prof":up})


@method_decorator(decs,name="dispatch")
class ProductAddedView(ListView):
    template_name="myproducts.html"
    model=Products
    context_object_name="product"

    def get_queryset(self):
        return Products.objects.filter(owner=self.request.user)

class ProductDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Products.objects.get(id=id).delete()
        return redirect('addedproduct')

@method_decorator(decs,name="dispatch")
class MobileView(ListView):
    template_name="home.html"
    model=Products
    context_object_name="product"

    def get_queryset(self):
        return Products.objects.filter(category="1").exclude(owner=self.request.user)


@method_decorator(decs,name="dispatch")
class CarView(ListView):
    template_name="home.html"
    model=Products
    context_object_name="product"

    def get_queryset(self):
        return Products.objects.filter(category="2").exclude(owner=self.request.user)


@method_decorator(decs,name="dispatch")
class EditProfileView(FormView):
    template_name="editprofile.html"
    form_class=EditProfileForm

    def post(self,request,*args,**kwargs) :
        user=request.user
        bio=request.POST.get("bio")
        pic=request.POST.get("pic")
        Userprofile.objects.create(user=user,bio=bio,pic=pic)
        messages.success(request,"Profile updated!!")
        return redirect("profile")

class ProductImageView(FormView):
    template_name="productimage.html"
    form_class=ProductImageForm
    def post(self,request,*args,**kwargs):
        id=kwargs.get("id")
        product=Products.objects.get(id=id)
        image=request.POST.get("image")
        Productimages.objects.create(product=product,image=image)
        messages.success(request,"product image added")
        return redirect("addedproduct")


    

@method_decorator(decs,name="dispatch")
class AddCategoryView(TemplateView):
    template_name="addcategory.html"
    def post(self,request,*args,**kwargs):
        cat=request.POST.get("name")
        Categories.objects.create(name=cat)
        messages.success(request,"category added!!")
        return redirect("addcat")


@method_decorator(decs,name="dispatch")
class ListCategoryView(ListView):
    template_name="catlist.html"
    context_object_name="cat"
    model=Categories


@method_decorator(decs,name="dispatch")
class ProductView(FormView):
    template_name="addproducts.html"
    form_class=ProductForm
    
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("id")
        name=request.POST.get("name")
        owner=request.user
        des=request.POST.get("description")
        con=request.POST.get("condition")
        cat=Categories.objects.get(id=id)
        loc=request.POST.get("location")
        price=request.POST.get("price")
        Products.objects.create(name=name,owner=owner,description=des,condition=con,category=cat,location=loc,price=price)
        messages.success(request,"Product added successfully!")
        return redirect("catlist")


@method_decorator(decs,name="dispatch")
class ProductDetailView(DetailView):
    template_name="productdetail.html"
    context_object_name="product"
    pk_url_kwarg="id"
    model=Products


@method_decorator(decs,name="dispatch")
class OrderView(TemplateView):
    template_name="checkout.html"
    def get(self,request,*args,**kwargs):
        pid=kwargs.get('id')
        qs=Products.objects.get(id=pid)
        return render(request,"checkout.html",{"product":qs})


# @method_decorator(decs,name="dispatch")
def SignOutView(request,*args,**kwargs):
    logout(request)
    return redirect('signin')
