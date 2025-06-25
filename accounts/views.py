from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status


def registerView(APIView):
    def post(self, request):
        try:     #a try exception block to handle errors
            data = request.data #get the data from the user

            serializer = RegisterSerializer(data=data) #create an instance of the register serializer class

            if not serializer.is_valid(): #validates if the data meets the requirements of the serializer class
                return Response({
                    'data': serializer.errors,
                    'message': 'Something Went Wrong'
                }, status=status.HTTP_400_BAD_REQUEST) # if not return an error message 

            serializer.save() #otherwise save the serializer created
            return Response({
                'data': {},
                'message': 'your account is created' #and return a success message

            }, status=status.HTTP_201_CREATED)

        except Exception as e: #catch unexpeted errors
            return Response({
                'data': {},
                'message': 'Something Went Wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
