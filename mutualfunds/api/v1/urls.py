from django.urls import path

from mutualfunds.api.v1.views import MutualFundsApiView

app_name = "mutual_funds"


urlpatterns = [
    path("mutual-funds/",MutualFundsApiView.as_view(),name="mutual-funds")
]
