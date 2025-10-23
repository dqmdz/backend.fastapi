from fastapi import APIRouter, HTTPException
from typing import List
from tortoise.exceptions import IntegrityError

from app import crud
from app.schemas import SaleSchema, SaleCreateSchema

router = APIRouter()
sale_schema = SaleSchema()
sales_schema = SaleSchema(many=True)
sale_create_schema = SaleCreateSchema()

@router.get("/", response_model=List[dict])
async def read_sales(skip: int = 0, limit: int = 100):
    sales = await crud.get_sales(skip=skip, limit=limit)
    return sales_schema.dump(sales)

@router.get("/{sale_id}", response_model=dict)
async def read_sale(sale_id: int):
    db_sale = await crud.get_sale(sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale_schema.dump(db_sale)

@router.post("/", response_model=dict)
async def create_sale(sale_data: dict):
    # Validate and deserialize input data
    data = sale_create_schema.load(sale_data)
    try:
        sale = await crud.create_sale(data)
        return sale_schema.dump(sale)
    except IntegrityError as e:
        if "FOREIGN KEY constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="Product with the specified product_id does not exist")
        raise HTTPException(status_code=400, detail="Database integrity error")

@router.put("/{sale_id}", response_model=dict)
async def update_sale(sale_id: int, sale_data: dict):
    # Validate and deserialize input data
    data = sale_create_schema.load(sale_data)
    db_sale = await crud.update_sale(sale_id=sale_id, sale=data)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale_schema.dump(db_sale)

@router.delete("/{sale_id}")
async def delete_sale(sale_id: int):
    success = await crud.delete_sale(sale_id=sale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {"message": "Sale deleted successfully"}