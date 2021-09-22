"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from projectFocusapi.models import Lot, Note, Super, Project, LotNote, ProjectNote
from django.contrib.auth.models import User #pylint:disable=imported-auth-user


class NoteView(ViewSet):
    """Level up events"""

    def create(self, request):
        """Handle POST operations for events
        Returns:
            Response -- JSON serialized event instance
        """
        note = Note()
        super = Super.objects.get(user=request.auth.user)
        lot = Lot.objects.get(pk=request.data["lotId"])
        note = Note.objects.get(pk=request.data["noteId"])
        project = Project.objects.get(pk=request.data["projectId"])
        if request.data == lot:
            try:
                note.name = request.data["name"]
                note.date = request.data["date"]
                note.itemsReceived = request.data["itemsReceived"]
                note.description = request.data["description"]
                note.contactNumber = request.data["contactNumber"]
                note.super = super
                note.lotId = lot
                try:
                    note.save()
                    serializer = LotNoteSerializer(note, context={'request': request})
                    return Response(serializer.data)
                except ValidationError as ex:
                    return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return

        elif request.data == project:
            try:
                note.name = request.data["name"]
                note.date = request.data["date"]
                note.itemsReceived = request.data["itemsReceived"]
                note.description = request.data["description"]
                note.contactNumber = request.data["contactNumber"]
                note.super = super
                note.projectId = project
                try:
                    note.save()
                    serializer = ProjectNoteSerializer(note, context={'request': request})
                    return Response(serializer.data)
                except ValidationError as ex:
                    return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return
        else:
            return

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


class NoteSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    super = NoteSuperSerializer(many=False)
    #lot = LotSerializer(many=False)
    #project = ProjectSerializer(many=False)

    class Meta:
        model = Note
        fields = '__all__'

class LotNoteSerializer(serializers.ModelSerializer):
    super = NoteSuperSerializer(many=False)
    lot = LotSerializer(many=False)

    class Meta:
        model = Note
        fields = '__all__'

class ProjectNoteSerializer(serializers.ModelSerializer):
    super = NoteSuperSerializer(many=False)
    project = ProjectSerializer(many=False)

    class Meta:
        model = Project
        fields = '__all__'