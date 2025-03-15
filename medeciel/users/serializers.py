from rest_framework import serializers
from .models import Profile



class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name' ,required=False)
    last_name = serializers.CharField(source='user.last_name' , required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image']

    def update(self, instance, validated_data):
        # تحديث بيانات المستخدم
        user_data = validated_data.pop('user', {})
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        # تحديث صورة البروفايل
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
