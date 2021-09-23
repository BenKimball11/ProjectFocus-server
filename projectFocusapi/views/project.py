"""View module for handling requests about game types"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from projectFocusapi.models import Lot, Project, Super, ProjectNote


class ProjectView(ViewSet):
    """Level up game types"""

    def create(self, request):
        """Handle POST operations for events
        Returns:
            Response -- JSON serialized event instance
        """
        lot = Lot.objects.get(pk=request.data["lotId"])

        project = Project()
        project.name = request.data["name"]
        project.estimatedCost = request.data["estimatedCost"]
        project.estimatedCompletionDate = request.data["estimatedCompletionDate"]
        project.lotId = lot
        #projectNote=projectNote


        try:
            project.save()
            serializer = ProjectSerializer(project, context={'request': request}) #converting data into json
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        lot = Lot.objects.get(pk=request.data["lotId"])

        project = Project.objects.get(pk=pk)
        project.name = request.data["name"]
        project.estimatedCost = request.data["estimatedCost"]
        project.estimatedCompletionDate = request.data["estimatedCompletionDate"]
        #project.projectNote = Note.objects.get(pk=request.data['projectNote'])

        project.lotId = lot
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

        serializer = ProjectSerializer(projects, many=True, context={'request': request}) # convert to json
        return Response(serializer.data)


    @action(methods=['post', 'delete'], detail=True)
    #detail=true will add a Primary key to the url
    #will take the name of the method and turn it into the route we can go to because that is the method name.
    def signup(self, request, pk):
        #get the gamer, taking the token and matching it from the front end
        project_note = ProjectNote.objects.get(user=request.auth.user)
        #try block here to try and get the event, if that doesnt work because the event doesnt exist
        #it will go the except block and respond with the message and return the 404_not_found error
        try:
            project_note = ProjectNote.objects.get(pk=pk)
        except ProjectNote.DoesNotExist:
            return Response(
            {'message': 'Event does not exist.'},
            status=status.HTTP_404_NOT_FOUND
        )
        #if the method we are using is post, then add the gamer to the attendees list. by using add and passing the gamer to it
        if request.method == "POST":
            try:
                project_note.projects.add(project_note)
                #if that works, send the 201 created status
                return Response({}, status=status.HTTP_201_CREATED) #empty dictionary bc not wanting to do with anything with the data thats sent back
            except Exception as ex:
                #if anything goes wrong with that try, respond with what is at the zero index 
                return Response({'message': ex.args[0]})
            # if its a delete request, delete the gamer from the attendees list
        elif request.method == "DELETE":
            try:
            #if the delete request is successful, send a 204_no_content response, which will return nothing other than the status
                project_note.projects.remove(project_note)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                #if that doesnt work, send the response at the zero index
                return Response({'message': ex.args[0]})

""" class NoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Note
        fields = '__all__' """

class ProjectUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

""" class ProjectSuperSerializer(serializers.ModelSerializer):
    
    user = ProjectUserSerializer(many=False)

    class Meta:
        model = Super
        fields = ['user'] """

class ProjectNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectNote
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    project_notes = ProjectNoteSerializer(many=True)
    #super = ProjectSuperSerializer(many=False)
    class Meta:
        model = Project
        fields = '__all__'
        # depth = 2

class LotSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Lot
        fields = '__all__'
