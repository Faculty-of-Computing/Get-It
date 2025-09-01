from sqlalchemy.inspection import inspect
from forms.product_form import AddProductForm
import os
from utils.utils import allowed_file
from werkzeug.utils import secure_filename
from core.database import db
from core.configs import logger
from models.products import Products
import json
import cloudinary.uploader

def add_new_product(form: AddProductForm):
    image_paths = []

    for file in form.images.data:
        if file and allowed_file(file.filename):
            #NOTE - This is uploading to a cloud container called CLoudinary and fetching the secure url after for rendering
            try:
                # Upload the file to Cloudinary. 
                # The 'file' object from Flask-WTF is directly usable.
                upload_result = cloudinary.uploader.upload(
                    file,
                    # You can add options here, e.g., a folder to store images
                    folder=f"products/{form.category.data}" #This specifies product upload
                )
                
                # The response from Cloudinary contains the URL
                image_paths.append(upload_result['secure_url'])
                logger.info(f"Successfully uploaded {file.filename} to Cloudinary.")

            except Exception as e:
                # If an upload fails, log the error and skip the file
                logger.error(f"Error uploading {file.filename} to Cloudinary: {e}")
                continue # Move to the next file
            
    if not image_paths:
        logger.error("All image uploads failed for the new product.")
        # Raise an exception to prevent creating a product without images.
        raise ValueError("Image upload failed. Could not create the product.")

    model_columns = {c.key for c in inspect(Products).mapper.column_attrs}  # type: ignore

    # Filter form data to only include model columns
    filtered_data = {key: value for key, value in form.data.items() if key in model_columns}

    # Store images as JSON string or comma-separated string (depending on your DB column type)
    filtered_data['images'] = image_paths

    new_product = Products(**filtered_data) #NOTE -Unpack filetered data into the products u
    db.session.add(new_product)
    db.session.commit()
    logger.info(f"Product {new_product.name} added successfully")
    return new_product


def get_products_by_category(category:str):
    products = db.session.execute(db.select(Products).where(Products.category==category))
    return products.scalars().all()