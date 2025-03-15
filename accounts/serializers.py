from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "sub_role",
            "is_active",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    sub_role = serializers.ChoiceField(
        choices=["ETUDIANT", "ENSEIGNANT", "ATS"], required=True
    )

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "sub_role"]

    def validate(self, data):
        email = data.get("email")
        sub_role = data.get("sub_role")

        if not email.endswith("@esi-sba.dz"):
            raise serializers.ValidationError(
                {
                    "email": "Seules les adresses email avec le domaine @esi-sba.dz sont autorisées."
                }
            )

        if sub_role not in ["ETUDIANT", "ENSEIGNANT", "ATS"]:
            raise serializers.ValidationError(
                {
                    "sub_role": "Le sous-role doit être 'ETUDIANT', 'ENSEIGNANT' ou 'ATS'."
                }
            )

        return data

    def create(self, validated_data):
        validated_data["role"] = "PATIENT"

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data["role"],
            sub_role=validated_data["sub_role"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("L'utilisateur n'existe pas.")

            if not user.is_active:
                raise serializers.ValidationError("Le compte utilisateur est inactif.")

            user = authenticate(email=email, password=password)
            if user:
                return user
            raise serializers.ValidationError("Identifiants incorrects.")
        raise serializers.ValidationError(
            "L'email et le mot de passe sont obligatoires."
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères."
            )
        return value

    def validate(self, data):

        user = self.context["request"].user
        if not user.check_password(data["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "Mot de passe actuel incorrect."}
            )
        return data

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        update_session_auth_hash(self.context["request"], user)
