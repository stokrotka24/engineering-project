from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def hello(request, format=None):
    if request.method == 'GET':
        return Response({'message': 'Hello unknown!'})

    name = request.data['name']
    return Response({'message': f'Hello {name}!'})
