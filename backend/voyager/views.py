from rest_framework.response import Response
from rest_framework.views import APIView


class Hello(APIView):
    def get(self, request, format=None):
        return Response({'message': 'Hello unknown!'})

    def post(self, request, format=None):
        name = request.data['name']
        return Response({'message': f'Hello {name}!'})
