from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NewsletterSerializer
from .models import NewsletterModel
# Create your views here.

class NewsletterView(APIView):
  
    def post(self,request):

        serializer= NewsletterSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()

        return Response({
            "status" : 200,
            "msg" : "Newsletter Saved Successfully"
        })


    def get(self,request):

        obj = NewsletterModel.objects.all()

        serializer = NewsletterSerializer(obj,context={"request": request},many=True)

        return Response({
            "status" : 200,
            "msg" : "Newsletter Fetch successfully",
            "data" : serializer.data
        })

    def patch(self,request):

        obj_id = request.GET.get("id")

        obj = NewsletterModel.objects.get(id=obj_id)

        serializer = NewsletterSerializer(obj,data=request.data,partial= True)
        serializer.is_valid()
        serializer.save()

        return Response({
            "status" : 200,
            "msg" : "Partially Data Updated"
        })


    def delete(self,request):

        obj_id = request.GET.get("id")

        obj = NewsletterModel.objects.get(id=obj_id)

        obj.delete()

        return Response({
            "status" : 200,
            "msg" : "Data Deleted Successfully"
        })