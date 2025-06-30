from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from .models import Blog
from django.db.models import Q


class publicBlog(APIView):
    def get(self, request):
        try:
            
            blogs = Blog.objects.all().order_by('?')
         

            # checks if there's a query parameter named search  in the URL
            if request.GET.get('search'):
                # retrieves the actual value of search
                search = request.GET.get("search")
                # filters to check if the previously fetched
                blogs = blogs.filter(
                    Q(title_icontains=search) | Q(blogtext_icontains=search))
                # data has the title or body as the value in the search field

            page_number = request.GET.get('page', 1)
            paginator = paginator(blogs, 5)
            serializer = BlogSerializer(paginator.page(page_number), many= True)

            return Response({
                'data': serializer.data,
                'message': 'blogs fetched successfully'  # and return a success message

            }, status=status.HTTP_200_OK
            )

        except Exception as e:  # catch unexpeted errors
            print(e)
            return Response({
                'data': {},
                'message': 'Something Went Wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # query the database to get all blog posts where the user
            blogs = Blog.objects.filter(user=request.user)
            # field matches the currently logged user

            # checks if there's a query parameter named search  in the URL
            if request.GET.get('search'):
                # retrieves the actual value of search
                search = request.GET.get("search")
                # filters to check if the previously fetched
                blogs = blogs.filter(
                    Q(title_icontains=search) | Q(blogtext_icontains=search))
                # data has the title or body as the value in the search field

            serializer = BlogSerializer(blogs, many=True)

            return Response({
                'data': serializer.data,
                'message': 'blogs fetched successfully'  # and return a success message

            }, status=status.HTTP_200_OK
            )

        except Exception as e:  # catch unexpeted errors
            print(e)
            return Response({
                'data': {},
                'message': 'Something Went Wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

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

    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'invalid blog'
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': 'you are not authorized to do this'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = BlogSerializer(blog[0], data=data, partial=True)

            
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something Went Wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'blog updated successfully'  # and return a success message

            }, status=status.HTTP_201_CREATED)

        except Exception as e:  # catch unexpeted errors
            print(e)
            return Response({
                'data': {},
                'message': 'Something Went Wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'invalid blog'
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': 'you are not authorized to do this'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            blog[0].delete()
            return Response({
                'data': {},
                'message': 'blog deleted successfully'  # and return a success message

            }, status=status.HTTP_201_CREATED)
        except Exception as e:  # catch unexpeted errors
            print(e)
            return Response({
                'data': {},
                'message': 'Something Went Wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


            
