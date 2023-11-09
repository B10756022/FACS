from rest_framework import serializers
from .models import Video, Order,Customer
from django.contrib.auth.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'

    def save(self, **kwargs):
        vid_model = Customer(
            user=kwargs['user'],
            **self.validated_data
        )
        vid_model.save()

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def save(self, **kwargs):
        vid_model = Order(
            user=kwargs['user'],
            **self.validated_data
        )
        vid_model.save()


class VideoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Video
        # fields = ['id','title','author']
        fields = '__all__'

    def save(self, **kwargs):

        vid_model = Video(
            user=kwargs['user'],
            **self.validated_data
        )
        vid_model.save()



# class VideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Video
#         fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Video
        fields = ('caption','video','user')
    def save(self, **kwargs):

        vid_model = Video(
            user=kwargs['user'],
            **self.validated_data
        )
        vid_model.save()
