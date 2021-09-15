"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from projectFocusapi.models import Lot, Note, Super


class NoteView(ViewSet):
    """Level up events"""

    def create(self, request):
        """Handle POST operations for events
        Returns:
            Response -- JSON serialized event instance
        """
        super = Super.objects.get(user=request.auth.user)

        note = Note()
        note.name = request.data["name"]
        note.date = request.data["date"]
        note.itemsReceived = request.data["itemsReceived"]
        note.description = request.data["description"]
        note.contactNumber = request.data["contactNumber"]
        note.super = super

        lot = Lot.objects.get(pk=request.data["lot"])
        note.lot = lot

        try:
            note.save()
            serializer = NoteSerializer(note, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            note = Note.objects.get(pk=pk)
            serializer = NoteSerializer(note, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an event
        Returns:
            Response -- Empty body with 204 status code
        """
        super = Super.objects.get(user=request.auth.user)

        note = Note.objects.get(pk=pk)
        note.name = request.data["name"]
        note.date = request.data["date"]
        note.itemsReceived = request.data["itemsReceived"]
        note.description = request.data["description"]
        note.contactNumber = request.data["contactNumber"]
        note.super = super

        lot = Lot.objects.get(pk=request.data["lotId"])
        note.lot = lot
        note.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            note = Note.objects.get(pk=pk)
            note.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to events resource
        Returns:
            Response -- JSON serialized list of events
        """
        notes = Note.objects.all()
        super = Super.objects.get(user=request.auth.user)
        # Support filtering events by game
        lot = self.request.query_params.get('lot_id', None)
        if lot is not None:
            notes = notes.filter(lot__id=lot)

        """ for note in notes:
            note.joined = super in note.attendees.all() """

        serializer = NoteSerializer(
            notes, many=True, context={'request': request})
        return Response(serializer.data)

    """ @action(methods=['post', 'delete'], detail=True)
    #detail=true will add a Primary key to the url
    #will take the name of the method and turn it into the route we can go to because that is the method name.
    def signup(self, request, pk):
        #get the gamer, taking the token and matching it from the front end
        super = Super.objects.get(user=request.auth.user)
        #try block here to try and get the event, if that doesnt work because the event doesnt exist
        #it will go the except block and respond with the message and return the 404_not_found error
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response(
            {'message': 'Note does not exist.'},
            status=status.HTTP_404_NOT_FOUND
        ) """
"""         #if the method we are using is post, then add the gamer to the attendees list. by using add and passing the gamer to it
        if request.method == "POST":
            try:
                event.attendees.add(gamer)
                #if that works, send the 201 created status
                return Response({}, status=status.HTTP_201_CREATED) #empty dictionary bc not wanting to do with anything with the data thats sent back
            except Exception as ex:
                #if anything goes wrong with that try, respond with what is at the zero index 
                return Response({'message': ex.args[0]})
            # if its a delete request, delete the gamer from the attendees list
        elif request.method == "DELETE":
            try:
            #if the delete request is successful, send a 204_no_content response, which will return nothing other than the status
                event.attendees.remove(gamer)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                #if that doesnt work, send the response at the zero index
                return Response({'message': ex.args[0]})
 """
class NoteUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class NoteSuperSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = NoteUserSerializer(many=False)

    class Meta:
        model = Super
        fields = ['user']


class LotSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Lot
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    super = NoteSuperSerializer(many=False)
    ##lot = LotSerializer(many=False)

    class Meta:
        model = Note
        fields = '__all__'