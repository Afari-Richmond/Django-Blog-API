from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id  


            serializer = BlogSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something Went Wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'blog created successfully'  # and return a success message

            }, status=status.HTTP_201_CREATED)

        except Exception as e:  # catch unexpeted errors
            print(e)
            return Response({
                'data': {},
                'message': 'Something Went Wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
