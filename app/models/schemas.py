from app import ma

class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'card_type', 'created_by', 'slots')

card_share_schema = CardSchema()
cards_share_schema = CardSchema(many=True)

class CollectionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'created_at', 'created_by', 'editable', 'white_card_count', 'black_card_count')

collection_share_schema = CollectionSchema()
collections_share_schema = CollectionSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'username', 'profile_img', 'profile_color', 'source')

user_share_schema = UserSchema()
users_share_schema = UserSchema(many=True)

class RoomSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'status', 'code', 'created_at', 'created_by', 'user_list')

room_share_schema = RoomSchema()