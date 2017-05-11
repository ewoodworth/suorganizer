# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.
class Tag(models.Model):
    name = models.CharField(
         max_length=31,
         unique = True)
    slug = models.SlugField(
         max_length=31,
         unique = True,
         help_text = 'A label for URL config')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Startup(models.Model):
    name = models.CharField(
         max_length=31,
         db_index = True)
    slug = models.SlugField(
         max_length=31, 
         unique=True, 
         help_text='A label for URL config')
    description = models.TextField()
    founded_date = models.DateField()
    contact = models.EmailField()
    website = models.URLField(
            max_length=255)
    #many to many relationship with tags.
    #this relationship goes ONLY IN ONE OF THE SIDES
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        get_latest_by = 'founded_date'

class NewsLink(models.Model):
    title = models.CharField(
          max_length=63)
    pub_date = models.DateField(
             'date published')
    link = models.URLField(
         max_length=255)
    #one-to-one relation with startups
    startup = models.ForeignKey(Startup)

    def __str__(self):
        return "{}:{}".format(
            self.startup, self.title)

    class Meta:
        verbose_name = 'news_article'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

class Post(models.Model):
    title = models.CharField(
          max_length=63)
    slug = models.SlugField(
         max_length=31, 
         unique=True, 
         help_text = 'A label for URL config',
         unique_for_month = 'pub_date')
    text = models.TextField()
    pub_date = models.DateField(
        'date published',
        # default = datetime.datetime.now,
        # auto_now_add = True,
        )
    #many to many relationships with tags and startups
    tags = models.ManyToManyField(
        Tag, 
        related_name='blog_posts')
    startups = models.ManyToManyField(
             Startup,
             related_name = 'blog_posts')

    def __str__(self):
        return "{} on {}".format(
            self.title,
            self.pub_date.strftime('%Y-%m-%d'))
        
    def __init__(self):
         if pub_date is None:
             pub_date = []
         self.pub_date = datetime.datetime.now

    class Meta:
        verbose_name = 'blog post'
        ordering = ['-pub_date', 'title']
        get_latest_by = 'pub_date'