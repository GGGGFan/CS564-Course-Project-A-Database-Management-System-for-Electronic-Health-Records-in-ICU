"""eicu_v0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import re_path
from query import query_views
from insert import insert_views
from home import home_views
from stats import stats_views
from users import views
from delete import delete_views
from django.conf.urls import url, include

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^$', home_views.home, name='home'),
    re_path(r'^query/', query_views.query, name='query'),
    re_path(r'^query_result/', query_views.pt_result, name='pt_result'),
    re_path(r'^stayinfo/', query_views.stayinfo, name='stayinfo'),
    re_path(r'^insert/', insert_views.insert, name='insert'),
    re_path(r'^new_patient/', insert_views.new_patient, name='new_patient'),
    re_path(r'^new_stay/', insert_views.new_stay, name='new_stay'),
    re_path(r'^new_data/', insert_views.new_data, name='new_data'),
    re_path(r'^new_modified_data/', insert_views.modify_data, name='modify_data'),
    re_path(r'^new_modified_data_select/', insert_views.modify_data_select, name='modify_data_select'),
    re_path(r'^new_modified_data_modified/', insert_views.modify_data_modified, name='modify_data_modified'),
    re_path(r'^data_added/', insert_views.data_added, name='data_added'),
    re_path(r'^delete/', delete_views.delete, name='delete'),
    re_path(r'^delete_pt/', delete_views.delete_pt, name='delete_pt'),
    re_path(r'^delete_stay/', delete_views.delete_stay, name='delete_stay'),
    re_path(r'^delete_success/', delete_views.delete_success, name='delete_success'),
    re_path(r'^icd_demograph/', stats_views.icd_demograph, name='icd_demograph'),
    re_path(r'^patients_disease/', stats_views.patients_disease, name='patients_disease'),
    url(r'^users/', include('users.urls')),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
]
