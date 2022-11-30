from django.urls import reverse


def test_products_list(login_user, product_factory, faker):
    client, user = login_user
    response = client.get(reverse('products'))
    assert response.status_code == 200
    assert not response.context['object_list']

    product = product_factory()
    response = client.get(reverse('products'))
    assert response.status_code == 200
    assert len(response.context['object_list']) == 3

    response = client.get(reverse('product_detail', args=(faker.uuid4(),)))
    assert response.status_code == 404

    response = client.get(reverse('product_detail', args=(str(product.id),)))
    assert response.status_code == 200
