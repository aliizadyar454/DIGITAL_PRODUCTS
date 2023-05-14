from django.shortcuts import render
from rest_framework import viewsets,generics

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from  .models import Category,Product,File
from .serializers import ProductSerializer,CategorySerializer,FileSerializer

# Create your views here.
class ProductListView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True,context={"request":request})
        return Response(serializer.data)


class ProductDetailView(APIView):
    def get(self,request,pk):
        try:
             product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product,context={"request":request})
        return Response(serializer.data)

class CategoryDetailView(APIView):
    def get(self,request,pk):
        try:
             category = Category.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(category,context={"request":request})
        return Response(serializer.data)
class FileListView(APIView):
    def get(self,request , product_id):
        files = File.objects.filter(product_id = product_id)
        serializer = FileSerializer(files,many=True,context={"request":request})
        return Response(serializer.data)

class FileDetailView(APIView):
    def get(self,request ,product_id, pk):
        try:
            f = File.objects.get(pk=pk,product_id = product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FileSerializer(f,context={"request":request})
        return Response(serializer.data)
        