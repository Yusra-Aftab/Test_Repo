

from accounts import views
from django.urls import include, path, re_path
from django.views.generic import TemplateView

urlpatterns = [

    path('upload/', views.upload_file, name='upload_file'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]


urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]