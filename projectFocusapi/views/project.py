"""View module for handling requests about game types"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from projectFocusapi.models import Project


class ProjectView(ViewSet):
    """Level up game types"""

    def create(self, request):
        """Handle POST operations for events
        Returns:
            Response -- JSON serialized event instance
        """
        ##super = Super.objects.get(user=request.auth.user)

        project = Project()
        project.name = request.data["name"]
        project.estimatedCost = request.data["estimatedCost"]
        project.estimatedCompletionDate = request.data["estimatedCompletionDate"]

        ##lot = Lot.objects.get(pk=request.data["lot"])
        ##note.lot = lot

        try:
            project.save()
            serializer = ProjectSerializer(project, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            project = Project.objects.get(pk=pk)
            serializer = ProjectSerializer(project, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        """Handle PUT requests for an event
        Returns:
            Response -- Empty body with 204 status code
        """

        project = Project.objects.get(pk=pk)
        project.name = request.data["name"]
        project.estimatedCost = request.data["estimatedCost"]
        project.estimatedCompletionDate = request.data["estimatedCompletionDate"]

        ##lot = Lot.objects.get(pk=request.data["lotId"])
        ##project.lot = lot
        project.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            project = Project.objects.get(pk=pk)
            project.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Project.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        projects = Project.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ProjectSerializer(
            projects, many=True, context={'request': request})
        return Response(serializer.data)


class ProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
        converts data from object to json string
    Arguments:
        serializers
    """
    class Meta:
        model = Project
        fields = '__all__'
