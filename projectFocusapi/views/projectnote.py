from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from projectFocusapi.models import Project, Note, ProjectNote

class ProjectNoteView(ViewSet):


    def create(self, request):
        projectNote = ProjectNote()
        project = Project.objects.get(pk=request.data["projectId"])
        note = Note.objects.get(pk=request.data["noteId"])
        projectNote.note = note
        projectNote.project = project

        try:
            projectNote.save()
            serializer = ProjectNoteSerializer(projectNote, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        projectNote = ProjectNote.objects.get(pk=pk)
        projectNote.project = Project.objects.get(pk=request.data["lot"])
        projectNote.note = Note.objects.get(pk=request.data["note"])
        projectNote.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


        return Response(projectnote)

    def destroy(self, request, pk=None):
        try:
            projectNote = ProjectNote.objects.get(pk=pk)
            projectNote.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
            project = self.request.query_params.get('project', None)
            if project is not None:
                projectNotes = ProjectNote.objects.filter(project__id=project)
            else:
                note = self.request.query_params.get('note', None)
                if note is not None:
                    projectNotes = ProjectNote.objects.filter(note__id=note)
                else:
                    projectNotes = ProjectNote.objects.all()

            serializer = ProjectNoteSerializer(
                projectNotes, many=True, context={'request': request}
            )
            return Response(serializer.data)

class ProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    #user = UserSerializer(many=False)

    class Meta:
        model = Project
        fields = '__all__'
class NoteSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    #user = UserSerializer(many=False)

    class Meta:
        model = Note
        fields = '__all__'


class ProjectNoteSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(many=False)
    note = NoteSerializer(many=False)
    class Meta:
        model = ProjectNote
        fields = '__all__'

