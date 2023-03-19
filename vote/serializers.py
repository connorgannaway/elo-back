from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'pk',
            'name',
            'votes',
            'rating',
            'gender',
            'college',
        ]
        extra_kwargs = {
            "college": {"required": False},
        }

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = [
            'pk',
            'item1',
            'item2',
            'item1win',
            'ipaddress',
            'gender',
        ]
        extra_kwargs = {
            "ipaddress": {"required": False},
        }

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = [
            'pk',
            'name',
            'rating',
            'gender',
        ]