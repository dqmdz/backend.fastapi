from tortoise.expressions import Q
from app.models import Product, Sale

async def get_product(product_id: int):
    return await Product.get_or_none(id=product_id)

async def get_products(skip: int = 0, limit: int = 100):
    return await Product.all().offset(skip).limit(limit)

async def create_product(product: dict):
    return await Product.create(**product)

async def update_product(product_id: int, product: dict):
    await Product.filter(id=product_id).update(**product)
    return await get_product(product_id)

async def delete_product(product_id: int):
    deleted_count = await Product.filter(id=product_id).delete()
    return deleted_count > 0

async def get_sale(sale_id: int):
    return await Sale.get_or_none(id=sale_id).prefetch_related("product")

async def get_sales(skip: int = 0, limit: int = 100):
    return await Sale.all().offset(skip).limit(limit).prefetch_related("product")

async def create_sale(sale: dict):
    sale_obj = await Sale.create(**sale)
    await sale_obj.fetch_related("product")
    return sale_obj

async def update_sale(sale_id: int, sale: dict):
    await Sale.filter(id=sale_id).update(**sale)
    sale_obj = await get_sale(sale_id)
    if sale_obj:
        await sale_obj.fetch_related("product")
    return sale_obj

async def delete_sale(sale_id: int):
    deleted_count = await Sale.filter(id=sale_id).delete()
    return deleted_count > 0