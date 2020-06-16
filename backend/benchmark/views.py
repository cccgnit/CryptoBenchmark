# pylint: disable = unused-variable
import datetime
import json
import time

import numpy as np
import serial
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from benchmark.models import CipherResult, SystemInfo
from benchmark.serializers import (CipherListSerializer,
                                   CipherResultSerializer,
                                   SystemInfoSerializer)

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

    # show benchmark cipher list
    @action(methods=['get'], detail=False)
    def cipher_list(self, request):
        cipher_list = []
        for r in CipherResult.objects.values_list('cipher').distinct():
            cipher_list.append(r[0])
        res = cipher_list
        return Response(res)

    # return a cipher benchmark result by django-restful-api
    @action(methods=['get'], detail=True)
    def result_list(self, request, pk=None):
        result_list = CipherResult.objects.filter(cipher=pk)
        elapsedTime_list = []
        throughput_list = []
        cpuUtilPct_list = []
        memUsed_list = []
        memUsedPct_list = []
        jitter_list = []
        res = {}
        for r in result_list:
            elapsedTime_list.append(float(r.elapsedTime))
            throughput_list.append(float(r.throughput))
            memUsed_list.append(float(r.memUsed))
            memUsedPct_list.append(float(r.memUsedPct))
            tmp = -0.1
            system_list = SystemInfo.objects.filter(
                startTime__range=(r.startTime-1, r.startTime+3))
            for i in system_list:
                tmp = max(i.cpuUtilPct, tmp)
            if tmp < 0:
                tmp = 0.5
            cpuUtilPct_list.append(float(r.cpuUtilPct) * tmp)
        for r in result_list:
            jitter_list.append(
                float('%0.2f' % (float(r.elapsedTime) - np.mean(elapsedTime_list))))
        res['elapsedTime_avg'] = float('%0.4f' % np.mean(elapsedTime_list))
        res['elapsedTime_std'] = float('%0.4f' % np.std(elapsedTime_list))
        res['throughput_avg'] = float('%0.4f' % np.mean(throughput_list))
        res['cpuUtilPct_avg'] = float('%0.6f' % np.mean(cpuUtilPct_list))
        res['memUsed_avg'] = float('%0.4f' % np.mean(memUsed_list))
        res['memUsedPct_avg'] = float('%0.6f' % np.mean(memUsedPct_list))
        res['elapsedTime'] = elapsedTime_list
        res['throughput'] = throughput_list
        res['cpuUtilPc'] = cpuUtilPct_list
        res['memUsed'] = memUsed_list
        res['memUsedPct'] = memUsedPct_list
        res['jitter'] = jitter_list
        return Response(res)

    # return all cipher benchmark result by django-restful-api
    @action(methods=['get'], detail=False)
    def all_cipher(self, request):
        cipher_list = []
        res_all = {}
        for r in CipherResult.objects.values_list('cipher').distinct():
            cipher_list.append(r[0])
        for cipher_name in cipher_list:
            result_list = CipherResult.objects.filter(cipher=cipher_name)
            elapsedTime_list = []
            throughput_list = []
            cpuUtilPct_list = []
            memUsed_list = []
            memUsedPct_list = []
            jitter_list = []
            res = {}
            for r in result_list:
                elapsedTime_list.append(float(r.elapsedTime))
                throughput_list.append(float(r.throughput))
                memUsed_list.append(float(r.memUsed))
                memUsedPct_list.append(float(r.memUsedPct))
                tmp = -0.1
                system_list = SystemInfo.objects.filter(
                    startTime__range=(r.startTime-1, r.startTime+3))
                for i in system_list:
                    tmp = max(i.cpuUtilPct, tmp)
                if tmp < 0:
                    tmp = 0.5
                cpuUtilPct_list.append(float(r.cpuUtilPct) * tmp)
            for r in result_list:
                jitter_list.append(
                    float('%0.2f' % (float(r.elapsedTime) - np.mean(elapsedTime_list))))
            res['elapsedTime_avg'] = float('%0.4f' % np.mean(elapsedTime_list))
            res['elapsedTime_std'] = float('%0.4f' % np.std(elapsedTime_list))
            res['throughput_avg'] = float('%0.4f' % np.mean(throughput_list))
            res['cpuUtilPct_avg'] = float('%0.6f' % np.mean(cpuUtilPct_list))
            res['memUsed_avg'] = float('%0.4f' % np.mean(memUsed_list))
            res['memUsedPct_avg'] = float('%0.6f' % np.mean(memUsedPct_list))
            res_all[cipher_name] = res
        return Response(res_all)

    # run cipher through COM3 serial
    @action(methods=['get'], detail=True)
    @csrf_exempt
    def run_cipher(self, request, pk=None):
        print('run_cipher')
        serial_line = 'COM3'
        speed = 115200
        ser = serial.Serial(port=serial_line, baudrate=speed, timeout=5)
        ser.write(
            'python3 /run/media/mmcblk0p2/cryptoapp/monitoragent.py & \r\n'.encode('gbk'))
        time.sleep(1)
        command = 'python3 /run/media/mmcblk0p2/cryptoapp/cryptoapp.py ' + \
            str(pk) + ' \r\n'
        result = ser.write(command.encode('gbk'))
        time.sleep(2)
        ser.write(
            'pid=$(ps x | grep monitoragent | grep -v grep | awk \'{print $1}\') \r\n '.encode('gbk'))
        # ser.write('echo $pid \r\n '.encode('gbk'))
        ser.write('kill $pid \r\n '.encode('gbk'))
        """ for i in range(20):
            print(ser.readline()) """
        ser.close()
        return HttpResponse('')

    # index html
    @action(methods=['get'], detail=False)
    def index(self, request):
        # cipher_result_list = CipherResult.objects.order_by('-startTime')[:5]
        cipher_list = []
        for r in CipherResult.objects.values_list('cipher').distinct():
            cipher_list.append(r[0])
        context = {'cipher_list': cipher_list}
        return render(request, 'benchmark/index.html', context)

    # benchmark result html for a cipher
    @action(methods=['get'], detail=True)
    def frontend(self, request, pk=None):
        context = {}
        context['cipher'] = pk
        # cipher benchmark info
        result_list = CipherResult.objects.filter(
            cipher=pk).order_by('-id')[:10]
        startTime_list = []
        elapsedTime_list = []
        throughput_list = []
        cpuUtilPct_list = []
        memUsed_list = []
        for r in result_list:
            t = datetime.datetime.fromtimestamp(r.startTime)
            startTime_list.insert(0, t)
            elapsedTime_list.insert(0, float(r.elapsedTime))
            throughput_list.insert(0, float(r.throughput))
            memUsed_list.insert(0, float(r.memUsed) / 1024.0)
            tmp = -0.1
            system_list = SystemInfo.objects.filter(
                startTime__range=(r.startTime-1, r.startTime+3))
            for s in system_list:
                tmp = max(s.cpuUtilPct, tmp)
            if tmp < 0:
                tmp = 0.5
            cpuUtilPct_list.insert(0, float(r.cpuUtilPct) * tmp * 100)
        context['startTime_list'] = startTime_list
        context['elapsedTime_list'] = elapsedTime_list
        context['throughput_list'] = throughput_list
        context['cpuUtilPct_list'] = cpuUtilPct_list
        context['memUsed_list'] = memUsed_list
        # system benchmark info
        system_list = SystemInfo.objects.all().order_by('-id')[:10]
        startTime_list = []
        cpuUtilPct_list = []
        memUsedPct_list = []
        getTotal_list = []
        sentTotal_list = []
        for s in system_list:
            t = datetime.datetime.fromtimestamp(s.startTime)
            startTime_list.insert(0, t)
            cpuUtilPct_list.insert(0, float(s.cpuUtilPct) * 100)
            memUsedPct_list.insert(0, float(s.memUsedPct) * 100)
            getTotal_list.insert(0, float(s.getTotal))
            sentTotal_list.insert(0, float(s.sentTotal))
        context['sys_startTime_list'] = startTime_list
        context['sys_cpuUtilPct_list'] = cpuUtilPct_list
        context['sys_memUsedPct_list'] = memUsedPct_list
        context['sys_getTotal_list'] = getTotal_list
        context['sys_sentTotal_list'] = sentTotal_list
        return render(request, 'benchmark/ech.html', context)


class SystemInfoViewSet(viewsets.ModelViewSet):
    queryset = SystemInfo.objects.all()
    serializer_class = SystemInfoSerializer

    @action(methods=['post'], detail=False)
    def new_systemInfo(self, request):
        data = json.loads(request.body)
        SystemInfo.objects.create(**data)
        res = {
            'success': True,
            'data': data
        }
        return Response(res)

    @action(methods=['get'], detail=False)
    def all_systemInfo(self, request):
        data = SystemInfoSerializer(
            SystemInfo.objects.all(), many=True).data
        res = {
            'success': True,
            'data': data
        }
        return Response(res)
