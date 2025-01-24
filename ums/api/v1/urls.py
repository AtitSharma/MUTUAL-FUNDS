from django.urls import path
from ums.api.v1.views import GetNewAccessTokenSerializer, InvestmentApiView, ReportGenerationListApiView, UserRegisterApiView,UserLoginApiView

app_name = "ums"


urlpatterns = [
    path("register/",UserRegisterApiView.as_view(),name="register"),
    path("login/",UserLoginApiView.as_view(),name="login"),
    path("token/refresh/",GetNewAccessTokenSerializer.as_view(),name="refresh"),
    path("investments/",InvestmentApiView.as_view(),name="investments"),
    path("report/",ReportGenerationListApiView.as_view(),name="report")
]



