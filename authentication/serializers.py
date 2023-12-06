from rest_framework import serializers
from .models import MyUser




class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        exclude = ("password",)
        # fields = "__all__"