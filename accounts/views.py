from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status


class RegisterView(APIView):
    def post(self, request):
        try:  # a try exception block to handle errors
            data = request.data  # get the data from the user

            # create an instance of the register serializer class
            serializer = RegisterSerializer(data=data)

            if not serializer.is_valid():  # validates if the data meets the requirements of the serializer class
                return Response({
                    'data': serializer.errors,
                    'message': 'Something Went Wrong'
                }, status=status.HTTP_400_BAD_REQUEST)  # if not return an error message

            serializer.save()  # otherwise save the serializer created
            return Response({
                'data': {},
                'message': 'your account is created'  # and return a success message

            }, status=status.HTTP_201_CREATED)

        except Exception as e:  # catch unexpeted errors
            print(e)
            return Response({
                'data': {},
                'message': 'Something Went Wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):

        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something Went Wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            response = serializer.get_jwt_token(serializer.data)
            return Response(response, status=status.HTTP_200_OK)


        except Exception as e:  # catch unexpeted errors
            print(e)
            return Response({
                'data': {},
                'message': 'Something Went Wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
