from django.db import models

# Create your models here.


class CipherResult(models.Model):
    cipher = models.CharField(max_length=100)
    startTime = models.IntegerField()
    elapsedTime = models.FloatField()
    throughput = models.FloatField()
    # CPU utilization percentage
    cpuUtilPct = models.FloatField(blank=True, null=True)
    # physical memory usage and percentage
    memUsed = models.FloatField(blank=True, null=True)
    memUsedPct = models.FloatField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.cipher


class SystemInfo(models.Model):
    startTime = models.IntegerField(blank=True, null=True)
    cpuUtilPct = models.FloatField(blank=True, null=True)
    memUsedPct = models.FloatField(blank=True, null=True)
    getTotal = models.IntegerField(blank=True, null=True)
    sentTotal = models.IntegerField(blank=True, null=True)

    objects = models.Manager()
