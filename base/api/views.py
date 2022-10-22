from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Event
from .serializers import EventSerializer



@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api/v1/',
        'GET /api/events/v1/',
        'GET /api/events/v1/:id/'
    ]
    return Response(routes)


@api_view(['GET'])
def get_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_event(request, pk):
    event = Event.objects.get(id=pk)
    serializer = EventSerializer(event, many=False)
    return Response(serializer.data)
