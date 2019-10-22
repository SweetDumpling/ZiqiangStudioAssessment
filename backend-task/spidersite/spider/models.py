from django.db import models


class Lecture(models.Model):
    url = models.URLField(max_length=130)
    page_title = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    speaker = models.CharField(max_length=50)
    announce_date = models.DateField()
    time = models.CharField(max_length=50)
    room = models.CharField(max_length=50)

    def __str__(self):
        return self.page_title
