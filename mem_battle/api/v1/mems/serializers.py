from django.conf import settings
from rest_framework import serializers

from apps.mems.models import Comment, Mem, Tag


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ('id', 'owner', 'text', 'parent')


class MemsListSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes_count

    def get_dislikes_count(self, obj):
        return obj.dislikes_count

    def get_comments_count(self, obj):
        return obj.com_count


    class Meta:
        model = Mem
        fields = (
            'id',
            'image',
            'owner',
            'created_at',
            'comments_count',
            'likes_count',
            'dislikes_count',
            'vote_score',
            'tags',
        )


class MemRetriveSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    likes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="username"
    )
    dislikes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Mem
        fields = (
            'id',
            'image',
            'owner',
            'created_at',
            'tags',
            'likes',
            'dislikes',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class MemCreateUpdateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(required=False)
    image = serializers.ImageField()
    # image = serializers.ListField()
    bad_tags = settings.BAD_TAGS

    class Meta:
        model = Mem
        fields = (
            'owner',
            'image',
            'tags',
        )

    def make_tags_list(self, tags):
        return [tag.strip().lower() for tag in tags['name'].split(',')]

    def get_or_create_tag(self, tag):
        if tag not in self.bad_tags:
            if not Tag.objects.filter(name=tag).exists():
                Tag.objects.create(name=tag)
            t = Tag.objects.get(name=tag)
            return t

    def create(self, validated_data):

        tags = validated_data.pop('tags')
        list_tags = self.make_tags_list(tags)
        mem = Mem.objects.create(**validated_data)
        #проходимся по списку картинок, в каждую картинку добавляем теги
        #validate len of list of images
        for tag in list_tags:
            t = self.get_or_create_tag(tag)
            mem.tags.add(t)
        return mem

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        list_tags = self.make_tags_list(tags)
        instance.tags.clear()
        instance.save()
        for tag in list_tags:
            t = self.get_or_create_tag(tag)
            instance.tags.add(t)
        return instance


class MemDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mem
        fields = ('id',)

