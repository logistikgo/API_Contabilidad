from django.conf.urls import url
from ApiViajes import views

urlpatterns = [
    url(r'api/$', views.PendientesEnviarList.as_view()),
    url(r'^api/(?P<pk>[A-Za-z0-9]+)/$', views.PendientesEnviarUpdate.as_view()),

]