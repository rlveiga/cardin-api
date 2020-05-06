import json

from app.models.card import Card, CardAssociation
from app.models.collection import Collection


def test_get_collection_info(test_client, init_db, token):
    collection = Collection.query.filter_by(created_by=1).first()

    response = test_client.get(
        f"/collections/{collection.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['collection']['name'] == 'Minhas cartas'
    assert type(data['collection']['cards']) is list


def test_get_unexisting_collection_info(test_client, init_db, token):
    response = test_client.get(
        '/collections/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Collection not found'


def test_get_unauthorized_collection_info(test_client, init_db, token):
    collection = Collection.query.filter_by(created_by=2).first()

    response = test_client.get(
        f"/collections/{collection.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this collection'


def test_create_owned_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(name='collection_1', created_by=2).first()

    response = test_client.post(f"/owned_collections/{collection.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 201

    assert data['data']['name'] == 'collection_1'
    assert data['data']['created_by'] == 2

def test_create_already_owned_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(name='collection_1', created_by=2).first()

    response = test_client.post(f"/owned_collections/{collection.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 422

    assert data['message'] == 'You already own this collection'

def test_create_owned_collection_unexisting(test_client, init_db, token):
    response = test_client.post(f"/owned_collections/42", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Collection not found'

def test_create_collection(test_client, init_db, token):
    response = test_client.post(
        '/collections/', json=dict(name='Random collection'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 201

    assert type(data['collection']) == dict
    assert data['collection']['data']['name'] == 'Random collection'
    assert type(data['collection']['cards']) == list


def test_add_to_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(
        name='Random collection', created_by=1).first()
    card = Card.query.filter_by(created_by=1).first()

    response = test_client.post(
        f"/collections/{collection.id}/add_card/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Card added to collection'
    assert data['collection']['cards'][0]['name'] == 'card_1'


def test_add_to_collection_again(test_client, init_db, token):
    collection = Collection.query.filter_by(
        name='Random collection', created_by=1).first()
    card = Card.query.filter_by(created_by=1).first()

    response = test_client.post(
        f"/collections/{collection.id}/add_card/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 409

    assert data['message'] == 'Card already belongs to this collection'


def test_add_to_unexisting_collection(test_client, init_db, token):
    card = Card.query.filter_by(created_by=1).first()

    response = test_client.post(
        f"/collections/42/add_card/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Collection not found'


def test_add_unexisting_card_to_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(created_by=1).first()

    response = test_client.post(
        f"/collections/{collection.id}/add_card/420000", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Card not found'


def test_add_unauthorized_card_to_collection(test_client, init_db, token):
    card = Card.query.filter_by(created_by=2).first()
    collection = Collection.query.filter_by(created_by=1).first()

    response = test_client.post(
        f"/collections/{collection.id}/add_card/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this card'


def test_add_to_unauthorized_collection(test_client, init_db, token):
    card = Card.query.filter_by(created_by=1).first()
    collection = Collection.query.filter_by(created_by=2).first()

    response = test_client.post(
        f"/collections/{collection.id}/add_card/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this collection'


def test_remove_from_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(
        name='Random collection', created_by=1).first()
    card = Card.query.filter_by(created_by=1).first()

    response = test_client.delete(
        f"/collections/{collection.id}/remove_card/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Card removed from collection'


def test_remove_from_collection_again(test_client, init_db, token):
    collection = Collection.query.filter_by(
        name='Random collection', created_by=1).first()
    card = Card.query.filter_by(created_by=1).first()

    response = test_client.delete(
        f"/collections/{collection.id}/remove_card/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Card does not belong to this collection'

def test_remove_from_unexisting_collection(test_client, init_db, token):
    card = Card.query.filter_by(created_by=1).first()

    response = test_client.delete(
        f"/collections/{42}/remove_card/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Collection not found'

def test_remove_unexisting_card_from_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(
        name='Random collection', created_by=1).first()

    response = test_client.delete(
        f"/collections/{collection.id}/remove_card/420000", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Card not found'

def test_remove_unauthorized_card_from_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(
        name='Random collection', created_by=1).first()
    card = Card.query.filter_by(created_by=2).first()

    response = test_client.delete(
        f"/collections/{collection.id}/remove_card/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this card'

def test_remove_from_unauthorized_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(created_by=2).first()
    card = Card.query.filter_by(created_by=1).first()

    response = test_client.delete(
        f"/collections/{collection.id}/remove_card/{card.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this collection'


def test_delete_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(
        name='Random collection', created_by=1).first()

    response = test_client.delete(
        f"/collections/{collection.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Collection deleted'
    assert data['collection'] == {}


def test_delete_unexisting_collection(test_client, init_db, token):
    response = test_client.delete(
        '/collections/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Collection not found'


def test_delete_unauthorized_collection(test_client, init_db, token):
    collection = Collection.query.filter_by(created_by=2).first()

    response = test_client.delete(
        f"/collections/{collection.id}", headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 401

    assert data['message'] == 'You do not own this collection'
