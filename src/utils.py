
import streamlit as st
import pandas as pd
import uuid
import sqlite3
from PIL import Image
import io
import os

# --- SQLite Configuration ---
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/products.db')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '../data/images')
os.makedirs(IMAGES_DIR, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10.0)
    conn.row_factory = sqlite3.Row
    # Enable foreign key constraints for data integrity
    conn.execute("PRAGMA foreign_keys = ON")
    # Set secure file permissions on database file
    try:
        os.chmod(DB_PATH, 0o600)  # Owner read/write only
    except (OSError, FileNotFoundError):
        pass  # File might not exist yet
    return conn

# --- Initialize DB if not exists ---
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        mould_no TEXT,
        description TEXT,
        image_url TEXT,
        location TEXT,
        hook TEXT,
        cavaties INTEGER,
        part_wt REAL,
        short_wt REAL
    )''')
    conn.commit()
    conn.close()
init_db()



# Function to load data from SQLite
@st.cache_data(ttl=3600)
def load_data():
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM products", conn)
        conn.close()
        expected_cols = ['id', 'mould_no', 'description', 'image_url', 'location', 'hook', 'cavaties', 'part_wt', 'short_wt']
        for col in expected_cols:
            if col not in df.columns:
                df[col] = ''
        df = df[expected_cols]
        return df
    except Exception as e:
        st.error(f"Error loading data from SQLite: {e}.")
        return pd.DataFrame(columns=['id', 'mould_no', 'description', 'image_url', 'location', 'hook', 'cavaties', 'part_wt', 'short_wt'])


# Function to add a product to SQLite
def add_product_to_db(product_data: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO products (id, mould_no, description, image_url, location, hook, cavaties, part_wt, short_wt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                product_data['id'],
                product_data['mould_no'],
                product_data['description'],
                product_data['image_url'],
                product_data['location'],
                product_data['hook'],
                product_data['cavaties'],
                product_data['part_wt'],
                product_data['short_wt']
            )
        )
        conn.commit()
        conn.close()
        st.cache_data.clear()
        return True
    except sqlite3.IntegrityError:
        st.error("Product ID already exists.")
        return False
    except Exception as e:
        st.error(f"Error adding product to SQLite: {e}")
        return False


# Function to delete a product from SQLite
def delete_product_from_db(product_id: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error deleting product from SQLite: {e}")
        return False


# Function to update a product in SQLite
def update_product_in_db(product_id: str, product_data: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''UPDATE products SET mould_no=?, description=?, image_url=?, location=?, hook=?, cavaties=?, part_wt=?, short_wt=? WHERE id=?''',
            (
                product_data['mould_no'],
                product_data['description'],
                product_data['image_url'],
                product_data['location'],
                product_data['hook'],
                product_data['cavaties'],
                product_data['part_wt'],
                product_data['short_wt'],
                product_id
            )
        )
        conn.commit()
        conn.close()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error updating product in SQLite: {e}")
        return False


# Function to get a single product from SQLite
def get_product_by_id(product_id: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching product from SQLite: {e}")
        return None



# Helper Function to Resize Image
def resize_image(image_bytes, size=(200, 200)):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
        image = image.resize(size)
        return image
    except Exception as e:
        st.error(f"Error resizing image: {e}")
        return None



# Upload Function: Save image locally and return relative path
def upload_image_to_local(uploaded_file, product_id):
    if uploaded_file is None:
        return ""
    
    # Sanitize product_id to prevent path traversal
    import re
    safe_product_id = re.sub(r'[^a-zA-Z0-9_-]', '_', str(product_id))
    if not safe_product_id or len(safe_product_id) > 50:
        st.error("Invalid product ID for file naming.")
        return ""
    
    image_bytes = uploaded_file.getvalue()
    
    # Validate file size (max 5MB)
    if len(image_bytes) > 5 * 1024 * 1024:
        st.error("Image file too large. Maximum size is 5MB.")
        return ""
    
    resized_image_obj = resize_image(image_bytes)
    if resized_image_obj is None:
        st.error("Failed to resize image, upload cancelled.")
        return ""
    
    unique_filename = f"{safe_product_id}-{uuid.uuid4()}.jpg"
    image_path = os.path.join(IMAGES_DIR, unique_filename)
    
    # Ensure the path is within the images directory (prevent path traversal)
    image_path = os.path.abspath(image_path)
    images_dir_abs = os.path.abspath(IMAGES_DIR)
    if not image_path.startswith(images_dir_abs):
        st.error("Invalid file path detected.")
        return ""
    
    try:
        resized_image_obj.save(image_path, format="JPEG")
        st.success("Image uploaded successfully!")
        # Return relative path for use in image_url
        return os.path.relpath(image_path, os.path.dirname(__file__))
    except Exception as e:
        st.error(f"Error saving image locally: {e}")
        return ""
    

