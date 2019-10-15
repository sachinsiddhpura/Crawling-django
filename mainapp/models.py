from django.db import models

# Create your models here.
class MainProject(models.Model):
    PROJECT_NAME = models.CharField(max_length=50)
    HOMEPAGE = models.URLField(max_length=100)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.PROJECT_NAME

    def get_absolute_url(self):
        return reverse('mainapp_mainproject_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('mainapp_mainproject_update', args=(self.pk,))
