"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from projectFocusapi.models import Lot, ProjectNote, Super, Project, LotNote, ProjectNote
from django.contrib.auth.models import User #pylint:disable=imported-auth-user


class ProjectNoteView(ViewSet):
    """Level up events"""

    def create(self, request):
        """Handle POST operations for events
        Returns:
            Response -- JSON serialized event instance
        """
        project_note = ProjectNote()
        #super = Super.objects.get(user=request.auth.user)
        project = Project.objects.get(pk=request.data["projectId"])
        #project_note = ProjectNote.objects.get(pk=request.data["projectNoteId"])

        project_note.name = request.data["name"]
        project_note.date = request.data["date"]
        project_note.itemsReceived = request.data["itemsReceived"]
        project_note.description = request.data["description"]
        project_note.contactNumber = request.data["contactNumber"]
        #project_note.super = super
        project_note.projectId = project
        

        #note.lot = lot

        try:
            project_note.save()
            
            serializer = ProjectNoteSerializer(project_note, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single event
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            project_note = ProjectNote.objects.get(pk=pk)
            serializer = ProjectNoteSerializer(project_note, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an event
        Returns:
            Response -- Empty body with 204 status code
        """
        #super = Super.objects.get(user=request.auth.user)

        project_note = ProjectNote.objects.get(pk=pk)
        project_note.name = request.data["name"]
        project_note.date = request.data["date"]
        project_note.itemsReceived = request.data["itemsReceived"]
        project_note.description = request.data["description"]
        project_note.contactNumber = request.data["contactNumber"]
        project_note.super = super

        #lot = Lot.objects.get(pk=request.data["lotId"])
        project_note.lot = project_note
        project_note.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            project_note = ProjectNote.objects.get(pk=pk)
            project_note.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProjectNote.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to events resource
        Returns:
            Response -- JSON serialized list of events
        """
        project_notes = ProjectNote.objects.all()
        super = Super.objects.get(user=request.auth.user)
        # Support filtering events by game
        lot = self.request.query_params.get('lot_id', None)
        if lot is not None:
            project_notes = project_notes.filter(lot__id=lot)

        """ for note in notes:
            note.joined = super in note.attendees.all() """

        serializer = ProjectNoteSerializer(
            project_notes, many=True, context={'request': request})
        return Response(serializer.data)

class ProjectNoteUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProjectNoteSuperSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = ProjectNoteUserSerializer(many=False)

    class Meta:
        model = Super
        fields = ['user', 'id']


class LotSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Lot
        fields = '__all__'
class ProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Project
        fields = '__all__'


class ProjectNoteSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    #super = ProjectNoteSuperSerializer(many=False)
    #lot = LotSerializer(many=False)
    #project = ProjectSerializer(many=False)

    class Meta:
        model = ProjectNote
        fields = '__all__'

class LotNoteSerializer(serializers.ModelSerializer):
    super = ProjectNoteSuperSerializer(many=False)
    lot = LotSerializer(many=False)

    class Meta:
        model = LotNote
        fields = '__all__'