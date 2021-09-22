from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from projectFocusapi.models import Lot, Note, LotNote

class LotNoteView(ViewSet):


    def create(self, request):
        lotNote = LotNote()
        lotNote.lot = Lot.objects.get(pk=request.data["lot"])
        lotNote.note = Note.objects.get(pk=request.data["note"])

        try:
            lotNote.save()
            serializer = LotNoteSerializer(lotNote, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        lotNote = LotNote.objects.get(pk=pk)
        lotNote.lot = Lot.objects.get(pk=request.data["lot"])
        lotNote.note = Note.objects.get(pk=request.data["note"])
        lotNote.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


        return Response(lotnote)

    def destroy(self, request, pk=None):
        try:
            lotNote = LotNote.objects.get(pk=pk)
            lotNote.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
            lot = self.request.query_params.get('lot', None)
            if lot is not None:
                lotNotes = LotNote.objects.filter(lot__id=lot)
            else:
                note = self.request.query_params.get('note', None)
                if note is not None:
                    lotNotes = LotNote.objects.filter(note__id=note)
                else:
                    lotNotes = LotNote.objects.all()

            serializer = LotNoteSerializer(
                lotNotes, many=True, context={'request': request}
            )
            return Response(serializer.data)

class LotSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    #user = UserSerializer(many=False)

    class Meta:
        model = Lot
        fields = '__all__'
class NoteSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    #user = UserSerializer(many=False)

    class Meta:
        model = Note
        fields = '__all__'


class LotNoteSerializer(serializers.ModelSerializer):
    lot = LotSerializer(many=False)
    note = NoteSerializer(many=False)
    class Meta:
        model = LotNote
        fields = '__all__'
