from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user_app.serializers import UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user_serilizer = UserSerializer(self.user).data
        data["user"] = user_serilizer
        return data
