from django.urls import include, path

import main.views as views

app_name = "main"

urlpatterns = [
    path("<int:year>/", views.summary, name="summary_year"),
    path("<int:year>/<int:month>/", views.summary, name="summary_month"),
    path("<int:year>/<int:month>/<int:day>/", views.home, name="weekof"),
    path("hours/create/", views.CreateHours.as_view(), name="hours_create"),
    path("",  views.home, name="home"),
]
