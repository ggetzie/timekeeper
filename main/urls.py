from django.urls import include, path, re_path, register_converter

import main.views as views
import main.converters as converters

app_name = "main"

register_converter(converters.YearConverter, "yyyy")
register_converter(converters.MonthConverter, "mm")
register_converter(converters.DayConverter, "dd")

urlpatterns = [
    path("<int:year>/",
         views.summary,
         name="summary_year"),
    
    path("<yyyy:year>/<mm:month>/",
         views.summary,
         name="summary_month"),
    
    path("<yyyy:year>/<mm:month>/<dd:day>/",
         views.home,
         name="weekof"),
    path("hours/create/",
         views.CreateHours.as_view(),
         name="hours_create"),
    
    re_path(r'project/(?P<pk>J[0-9]{4}_[0-9]{4})/',
         views.ProjectDetail.as_view(),
         name="project_detail"),
    
    path("",  views.home, name="home"),
]
