"""building_construction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('building/', include('profile_utility.urls')),
    path('auth/', include('djoser.urls')),  # Keep one set of authentication URLs
    path('auth/jwt/', include('djoser.urls.jwt')),  # Use a different path for JWT authentication
    path('kovais/', include('Kovais.urls')),
    path('thiran_attendance/', include('Attendance.urls')),
    path('app/', include('app.urls')),
    # path('ecomapp/', include('ecomapp.urls'))   
 # path('Trust/',include('Trust.urls')),
]
# ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
