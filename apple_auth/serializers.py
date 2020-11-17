from rest_framework import serializers

from apple_auth.models import AppleCredentials, NameComponents


class NameComponentsSerializer(serializers.Serializer):
    namePrefix = serializers.CharField(required=False)
    givenName = serializers.CharField(required=False)
    middleName = serializers.CharField(required=False)
    familyName = serializers.CharField(required=False)
    nameSuffix = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False)


class AppleSignInSerializer(serializers.Serializer):
    token = serializers.CharField()
    name = NameComponentsSerializer(required=False)

    def create(self, validated_data):
        credentials = AppleCredentials(**validated_data)
        if name_data := validated_data.pop('name', None):
            credentials.name = NameComponents(**name_data)

        return credentials
