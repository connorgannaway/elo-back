from distutils.ccompiler import gen_lib_options
from backend import settings
from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from .serializers import *
import math
import random

ELO_K = 7

def Probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

def EloRating(Ra, Rb, K, d):
   
  
    # To calculate the Winning
    # Probability of Player B
    Pb = Probability(Ra, Rb)
  
    # To calculate the Winning
    # Probability of Player A
    Pa = Probability(Rb, Ra)
  
    # Case -1 When Player A wins
    # Updating the Elo Ratings
    if (d == 1) :
        Ra = Ra + K * (1 - Pa)
        Rb = Rb + K * (0 - Pb)
      
  
    # Case -2 When Player B wins
    # Updating the Elo Ratings
    else :
        Ra = Ra + K * (0 - Pa)
        Rb = Rb + K * (1 - Pb)

    return Ra, Rb


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        #if(settings.ON_HEROKU):
        #    ip = x_forwarded_for.split(',')[-1]
        #else:
        #    ip = x_forwarded_for.split(',')[0]
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#/api/votes/
class VoteList(APIView):
    def get(self, request, format=None):
        try:
            if(request.query_params.get('gender').lower() == 'm'):
                votes = Vote.objects.filter(gender='M')
            elif(request.query_params.get('gender').lower() == 'f'):
                votes = Vote.objects.filter(gender='F')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            votes = Vote.objects.all()

        serializer = VoteSerializer(votes, many=True)
        
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            it1 = serializer.validated_data['item1']
            it2 = serializer.validated_data['item2']

            Ra, Rb = EloRating(
                it1.rating,
                it2.rating,
                ELO_K,
                serializer.validated_data['item1win']
                )
            it1.rating = Ra
            it2.rating = Rb

            if(serializer.validated_data['item1win'] == 1):
                it1.votes += 1
            else:
                it2.votes += 1

            serializer.validated_data['ipaddress'] = get_client_ip(request)

            it1.save()
            it2.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#/api/votes/<int:pk>/
class VoteDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def getObject(self, pk):
        try:
            return Vote.objects.get(pk=pk)
        except Vote.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk, format=None):
        vote = self.getObject(pk)
        serializer = VoteSerializer(vote)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vote = self.getObject(pk)
        serializer = VoteSerializer(vote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vote = self.getObject(pk)
        try:
            vote.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


#/api/items/
class ItemList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        try:
            if(request.query_params['gender'].lower() == 'm'):
                items = Item.objects.filter(gender='M').order_by('-rating')
            elif(request.query_params['gender'].lower() == 'f'):
                items = Item.objects.filter(gender='F').order_by('-rating')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            items = Item.objects.all()
            
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

#/api/random/
class Item_Random(APIView):
    def get(self, request, format=None):
        try:
            if(request.query_params['gender'].lower() == 'm'):
                pks = Item.objects.values_list('pk', flat=True).filter(gender='M')
            elif(request.query_params['gender'].lower() == 'f'):
                pks = Item.objects.values_list('pk', flat=True).filter(gender='F')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        randomPk = random.sample(list(pks), 2)
        items = Item.objects.filter(pk=randomPk[0]) | Item.objects.filter(pk=randomPk[1])
        serializer = ItemSerializer(items, many=True)

        return Response(serializer.data)

#/api/colleges/
class CollegeList(APIView):
    def get(self, request, format=None):
        try:
            if(request.query_params['gender'].lower() == 'm'):
                colleges = College.objects.filter(gender='M').order_by('-rating')
            elif(request.query_params['gender'].lower() == 'f'):
                colleges = College.objects.filter(gender='F').order_by('-rating')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data)