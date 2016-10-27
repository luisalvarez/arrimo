
from django.conf.urls import url
from reports.views import reports, generate, download

urlpatterns = [
    url(r'^generate/', generate, name='generate'),
    url(r'^reports/', reports, name='reportes'),
    url(r'^download/', download, name='download'),
]
