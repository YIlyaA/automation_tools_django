from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),

    # Dataentry app
    path('dataentry/', include('dataentry.urls')),

    # Test views
    path('celery-test/', views.celery_test),

    # Registration and login
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    # Bulk Emails
    path('emails/', include('emails.urls')),

    # Compress Image
    path('image-compression/', include('image_compression.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
