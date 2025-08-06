from sqlalchemy.inspection import inspect
from forms.product_form import AddProductForm
import os
from utils.utils import allowed_file
from werkzeug.utils import secure_filename
from core.database import db
from core.configs import UPLOAD_FOLDER,logger
from models.products import Products
import json

def add_new_product(form: AddProductForm):
    image_paths = []

    for file in form.images.data:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            image_paths.append(f'/uploads/{filename}')  # Relative path

    model_columns = {c.key for c in inspect(Products).mapper.column_attrs}  # type: ignore

    # Filter form data to only include model columns
    filtered_data = {key: value for key, value in form.data.items() if key in model_columns}

    # Store images as JSON string or comma-separated string (depending on your DB column type)
    filtered_data['images'] = json.dumps(image_paths)  # <-- This fixes the error

    new_product = Products(**filtered_data)
    db.session.add(new_product)
    db.session.commit()
    logger.info(f"Product {new_product.name} added successfully")
    return new_product


def get_products_by_category(category:str):
    products = db.session.execute(db.select(Products).where(Products.category==category))
    return products.scalars().all()