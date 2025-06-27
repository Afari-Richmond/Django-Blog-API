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


class LoginView(APIView):    # Define The Login View Inside the API View Class
    def post(self, request):  # Define a POST request because user will be entering data

        try:
            data = request.data                  # store the data from the user in data
            # pass the data into the login serializer and store it in the serializer variable
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():  # validates if the data is correct or not using the serializer defined
                return Response({
                    'data': serializer.errors,
                    'message': 'Something Went Wrong'
                }, status=status.HTTP_400_BAD_REQUEST)  # if it's not, it returns an error message

            response = serializer.get_jwt_token(
                serializer.data)  # if yes, it creates a JWT Token
            # and returns a success message
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:  # catch unexpeted errors
            print(e)
            return Response({
                'data': {},
                'message': 'Something Went Wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
