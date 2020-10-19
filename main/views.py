import datetime
import json

from collections import defaultdict
from decimal import Decimal

from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.db import connection
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from main.forms import HoursForm
from main.models import Project, Hours, Company, Client
from main.utils import get_week

@login_required
def home(request, year=None, month=None, day=None):
    if all([year, month, day]):
        try:
            today = datetime.date(year=year, month=month, day=day)
        except ValueError:
            raise Http404("Invalid date")
    else:
        today = datetime.date.today()
    
    week = get_week(today)
    weekhours = Hours.objects.filter(user=request.user,
                                     date__gte=week[0],
                                     date__lte=week[6])
    hours_dict = defaultdict(lambda: [Decimal(0)]*7)

    for hour in weekhours:
        hours_dict[hour.project][hour.date.weekday()] += hour.quantity

    hours_form = HoursForm(initial={"user": request.user,
                                    "date": today})
    prev_week = today - datetime.timedelta(days=7)
    next_week = today + datetime.timedelta(days=7)
    return render(request,
                  "main/home.html",
                  context={"week": week,
                           "hours_dict": dict(hours_dict),
                           "hours_form": hours_form,
                           "prev_week": prev_week,
                           "next_week": next_week})

@login_required
def summary(request, year, month=None):
    if month:
        start_date = datetime.date(year=year, month=month, day=1)
        end_date = start_date + relativedelta(months=+1, days=-1)
    else:
        start_date = datetime.date(year=year, month=1, day=1)
        end_date = datetime.date(year=year, month=12, day=31)

    HOURS_CT = f"""SELECT * FROM 
crosstab('SELECT project_id, billed, SUM(quantity) FROM hours WHERE date >= ''{start_date}'' AND date <= ''{end_date}'' AND user_id = %s GROUP BY project_id, billed ORDER BY 1', 'VALUES (FALSE), (TRUE)') 
AS ct ("Project" varchar, "Unbilled" numeric, "Billed" numeric);"""        

    with connection.cursor() as cursor:
        cursor.execute(HOURS_CT, [request.user.id])
        rows = cursor.fetchall()
        
    return render(request,
                  "main/summary.html",
                  context={"rows": rows,
                           "start_date": start_date,
                           "end_date": end_date})


class CreateHours(LoginRequiredMixin, CreateView):
    model = Hours
    form_class = HoursForm

    def get_success_url(self):
        return reverse("main:weekof",
                       kwargs={"year": self.object.date.year,
                               "month": self.object.date.month,
                               "day": self.object.date.day})


    
class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sd = datetime.date(year=datetime.date.today().year,
                           month=1,
                           day=1)
        ed = datetime.date(year=datetime.date.today().year,
                           month=12,
                           day=31)
        hours = Hours.objects.filter(project=self.object,
                                     date__gte=sd,
                                     date__lte=ed).order_by("date")
        months = [f"{datetime.date(year=2020,month=i,day=1):%B}"
                  for i in range(1, 13)]
        hours_table = {}
        for m in months:
            hours_table[m] = [Decimal(0), Decimal(0)]
        for h in hours:
            hours_table[f"{h.date:%B}"][h.billed] += h.quantity
        context["hours_table"] = hours_table
        return context
