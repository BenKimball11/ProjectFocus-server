"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from projectFocusapi.models import Lot, Project, Super, Note


class LotView(ViewSet):

    def create(self, request):
        """[summary]
        Args:
            request ([type]): [description]
        Returns:
            [type]: [description]
        """
        super = Super.objects.get(user=request.auth.user)
        project = Project.objects.get(pk=request.data['project'])
        note = Note.objects.get(pk=request.data['note'])
        try:
            lot = Lot.objects.create(
                lotSize=request.data['lotSize'],
                lotNumber=request.data['lotNumber'],
                note=note,
                project=project,
                super=super
            )
            serializer = LotSerializer(lot, context={'request': request})
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
        lot.note = Note.objects.get(pk=request.data['note'])
        project = Project.objects.get(pk=request.data['project'])
        lot.project = project

        lot.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        lots = Lot.objects.all()

        project = request.query_params.get('type', None)

        if project is not None:
            lots = lots.filter(project__id=project)

        serializer = LotSerializer(
            lots, many=True, context={'request': request})

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


class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = '__all__'
        # depth = 2