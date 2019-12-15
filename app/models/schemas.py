from app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

user_share_schema = UserSchema()
users_share_schema = UserSchema(many=True)

class RoomSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'code')

room_share_schema = RoomSchema()