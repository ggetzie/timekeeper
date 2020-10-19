from django.contrib import admin

from main.models import Project, Client, Company, Hours

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "status")
    list_display_linkes = ("number", "title")
    date_hierarcy = "start_date"
    list_editable = ("status",)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company_name")

    def company_name(self, obj):
        return obj.company.name

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Hours)
class HoursAdmin(admin.ModelAdmin):
    list_display = ("date", "project_title", "quantity", "billed")
    list_editable = ("billed",)
    list_display_links = ("date", "project_title")
    list_filter = ("project", "date")

    def project_title(self, obj):
        return obj.project.title
