import datetime
import json

from collections import defaultdict
from decimal import Decimal

from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from main.forms import HoursForm
from main.models import Project, Hours, Company, Client
from main.utils import get_week

SUM_HOURS = """'SELECT project_id, billed, SUM(quantity) FROM hours WHERE date >= %s AND date <= %s AND user_id = %s GROUP BY project_id, billed ORDER BY project_id, ''"""

@login_required
def home(request, year=None, month=None, day=None):
    if all([year, month, day]):
        today = datetime.date(year=year, month=month, day=day)
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

def summary(request, year, month=None):
    if month:
        start_date = datetime.date(year=year, month=month, day=1)
        end_date = start_date + relativedelta(months=+1, days=-1)
    else:
        start_date = datetime.date(year=year, month=1, day=1)
        end_date = datetime.date(year=year, month=12, day=31)

    HOURS_CT = f"""SELECT * FROM 
crosstab('SELECT project_id, billed, SUM(quantity) FROM hours WHERE date >= ''{start_date}'' AND date <= ''{end_date}'' AND user_id = %s GROUP BY project_id, billed ORDER BY 1', 'SELECT DISTINCT billed FROM hours ORDER BY 1') 
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
