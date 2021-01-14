import datetime

from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

def next_pnum():
    """
    Determine the next project number to use.
    Project numbers are in the format "JYYYY_####"
    Where YYYY is the current year and 
    #### is a sequential index of projects in that year
    """
    current_year = datetime.date.today().year
    maxnum = Project.objects.aggregate(models.Max("number"))["number__max"]
    if not maxnum:
        return f"J{current_year}_0001"
    max_year, index = maxnum.split("_")
    max_year = int(max_year[1:])
    
    if current_year == max_year:
        index = int(index)+1
    else:
        # we've moved to a new year, start index over at 1
        index = 1
    return f"J{current_year}_{index:04}"

class Project(models.Model):
    number = models.CharField("Project Number",
                              max_length=12,
                              primary_key=True,
                              default=next_pnum)
    title = models.CharField("Title",
                             max_length=150)
    client = models.ForeignKey("Client",
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)
    start_date = models.DateField("Start Date",
                                  blank=True,
                                  null=True)
    end_date = models.DateField("End Date",
                                blank=True,
                                null=True)
    status = models.CharField("Status",
                              max_length=1,
                              choices=(("P", "Proposal"),
                                       ("L", "Lost"),
                                       ("D", "Development"),
                                       ("M", "Maintenance"),
                                       ("C", "Closed")))
    total_hours = models.IntegerField("Total Hours",
                                      default=-1)

    class Meta:
        db_table = "projects"
        ordering = ["number"]

    def __str__(self):
        return f"{self.number} - {self.title[:20]}"


class Client(models.Model):
    name = models.CharField("Name",
                            max_length=150)
    company = models.ForeignKey("Company",
                                on_delete=models.CASCADE)
    email = models.EmailField("Email")
    phone = PhoneNumberField("Direct Phone", blank=True)

    class Meta:
        db_table = "clients"
        ordering = ["company__name", "name"]

    def __str__(self):
        return f"{self.name} - {self.company.name[:20]}"


class Company(models.Model):
    name = models.CharField("Name",
                            max_length=150)
    address = models.TextField("Address",
                               default="",
                               blank=True)
    phone = PhoneNumberField("Main Phone", blank=True)
    fax = PhoneNumberField("Fax", blank=True)

    class Meta:
        db_table = "companies"
        ordering = ["name"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.name}"

    
class Hours(models.Model):
    quantity = models.DecimalField("quantity",
                                   max_digits=4,
                                   decimal_places=2,
                                   default=0.0)
    date = models.DateField("Date",
                            default=datetime.date.today)
    project = models.ForeignKey("Project",
                                on_delete=models.CASCADE)
    notes = models.CharField("Notes",
                             max_length=280,
                             default="",
                             blank=True)
    billed = models.BooleanField("Billed?",
                                 default=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)


    class Meta:
        db_table = "hours"
        ordering = ["-date", "project__number"]
        verbose_name = "Hours"
        verbose_name_plural = "Hours"

    def __str__(self):
        return f"{self.date} - {self.quantity} hours - {self.project.number}"
