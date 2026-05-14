"""cyber_attack_prediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import re_path as url
from django.contrib import admin
from Remote_User import views as remoteuser
from cyber_attack_prediction import settings
from Service_Provider import views as serviceprovider
from django.conf.urls.static import static


urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', remoteuser.index, name="index"),
    url(r'^login/$', remoteuser.login, name="login"),
    url(r'^remote_login/$', remoteuser.login, name="remote_login"),
    url(r'^provider_home/$', remoteuser.provider_home, name="provider_home"),
    url(r'^logout/$', remoteuser.logout, name="logout"),
    url(r'^Register1/$', remoteuser.Register1, name="Register1"),
    url(r'^Prediction_Of_Cyber_Attack_Type/$', remoteuser.Prediction_Of_Cyber_Attack_Type, name="Prediction_Of_Cyber_Attack_Type"),
    url(r'^ViewYourProfile/$', remoteuser.ViewYourProfile, name="ViewYourProfile"),
    url(r'^serviceproviderlogin/$',serviceprovider.serviceproviderlogin, name="serviceproviderlogin"),
    url(r'^provider_login/$',serviceprovider.serviceproviderlogin, name="provider_login"),
    url(r'^serviceproviderregister/$',serviceprovider.serviceproviderregister, name="serviceproviderregister"),
    url(r'^provider_register/$',serviceprovider.serviceproviderregister, name="provider_register"),
    url(r'^View_Remote_Users/$',serviceprovider.View_Remote_Users,name="View_Remote_Users"),
    url(r'^charts/(?P<chart_type>\w+)/$', serviceprovider.charts,name="charts"),
    url(r'^charts1/(?P<chart_type>\w+)/$', serviceprovider.charts1, name="charts1"),
    url(r'^likeschart/(?P<like_chart>\w+)/$', serviceprovider.likeschart, name="likeschart"),
    url(r'^Find_Prediction_Of_Cyber_Attack_Type_Ratio/$', serviceprovider.Find_Prediction_Of_Cyber_Attack_Type_Ratio, name="Find_Prediction_Of_Cyber_Attack_Type_Ratio"),
    url(r'^train_model/$', serviceprovider.train_model, name="train_model"),
    url(r'^View_Prediction_Of_Cyber_Attack_Type_Details/$', serviceprovider.View_Prediction_Of_Cyber_Attack_Type_Details, name="View_Prediction_Of_Cyber_Attack_Type_Details"),
    url(r'^Download_Predicted_DataSets/$', serviceprovider.Download_Predicted_DataSets, name="Download_Predicted_DataSets"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
