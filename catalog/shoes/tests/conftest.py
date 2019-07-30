import pytest


@pytest.fixture
def shoes_payload():
    return {
        "sku": "3487-1230912",
        "brand": "adidas",
        "model": "airflow",
        "price": "190.00",
        "description": "Lançamento mundial da Adidas",
        "main_color": "black",
        "style": "casual",
        "size": 38,
        "external_material": "sintetico",
        "internal_material": "sintetico",
        "sole_material": "borracha",
        "weight": "1.000",
        "height": "2.000",
        "width": "1.000",
        "length": "1.000",
        "stock": 33
    }


@pytest.fixture
def shoes_payload_invalid():
    return {
        "sku": "3487-1230912",
        "brand": "adidas",
        "model": "airflow",
        "price": "190.00",
        "description": "Lançamento mundial da Adidas",
        "main_color": "black",
        "style": "casual",
        "size": 88,
        "external_material": "sintetico",
        "internal_material": "sintetico",
        "sole_material": "borracha",
        "weight": "1.000",
        "height": "2.000",
        "width": "1.000",
        "length": "1.000",
        "stock": 33
    }


@pytest.fixture
def shoes_payload_partial():
    return {
        "price": "190.00",
        "stock": 33
    }
