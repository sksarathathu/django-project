from django.urls import path
from customer import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
   
    path("register",views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("home",views.HomeIndexView.as_view(),name="home"),
    path("profile",views.ProfileView.as_view(),name="profile"),
    path("editprofile",views.EditProfileView.as_view(),name="editprofile"),
    path("logout",views.SignOutView,name="signout"),
    path("addproducts/<int:id>",views.ProductView.as_view(),name="addproduct"),
    path("addcategory",views.AddCategoryView.as_view(),name="addcat"),
    path("listcategory",views.ListCategoryView.as_view(),name="catlist"),
    path("productadded",views.ProductAddedView.as_view(),name="addedproduct"),
    path("productdetail/<int:id>",views.ProductDetailView.as_view(),name="productdetail"),
    path("mobiles",views.MobileView.as_view(),name="mobiles"),
    path("cars",views.CarView.as_view(),name="cars"),
    path("checkout/<int:id>",views.OrderView.as_view(),name="checkout"),
    path("deleteproduct/<int:id>",views.ProductDeleteView.as_view(),name="deleteprod"),
    path("addproductimage/<int:id>",views.ProductImageView.as_view(),name="productimage")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)