from rest_framework import serializers

from rest_auth.blog.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(many=False)

    class Meta:
        model = Blog
        fields= ('id', 'title', 'description', 'owner')
