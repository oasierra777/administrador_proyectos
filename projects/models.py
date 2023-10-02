from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from status.models import Status

import datetime

class Project(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()
    dead_line = models.DateField()
    create_date = models.DateField(default = datetime.date.today)
    slug = models.CharField(max_length = 50, default = "")

    def validate_unique(self, exclude = None):
        self.slug = self.create_slug_field(self.title)
        if Project.objects.filter(slug = self.slug).exclude(pk = self.id).exists():
            raise ValidationError('Ya se encuentra un proyecto validado con ese nombreee')

    def create_slug_field(self, value):
        return value.lower().replace(" ", "-")

    def get_id_status(self):
        return self.projectstatus_set.last().status_id

    def get_status(self):
        return self.projectstatus_set.last().status

    def user_has_permission(self, user):
        #va a buscar un id en una lista select * from projectuser where permission_id in(la lista)
        #la lista le pertenece a ProjectPermission entonces vamos a ella
        return self.projectuser_set.filter(user=user,
                    permission_id__in = ProjectPermission.admin_permission()).count() > 0

    def __str__(self):
        return self.title

class ProjectStatus(models.Model):
    project = models.ForeignKey(Project)
    status = models.ForeignKey(Status)
    create_date = models.DateTimeField(default = timezone.now)

class ProjectPermission(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()
    level = models.IntegerField()
    create_date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.title

    @classmethod
    def founder_permission(cls):
        return ProjectPermission.objects.get(pk=1)

    @classmethod
    def co_founder_permission(cls):
        return ProjectPermission.objects.get(pk=2)

    @classmethod
    def contributor_permission(cls):
        return ProjectPermission.objects.get(pk=3)

    #generamos un metodo de classmethod
    @classmethod
    def admin_permission(cls):
        return[1, 3]

class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    user = models.ForeignKey(User)
    permission = models.ForeignKey(ProjectPermission)
    create_date = models.DateTimeField(default = timezone.now)

    def get_project(self):
        return self.project

    def is_founder(self):
        #si ambos registros son el mismo es fundador
        return self.permission == ProjectPermission.founder_permission()

    def valid_change_permission(self):
        if not self.is_founder():
            return True
        return self.exist_founder()

    def exist_founder(self):
        #existen otros fundadores aparte de ti
        return ProjectUser.objects.filter(project=self.project,
                        permission=ProjectPermission.founder_permission()).exclude(user=self.user).count()>0
