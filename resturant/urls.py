from django.contrib import admin
from django.urls import path, include
from rest import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest.urls')),
    path('', views.home, name='frontend_app'),
    path('logintotahvil/', views.logintotahvil, name='login_page'),
    

]