
import string
import random
from datetime import datetime
from woocommerce import API
from ssqatest.src.helpers.config_helpers import get_api_credentials
from ssqatest.src.helpers.generic_helpers import generate_random_email_and_password


def create_api_object():
    api_creds = get_api_credentials()

    wcapi = API(
        url=api_creds['base_url'],
        consumer_key=api_creds['api_key'],
        consumer_secret=api_creds['api_secret'],
        version="wc/v3"
    )

    return wcapi

def create_user():
    api_obj = create_api_object()
    user_info = generate_random_email_and_password()

    create_customer_payload = {
        "email": user_info['email'],
        "password": user_info['password']

    }
    response = api_obj.post('customers', create_customer_payload)

    assert response.status_code == 201, f"Failed to create user. Response: {response.json()}"

    return user_info


def create_customer():
    """
    Creates a customer via WooCommerce API and returns id, email, password.
    Use when you need the customer id (e.g. to create an order for that customer).
    """
    api_obj = create_api_object()
    user_info = generate_random_email_and_password()
    payload = {"email": user_info["email"], "password": user_info["password"]}
    response = api_obj.post("customers", payload)
    assert response.status_code == 201, f"Failed to create customer. Response: {response.json()}"
    data = response.json()
    return {"id": data["id"], "email": user_info["email"], "password": user_info["password"]}


def create_order_for_customer(customer_id, product_id=None):
    """
    Creates one order for the given customer via WooCommerce API (status=completed so it appears in My Account).
    :param customer_id: WooCommerce customer ID (int).
    :param product_id: Product to add to the order; if None, uses first available product (e.g. beanie).
    :return: Created order dict from API.
    """
    api_obj = create_api_object()
    if product_id is None:
        product = get_product_by_slug("beanie")
        product_id = product["id"]
    payload = {
        "customer_id": int(customer_id),
        "line_items": [{"product_id": int(product_id), "quantity": 1}],
        "status": "completed",
    }
    response = api_obj.post("orders", payload)
    assert response.status_code == 201, (
        f"Failed to create order for customer {customer_id}. "
        f"Status: {response.status_code}. Response: {response.text}"
    )
    return response.json()


def create_coupon(coupon_code=None, length=7, expired=False):

    if expired:
        expiration_date = datetime.now().isoformat()
    else:
        expiration_date = None

    if not coupon_code:
        coupon_code = ''.join(random.choice(string.ascii_uppercase) for i in range(length))

    payload = {
            "code": coupon_code,
            "discount_type": "percent",
            "amount": "100",
            "date_expires": expiration_date
        }

    api_obj = create_api_object()
    rs_api = api_obj.post('coupons', data=payload)
    assert rs_api.status_code == 201, f'Failed creating coupon. Status code {rs_api.status_code}. ' \
                                        f'Payload: {payload}. \n' \
                                        f'Response: {rs_api.json()}'

    return coupon_code

def get_coupon_info_by_coupon_code(coupon_code):
    api_obj = create_api_object()
    params = {'code': coupon_code}
    rs_api = api_obj.get('coupons', params=params)
    assert rs_api.status_code == 200, f"Failed getting coupon by coupon code: {coupon_code}"

    return rs_api.json()

def delete_coupon_by_coupon_code(coupon_code):
    api_obj = create_api_object()
    coupon_info = get_coupon_info_by_coupon_code(coupon_code)
    coupon_id = coupon_info[0]['id']
    rs_api = api_obj.delete(f"coupons/{coupon_id}", params={"force": True})
    assert rs_api.status_code == 200, f"Failed to delete coupon via api: coupon code: {coupon_code}"

def get_product_by_slug(slug):
    """
    Fetches a single product by slug from the WooCommerce API.
    Used as source-of-truth for PDP tests (name, images, SKU, etc.).
    :param slug: Product slug (e.g. 'beanie', 'hoodie').
    :return: Product dict from API.
    """
    api_obj = create_api_object()
    rs_api = api_obj.get('products', params={'slug': slug})
    assert rs_api.status_code == 200, (
        f"Failed to get product by slug '{slug}'. Status: {rs_api.status_code}. Response: {rs_api.text}"
    )
    products = rs_api.json()
    assert len(products) > 0, (
        f"No product found with slug '{slug}'. API returned empty list."
    )
    return products[0]


def update_product(product_id, data):
    """
    Updates a product via WooCommerce API (PUT).
    :param product_id: Product ID (int).
    :param data: Dict of fields to update (e.g. {"regular_price": "20", "sale_price": "18"}).
                 Use sale_price="" to remove sale.
    :return: Updated product dict from API.
    """
    api_obj = create_api_object()
    rs_api = api_obj.put(f"products/{product_id}", data)
    assert rs_api.status_code == 200, (
        f"Failed to update product {product_id}. Status: {rs_api.status_code}. Response: {rs_api.text}"
    )
    return rs_api.json()


def create_product_review(product_id, reviewer, review, rating, reviewer_email=None):
    """
    Creates a product review via WooCommerce REST API (wc/v3).
    :param product_id: Product ID (int).
    :param reviewer: Reviewer display name.
    :param review: Review content (text).
    :param rating: Star rating 1-5 (int).
    :param reviewer_email: Optional reviewer email (some stores require it).
    :return: Created review dict from API.
    """
    api_obj = create_api_object()
    payload = {
        "product_id": product_id,
        "reviewer": reviewer,
        "review": review,
        "rating": int(rating),
    }
    if reviewer_email:
        payload["reviewer_email"] = reviewer_email
    rs_api = api_obj.post("products/reviews", data=payload)
    assert rs_api.status_code == 201, (
        f"Failed to create review for product {product_id}. "
        f"Status: {rs_api.status_code}. Response: {rs_api.text}"
    )
    return rs_api.json()


def get_product_reviews(product_id):
    """
    Fetches all reviews for a product from the WooCommerce API.
    :param product_id: Product ID (int).
    :return: List of review dicts.
    """
    api_obj = create_api_object()
    rs_api = api_obj.get("products/reviews", params={"product": product_id, "per_page": 100})
    assert rs_api.status_code == 200, (
        f"Failed to get reviews for product {product_id}. Status: {rs_api.status_code}. Response: {rs_api.text}"
    )
    return rs_api.json()


def delete_product_review(review_id):
    """
    Deletes a product review via WooCommerce REST API (wc/v3).
    :param review_id: Review ID (int).
    :return: Response dict (typically {"deleted": true, "previous": {...}}).
    """
    api_obj = create_api_object()
    rs_api = api_obj.delete(f"products/reviews/{review_id}", params={"force": True})
    assert rs_api.status_code == 200, (
        f"Failed to delete review {review_id}. Status: {rs_api.status_code}. Response: {rs_api.text}"
    )
    return rs_api.json()


def get_random_products(qty=1, **kwargs):
    """
    Gets random products using the 'products' api.
    It calls the products api with the given parameters in **kwargs, randomly selects the given number of products
    from the response and returns it.
    List of available properties: https://woocommerce.github.io/woocommerce-rest-api-docs/#product-properties
    Example function calls:
        get_random_products(qty=1, status=private, type=variable)
        get_random_products(qty=1, downloadable=True)

    :param qty: number of products to return.
    :param kwargs:
    :return:
    """
    api_obj = create_api_object()

    kwargs['per_page'] = 100

    rs_api = api_obj.get('products', params=kwargs)
    products = rs_api.json()

    return random.sample(products, int(qty))
