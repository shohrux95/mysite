from django.urls import path
from .views import homepage, logoutview,products,register,loginview,logoutview,blog,articleview,userpage


urlpatterns = [
    path('',homepage,name='home'),
    path('product/',products,name='product'),
    path('register/',register,name='register'),
    path('login/',loginview,name='login'),
    path('logout/',logoutview,name='logout'),
    path('blog/<tag_page>',blog,name='blog'),
    path('<article_page>',articleview,name='article'),
    path('user/',userpage,name='userpage')
]

