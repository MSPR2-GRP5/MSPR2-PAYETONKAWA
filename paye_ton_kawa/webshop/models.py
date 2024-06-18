from datetime import datetime
# https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object


class Clients:
    def __init__(self, id: int, last_name: str, first_name: str, address: str):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.address = address

    def __str__(self) -> str:
        return "{0} {1}".format(self.first_name, self.last_name)


class Products:
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


class Command:
    def __init__(
        self,
        id: int,
        client_id: int,
        product_id: int,
        date: datetime,
        quantity: int,
        price: int,
    ):
        self.id = id
        self.client_id = client_id
        self.product_id = product_id
        self.date = date
        self.quantity = quantity
        self.price = price

    def __str__(self) -> str:
        return "{0}: {1}, {2}".format(self.date, self.client_id, self.product_id)
