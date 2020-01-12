from app import ma

class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'card_type')

card_share_schema = CardSchema()
cards_share_schema = CardSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')

user_share_schema = UserSchema()
users_share_schema = UserSchema(many=True)

class RoomSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'status', 'code', 'created_at','created_by', 'data')

room_share_schema = RoomSchema()