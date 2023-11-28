from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', include('problems.urls')),
    path('problems/', include('problems.urls'))
]
