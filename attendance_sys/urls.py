from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from attendance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('',views.home, name='home'),
    path('', include('attendance.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
