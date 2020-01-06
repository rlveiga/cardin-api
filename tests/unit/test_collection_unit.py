from app.models.collection import Collection

def test_remove_from_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(id=1).one()

    assert len(collection.cards) == 2

    collection.remove_card(collection.cards[0])

    assert collection.cards.length == 0