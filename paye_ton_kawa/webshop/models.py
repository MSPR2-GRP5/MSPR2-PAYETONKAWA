from datetime import datetime


# https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object


class Customer(object):
    def __init__(
            self,
            customer_id: int,
            created_at: datetime,
            name: str,
            username: str,
            last_name: str,
            first_name: str,
            address: dict[str, str | int],
            profile: dict[str, str],
            company: dict[str, str],
    ):
        self.id = customer_id
        self.created_at = created_at
        self.name = name
        self.username = username
        self.last_name = last_name
        self.first_name = first_name
        self.address = address
        self.profile = profile
        self.company = company

    def __str__(self) -> str:
        return self.name


class Product:
    def __init__(
            self,
            id: int,
            name: str,
            description: str,
            import_location: str,
            price: int,
            stocks: int,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.import_location = import_location
        self.price = price
        self.stocks = stocks

    def __str__(self) -> str:
        return self.name


class Order:
    def __init__(
            self,
            id: int,
            customer_id: int,
            product_id: int,
            date: datetime,
            quantity: int,
            price: int,
    ):
        self.id = id
        self.client_id = customer_id
        self.product_id = product_id
        self.date = date
        self.quantity = quantity
        self.price = price

    def __str__(self) -> str:
        return "{0}: {1}, {2}".format(self.date, self.client_id, self.product_id)
