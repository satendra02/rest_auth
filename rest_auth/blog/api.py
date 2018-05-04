from rest_framework import viewsets, status

from rest_auth.blog import error_codes
from rest_auth.blog.models import Blog
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_auth.blog.serializers import BlogSerializer
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication


class BlogListViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (OAuth2Authentication,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_object(self, pk):
        return Blog.objects.get(pk=pk)

    def retrieve(self, request, pk=None):
        try:
            blog = self.get_object(pk)
            serializer = BlogSerializer(blog)
            return Response(serializer.data)
        except Blog.DoesNotExist:
            return Response(error_codes.HTTP_BLOGS_NOT_AVAILABLE, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(error_codes.parse_exception(e, error_codes.G_EXCEPTION), status=status.HTTP_404_NOT_FOUND)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = BlogSerializer

    def get_object(self, pk):
        return Blog.objects.get(pk=pk)

    def create(self, request):
        try:
            title = request.data['title']
            description = request.data['description']
            owner = request.user
            blog = Blog.objects.create(title=title, description=description,
                                       owner=owner)
            serializer = self.serializer_class(blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Blog.DoesNotExist:
            return Response(error_codes.HTTP_BLOG_NOT_AVAILABLE, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(error_codes.parse_exception(e, error_codes.G_EXCEPTION), status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        try:
            instance = self.get_object(pk)
            user = request.user
            if user == instance.owner:
                self.perform_destroy(instance)
                return Response({'message': "Blog has been deleted", 'status': status.HTTP_201_CREATED})
            else:
                return Response({"message": "only owner can delete the rest_auth", "status": status.HTTP_401_UNAUTHORIZED})
        except Blog.DoesNotExist:
            return Response(error_codes.HTTP_BLOG_NOT_AVAILABLE, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        try:
            instance = self.get_object(pk)
            if request.user == instance.owner:
                instance.title = request.data['title']
                instance.description = request.data['description']
                instance.save()
                serializer = BlogSerializer(instance)
                return Response(serializer.data)
            else:
                return Response({"message": "only owner can update the rest_auth", "status": status.HTTP_401_UNAUTHORIZED})
        except Blog.DoesNotExist:
            return Response(error_codes.HTTP_BLOG_NOT_AVAILABLE, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(error_codes.parse_exception(e, error_codes.G_EXCEPTION), status=status.HTTP_404_NOT_FOUND)

