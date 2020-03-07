from app.models.collection import OwnedCollections

def user_owns_collection(user_id, collection_id):
  collection = OwnedCollections.query.filter_by(user_id=user_id, collection_id=collection_id).first()

  if collection is None:
    return False

  return True