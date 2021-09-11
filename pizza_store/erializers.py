from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Pizzeria, PizzaImage

UserModel = get_user_model()


class PizzeriaListSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Pizzeria
        fields = ('id', 'pizzeria_name', 'city', 'state', 'description', 'logo_image',
                  'is_active', 'email', 'absolute_url')

    def get_absolute_url(self, obj):
        return reverse('pizza_details', args=(obj.pk,))


class ImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PizzaImage
        fields = ('id', 'image', 'image_title', 'uploaded_at')


class PizzeriaDetailsSerializer(serializers.ModelSerializer):
    update = serializers.SerializerMethodField()
    delete = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Pizzeria
        fields = ('pizzeria_name', 'city', 'phone_number', 'state',
                  'description', 'is_active', 'email', 'update', 'delete', 'images')

    def get_update(self, obj):
        return reverse('pizza_update', args=(obj.pk,))

    def get_delete(self, obj):
        return reverse('pizza_delete', args=(obj.pk,))


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'password']

    def create(self, validated_data):
        user = UserModel.objects.create(username=validated_data.get('username'))
        user.set_password(validated_data.get('password'))
        user.save()
        new_token = Token.objects.create(user=user)
        return user
