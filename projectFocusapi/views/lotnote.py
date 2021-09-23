"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from projectFocusapi.models import Lot, LotNote, Super, Project, ProjectNote
from django.contrib.auth.models import User #pylint:disable=imported-auth-user


class LotNoteView(ViewSet):
    """Level up events"""

    def create(self, request):
        """Handle POST operations for events
        Returns:
            Response -- JSON serialized event instance
        """
        lot_note = LotNote()
        #super = Super.objects.get(user=request.auth.user)
        lot = Lot.objects.get(pk=request.data["lotId"])
        #lot_note = LotNote.objects.get(pk=request.data["lotNoteId"])
        
        lot_note.name = request.data["name"]
        lot_note.date = request.data["date"]
        lot_note.itemsReceived = request.data["itemsReceived"]
        lot_note.description = request.data["description"]
        lot_note.contactNumber = request.data["contactNumber"]
        #lot_note.super = super
        lot_note.lotId = lot
        

        #note.lot = lot

        try:
            lot_note.save()
            
            serializer = LotNoteSerializer(lot_note, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            lot_note = LotNote.objects.get(pk=pk)
            serializer = LotNoteSerializer(lot_note, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an event
        Returns:
            Response -- Empty body with 204 status code
        """
        #super = Super.objects.get(user=request.auth.user)

        lot_note = LotNote.objects.get(pk=pk)
        lot_note.name = request.data["name"]
        lot_note.date = request.data["date"]
        lot_note.itemsReceived = request.data["itemsReceived"]
        lot_note.description = request.data["description"]
        lot_note.contactNumber = request.data["contactNumber"]
        #lot_note.super = super

        #lot = Lot.objects.get(pk=request.data["lotId"])
        #lot_note.lot = lot
        lot_note.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            lot_note = LotNote.objects.get(pk=pk)
            lot_note.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except LotNote.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to events resource
        Returns:
            Response -- JSON serialized list of events
        """
        lot_notes = LotNote.objects.all()
        super = Super.objects.get(user=request.auth.user)
        # Support filtering events by game
        lot = self.request.query_params.get('lot_id', None)
        if lot is not None:
            lot_notes = lot_notes.filter(lot__id=lot)

        """ for note in notes:
            note.joined = super in note.attendees.all() """

        serializer = LotNoteSerializer(
            lot_notes, many=True, context={'request': request})
        return Response(serializer.data)

    
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
        fields = ['user', 'id']


class ProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Project
        fields = '__all__'

class LotSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    #lot_notes = LotNoteSerializer(many=True)
    class Meta:
        model = Lot
        fields = '__all__'

class LotNoteSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    #super = NoteSuperSerializer(many=False)
    lotId = LotSerializer(many=False)
    #lot_notes = LotNoteSerializer(many=True)
    #project = ProjectSerializer(many=False)

    class Meta:
        model = LotNote
        fields = '__all__'

