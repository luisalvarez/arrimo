from django.conf.urls import url
from control_de_vapores.views import reg_vapor_arr, reg_vapor_arr_save, get_name, graph, search


urlpatterns = [
    url(r'^reg-vap-arr/', reg_vapor_arr, name='reg_vap_arr'),
    url(r'^reg-vap-arr-save/', reg_vapor_arr_save, name='reg_vapor_arr_save'),
    url(r'^get-name/', get_name, name='get_name'),
    url(r'^graph/', graph, name='graph'),
    url(r'^search/', search, name='search'),
]
