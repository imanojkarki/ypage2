from django.urls import path

# import custom views here.
from ypages.views import (YPages_Index, )
app_name = "app_ypages"
urlpatterns = [
    path('<int:ypage>/<slug:slug>/', YPages_Index.as_view()),
]
