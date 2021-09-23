"""View module for handling requests about games"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from projectFocusapi.models import Lot, Project, Super, ProjectNote, LotNote
#from django.contrib.auth.models import User #pylint:disable=imported-auth-user


class LotView(ViewSet):

    def create(self, request):
        """[summary]
        Args:
            request ([type]): [description]
        Returns:
            [type]: [description]
        """
        super = Super.objects.get(user=request.auth.user)
        lot = Lot()
        lot.lotSize = request.data['lotSize']
        lot.lotNumber=request.data['lotNumber']
        lot.super = super


        try:
            lot.save()
            serializer = LotSerializer(lot, context={'request': request}) #converting data into json
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            lot = Lot.objects.get(pk=pk)
            serializer = LotSerializer(lot, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):
        lot = Lot.objects.get(pk=pk)
        lot.lotSize = request.data['lotSize']
        lot.lotNumber = request.data['lotNumber']

        lot.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):

        super = Super.objects.get(user=request.auth.user)

        lots = Lot.objects.filter(super=super)
        """ if super is not None:
            lots = lots.filter(user=super.user) """ 


        serializer = LotSerializer(lots, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            lot = Lot.objects.get(pk=pk)
            lot.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Lot.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    @action(methods=['post', 'delete'], detail=True)
    #detail=true will add a Primary key to the url
    #will take the name of the method and turn it into the route we can go to because that is the method name.
    def add_note(self, request, pk):
        #get the gamer, taking the token and matching it from the front end
        lot_note = LotNote.objects.get(user=request.auth.user)
        #try block here to try and get the event, if that doesnt work because the event doesnt exist
        #it will go the except block and respond with the message and return the 404_not_found error
        try:
            lot_note = LotNote.objects.get(pk=pk)
        except LotNote.DoesNotExist:
            return Response(
            {'message': 'Event does not exist.'},
            status=status.HTTP_404_NOT_FOUND
        )
        #if the method we are using is post, then add the gamer to the attendees list. by using add and passing the gamer to it
        if request.method == "POST":
            try:
                lot_note.lots.add(lot_note)
                #if that works, send the 201 created status
                return Response({}, status=status.HTTP_201_CREATED) #empty dictionary bc not wanting to do with anything with the data thats sent back
            except Exception as ex:
                #if anything goes wrong with that try, respond with what is at the zero index 
                return Response({'message': ex.args[0]})
            # if its a delete request, delete the gamer from the attendees list
        elif request.method == "DELETE":
            try:
            #if the delete request is successful, send a 204_no_content response, which will return nothing other than the status
                lot_note.lots.remove(lot_note)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                #if that doesnt work, send the response at the zero index
                return Response({'message': ex.args[0]})



""" class LotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']        
 """
class LotSuperSerializer(serializers.ModelSerializer):
    
    #user = LotUserSerializer(many=False)

    class Meta:
        model = Super
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Project
        fields = '__all__'

""" class LotNoteSerializer(serializers.ModelSerializer):
    note = NoteSerializer(many=False)

    class Meta:
        model = LotNote
        fields = '__all__' """ 

class LotNoteSerializer(serializers.ModelSerializer):
    #lotId = LotSerializer(many=False)
    class Meta:
        model = LotNote
        fields = '__all__'

class LotSerializer(serializers.ModelSerializer):
    lot_projects = ProjectSerializer(many=True)
    lot_lot_notes = LotNoteSerializer(many=True)
    super = LotSuperSerializer(many=False)
    class Meta:
        model = Lot
        fields = '__all__'
        # depth = 2

