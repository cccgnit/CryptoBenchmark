# pylint: disable = unused-variable
import json
import serial

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from benchmark.models import CipherResult, SystemInfo
from benchmark.serializers import CipherResultSerializer, SystemInfoSerializer


def index(request):
    cipher_result_list = CipherResult.objects.order_by('-startTime')[:5]
    context = {'cipher_result_list': cipher_result_list}
    return render(request, 'benchmark/grid-multiple.html', context)


def ptlnx_serial(request):
    serial_line = 'COM3'
    speed = 115200
    ser = serial.Serial(port=serial_line, baudrate=speed, timeout=5)
    result = ser.write('python3 /run/media/mmcblk0p2/test.py\r\n'.encode('gbk'))
    print(ser.readline())
    print(ser.readline())
    print(ser.readline(), type(ser.readline()))
    ser.close()


# FBV, function base view
# CBV, class base view
# Create your views here.

# ViewSets define the view behavior.


class CipherResultViewSet(viewsets.ModelViewSet):
    queryset = CipherResult.objects.all()
    serializer_class = CipherResultSerializer

    @action(methods=['post'], detail=False)
    def new_result(self, request):
        data = json.loads(request.body)
        CipherResult.objects.create(**data)
        res = {
            'success': True,
            'data': data
        }
        return Response(res)

    @action(methods=['get'], detail=False)
    def all_result(self, request):
        data = CipherResultSerializer(
            CipherResult.objects.all(), many=True).data
        res = {
            'success': True,
            'data': data
        }
        return Response(res)


class SystemInfoViewSet(viewsets.ModelViewSet):
    queryset = SystemInfo.objects.all()
    serializer_class = SystemInfoSerializer

    @action(methods=['post'], detail=False)
    def new_result(self, request):
        data = json.loads(request.body)
        SystemInfo.objects.create(**data)
        res = {
            'success': True,
            'data': data
        }
        return Response(res)

    @action(methods=['get'], detail=False)
    def all_result(self, request):
        data = SystemInfoSerializer(
            SystemInfo.objects.all(), many=True).data
        res = {
            'success': True,
            'data': data
        }
        return Response(res)
