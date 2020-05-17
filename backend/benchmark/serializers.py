from rest_framework import serializers
from benchmark.models import CipherResult, SystemInfo

# Serializers define the API representation.


class CipherResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CipherResult
        fields = ('cipher', 'startTime', 'elapsedTime', 'throughput',
                  'cpuUtilPct', 'memUsed', 'memUsedPct',)


class SystemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = ('startTime', 'cpuUtilPct', 'memUsedPct',
                  'getTotal', 'sentTotal',)
