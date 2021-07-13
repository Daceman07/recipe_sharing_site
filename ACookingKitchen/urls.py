"""ACookingKitchen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from category import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    # AUTH
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    # CATEGORY
    path('category/create', views.CreateCategory.as_view(), name='create_category'),
    path('category/<int:pk>', views.DetailCategory.as_view(), name='detail_category'),
    path('category/<int:pk>/update', views.UpdateCategory.as_view(), name='update_category'),
    path('category/<int:pk>/delete', views.DeleteCategory.as_view(), name='delete_category'),
    # Recipes
    path('category/<int:pk>/addrecipe', views.add_recipe, name='add_recipe'),
    path('recipe/<int:pk>', views.DetailRecipe.as_view(), name='detail_recipe'),
    path('recipe/<int:pk>/update', views.UpdateRecipe.as_view(), name='update_recipe'),
    path('recipe/<int:pk>/delete', views.DeleteRecipe.as_view(), name='delete_recipe')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)