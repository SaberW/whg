# place.models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone

from django.contrib.auth.models import User
#from datasets.models import Dataset

from main.choices import *

import json

class Place(models.Model):
    # let id be auto-maintained, as Django decrees/prefers
    title = models.CharField(max_length=255)
    src_id = models.CharField(max_length=24)
    dataset = models.ForeignKey('datasets.Dataset', db_column='dataset',
        to_field='label', related_name='places', on_delete=models.CASCADE)
    ccodes = ArrayField(models.CharField(max_length=2))

    def __str__(self):
        # return str(self.id)
        return '%s:%d' % (self.dataset, self.id)

    class Meta:
        managed = True
        db_table = 'places'
        indexes = [
            models.Index(fields=['src_id', 'dataset']),
        ]

class Source(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: force unique...turn into slug or integer
    src_id = models.CharField(max_length=30, unique=True)    # contributor's id
    uri = models.URLField(null=True, blank=True)
    label = models.CharField(max_length=255)    # short, e.g. title, author
    citation = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.src_id

    class Meta:
        managed = True
        db_table = 'sources'

class PlaceName(models.Model):
    # {toponym, lang, citation{}, when{}}
    place_id = models.ForeignKey(Place, related_name='names',
        default=-1, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=100, blank=True, null=True)
    toponym = models.CharField(max_length=200)
    name_src = models.ForeignKey(Source, null=True, on_delete=models.SET_NULL)
    json = JSONField(blank=True, null=True)

    src_id = models.CharField(max_length=24,default='') # contributor's identifier

    def __str__(self):
        return self.toponym

    class Meta:
        managed = True
        db_table = 'place_name'

class PlaceType(models.Model):
    # identifier, label, source_label, when{}
    place_id = models.ForeignKey(Place,related_name='types',
        default=-1, on_delete=models.CASCADE)
    json = JSONField(blank=True, null=True)

    src_id = models.CharField(max_length=24,default='') # contributor's identifier

    def __str__(self):
        return self.json['src_label'] #(self.json.src_label)

    class Meta:
        managed = True
        db_table = 'place_type'

class PlaceGeom(models.Model):
    place_id = models.ForeignKey(Place,related_name='geoms',
        default=-1, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=100, blank=True, null=True)
    geom_src = models.ForeignKey(Source, null=True, db_column='geom_src',
        to_field='src_id', on_delete=models.SET_NULL)
    json = JSONField(blank=True, null=True)

    src_id = models.CharField(max_length=24,default='') # contributor's identifier

    class Meta:
        managed = True
        db_table = 'place_geom'

class PlaceLink(models.Model):
    place_id = models.ForeignKey(Place,related_name='links',
        default=-1, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=100, blank=True, null=True)
    review_note = models.CharField(max_length=2044, blank=True, null=True)
    json = JSONField(blank=True, null=True)

    src_id = models.CharField(max_length=24,default='') # contributor's identifier

    class Meta:
        managed = True
        db_table = 'place_link'

class PlaceWhen(models.Model):
    place_id = models.ForeignKey(Place,related_name='whens',
        default=-1, on_delete=models.CASCADE)
    json = JSONField(blank=True, null=True)
    # timespans[{start{}, end{}}], periods[{name,id}], label, duration

    src_id = models.CharField(max_length=24,default='') # contributor's identifier

    class Meta:
        managed = True
        db_table = 'place_when'

class PlaceRelated(models.Model):
    place_id = models.ForeignKey(Place,related_name='related',
        default=-1, on_delete=models.CASCADE)
    json = JSONField(blank=True, null=True)
    # relation_type, relation_to, label, when{}, citation{label,id}, certainty

    src_id = models.CharField(max_length=24,default='') # contributor's identifier

    class Meta:
        managed = True
        db_table = 'place_related'

class PlaceDescription(models.Model):
    place_id = models.ForeignKey(Place,related_name='descriptions',
        default=-1, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=100, blank=True, null=True)
    json = JSONField(blank=True, null=True)
    # id, value, lang

    src_id = models.CharField(max_length=24,default='') # contributor's identifier

    class Meta:
        managed = True
        db_table = 'place_description'

class PlaceDepiction(models.Model):
    place_id = models.ForeignKey(Place,related_name='depictions',
        default=-1, on_delete=models.CASCADE)
    json = JSONField(blank=True, null=True)
    # id, title, license

    src_id = models.CharField(max_length=24,default='') # contributor's identifier

    class Meta:
        managed = True
        db_table = 'place_depiction'
        
# raw hits from reconciliation
# [{'place_id', 'task_id', 'authority', 'dataset', 'authrecord_id', 'id'}]
#class Hit(models.Model):
    #place_id = models.ForeignKey(Place, on_delete=models.CASCADE)
    ## FK to celery_results_task_result.task_id; TODO: written yet?
    ## task_id = models.ForeignKey(TaskResult, related_name='task_id', on_delete=models.CASCADE)
    #task_id = models.CharField(max_length=50)
    #authority = models.CharField(max_length=12, choices=AUTHORITIES )
    #dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    #query_pass = models.CharField(max_length=12, choices=AUTHORITIES )
    #src_id = models.CharField(max_length=50)
    #reviewed = models.BooleanField(default=False)

    ## authority record identifier (could be uri)
    #authrecord_id = models.CharField(max_length=255)

    ## json response; parse later according to authority
    #json = JSONField(blank=True, null=True)
    #geom = JSONField(blank=True, null=True)

    #def __str__(self):
        #return str(self.id)

    #class Meta:
        #managed = True
        #db_table = 'hits'
