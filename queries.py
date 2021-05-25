create_products_table = """
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    );
    """

create_offers_table = """
    CREATE TABLE IF NOT EXISTS offers(
        product_id INTEGER,
        id INTEGER PRIMARY KEY,
        price INTEGER,
        items_in_stock INTEGER,
        FOREIGN KEY(product_id) REFERENCES products(id)
        );
    """

create_offers_history_table = """
    CREATE TABLE IF NOT EXISTS offers_history(
        product_id INTEGER,
        offer_id INTEGER,
        price INTEGER,
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(product_id) REFERENCES offers(product_id),
        FOREIGN KEY(offer_id) REFERENCES offers(id)
        );
    """ 

def create_products(name, description):
    create_product = f"""
    INSERT INTO
      products (name, description)
    VALUES
      ('{name}', '{description}');
    """
    return create_product

def read_products(id):
    read_product = f"""
    SELECT *
    FROM products
    WHERE id={id};
    """
    return read_product

def update_products_name(id, name):
    update_product_name = f"""
    UPDATE products
    SET name='{name}'
    WHERE id={id};
    """
    return update_product_name

def update_products_description(id, description):
    update_product_desc = f"""
    UPDATE products
    SET name='{description}'
    WHERE id={id};
    """
    return update_product_desc

def delete_products(id):
    delete_product = f"""
    DELETE FROM products
    WHERE id={id};
    """
    return delete_product

def read_offers(id):
    read_offer = f"""
    SELECT *
    FROM offers
    WHERE id={id};
    """
    return read_offer
