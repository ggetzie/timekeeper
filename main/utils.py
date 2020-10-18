import csv
import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model

User = get_user_model()


from main.models import Project, Client, Company, Hours

def load_hours(inpath):
    with open(inpath) as infile:
        rows = [row for row in csv.DictReader(infile)]
    user = User.objects.get(username="gabe")
    for row in rows:
        company, _ = Company.objects.get_or_create(name=row["Company"])
        client, _ = Client.objects.get_or_create(name=row["Client"],
                                               company=company)
        project, _ = Project.objects.get_or_create(title=row["Project"],
                                                 number=row["Project Number"],
                                                 client=client)
        hours = Hours(quantity=Decimal(row["Hours"]),
                      notes=row["Description"],
                      date=datetime.date(year=int(row["Year"]),
                                         month=int(row["Month"]),
                                         day=int(row["Day"])),
                      project=project,
                      user=user)
        hours.save()                                         
        
        
def get_week(today):
    monday = today - datetime.timedelta(days=today.weekday())
    return [monday + datetime.timedelta(days=i) for
            i in range(7)]
