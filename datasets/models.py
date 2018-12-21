# datasets.models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from .choices import *

def user_directory_path(instance, filename):
    # upload to MEDIA_ROOT/user_<username>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.username, filename)

# TODO: operations on entire table
# class DatasetQueryset(models.Queryset):
#     pass
# class DatasetManager(models.Manager):
#     pass

# TODO: multiple files per dataset w/File model and formset
# TODO: linking delimited dataset with sources dataset
class Dataset(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='datasets', on_delete=models.CASCADE)
    # owner = models.ForeignKey(User, related_name='datasets', on_delete=models.CASCADE)
    label = models.CharField(max_length=20, null=False, unique="True")
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=2044, null=False)
    file = models.FileField(upload_to=user_directory_path)
    format = models.CharField(max_length=12, null=False,choices=FORMATS,
        default='delimited')
    datatype = models.CharField(max_length=12, null=False,choices=DATATYPES,
        default='place')
    delimiter = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=12, null=True, blank=True, choices=STATUS)
    upload_date = models.DateTimeField(null=True, auto_now_add=True)
    accepted_date = models.DateTimeField(null=True)
    # accepted_date = models.DateTimeField(null=True, auto_now_add=True)
    mapbox_id = models.CharField(max_length=200, null=True, blank=True)

    # backfilled
    header = ArrayField(models.CharField(max_length=30), null=True, blank=True)
    numrows = models.IntegerField(null=True, blank=True)
    numlinked = models.IntegerField(null=True, blank=True)
    total_links = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%d: %s' % (self.id, self.label)
    def get_absolute_url(self):
        # return f"/datasets/{self.id}"
        # return reverse('datasets:ds_edit', kwargs={'pk': self.id})
        return reverse('datasets:dataset-update', kwargs={'id': self.id})

    @property
    def tasks(self):
        from django_celery_results.models import TaskResult
        return TaskResult.objects.all().filter(task_args = '['+str(self.id)+']')

    class Meta:
        managed = True
        db_table = 'datasets'


@receiver(pre_delete, sender=Dataset)
def remove_file(**kwargs):
    instance = kwargs.get('instance')
    instance.file.delete(save=False)

# product of hit validation
class Link(models.Model):
    # WHG identifier
    place_id = models.ForeignKey('main.Place', on_delete="models.CASCADE")

    # contributor identifier
    src_id = models.CharField(max_length=24)

    authority = models.CharField(max_length=12, choices=AUTHORITIES )

    # authority place record identifier; could be uri
    authrecord_id = models.CharField(max_length=255)
    match_type = models.CharField(max_length=12, choices=MATCHTYPES )
    review_note = models.CharField(max_length=2044, blank=True, null=True)
    flag_geom = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True
        db_table = 'links'

# raw hits from reconciliation
class Hit(models.Model):
    # FK to celery_results_task_result.task_id; TODO: written yet?
    task_id = models.CharField(max_length=50)
    authority = models.CharField(max_length=12, choices=AUTHORITIES )
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    place_id = models.ForeignKey('main.Place', on_delete=models.CASCADE)
    query_pass = models.CharField(max_length=12, choices=AUTHORITIES )
    src_id = models.CharField(max_length=50)

    # authority record identifier (could be uri)
    authrecord_id = models.CharField(max_length=255)

    # json response; parse later according to authority
    json = JSONField(blank=True, null=True)
    geom = JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True
        db_table = 'hits'
