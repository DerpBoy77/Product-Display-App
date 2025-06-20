import streamlit as st
import pandas as pd
import uuid
from supabase import create_client, Client
from PIL import Image
import io

# --- Supabase Configuration (from .streamlit/secrets.toml) ---
try:
    SUPABASE_URL = st.secrets["supabase_url"]
    SUPABASE_ANON_KEY = st.secrets["supabase_anon_key"]
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    SUPABASE_BUCKET_NAME = "product-images" # Your Supabase Storage bucket name
except KeyError:
    st.error("Supabase credentials not found in .streamlit/secrets.toml. Please set them up.")
    st.stop()
except Exception as e:
    st.error(f"Error initializing Supabase client: {e}")
    st.stop()


# Function to load data (NOW from Supabase)
@st.cache_data(ttl=3600)
def load_data():
    try:
        # Fetch all products from the 'products' table
        response = supabase.table('products').select('*').execute()
        
        # Check for data
        if response.data:
            df = pd.DataFrame(response.data)
            # Ensure columns are in the expected order and types if needed
            expected_cols = ['id', 'mould_no', 'description', 'weight_pp', 'weight_hip', 'image_url']
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = '' # Add missing columns
            df = df[expected_cols] # Reorder columns
            return df
        else:
            # Return an empty DataFrame if no data found
            st.info("No products found in the database.")
            return pd.DataFrame(columns=['id', 'mould_no', 'description', 'weight_pp', 'weight_hip', 'image_url'])
    except Exception as e:
        st.error(f"Error loading data from Supabase: {e}. Please check your database connection and RLS policies.")
        return pd.DataFrame(columns=['id', 'mould_no', 'description', 'weight_pp', 'weight_hip', 'image_url'])

# --- NEW: Function to add a product to Supabase ---
def add_product_to_db(product_data: dict):
    try:
        response = supabase.table('products').insert(product_data).execute()
        if response.data:
            st.cache_data.clear() # Clear cache to fetch new data on next load
            return True
        else:
            st.error(f"Failed to add product: {response.json()}")
            return False
    except Exception as e:
        st.error(f"Error adding product to Supabase: {e}")
        return False

# --- NEW: Function to delete a product from Supabase ---
def delete_product_from_db(product_id: str):
    try:
        response = supabase.table('products').delete().eq('id', product_id).execute()
        if response.data: # Supabase returns data for deleted rows if successful
            st.cache_data.clear() # Clear cache after deletion
            return True
        else:
            st.error(f"Failed to delete product: {response.json()}")
            return False
    except Exception as e:
        st.error(f"Error deleting product from Supabase: {e}")
        return False


# --- Corrected Helper Function to Resize Image ---
def resize_image(image_bytes, size=(200, 200)):
    """
    Receives image bytes, resizes the image while maintaining aspect ratio,
    and returns a PIL Image object.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        image = image.convert("RGB")

        image = image.resize(size)

        return image
        
    except Exception as e:
        st.error(f"Error resizing image: {e}")
        return None


# --- Corrected Upload Function ---
def upload_image_to_supabase(uploaded_file, product_id):
    """
    Resizes an uploaded image and uploads it to Supabase Storage.
    Returns the public URL of the uploaded image.
    """
    if uploaded_file is None:
        return ""

    image_bytes = uploaded_file.getvalue()

    resized_image_obj = resize_image(image_bytes)

    if resized_image_obj is None:
        st.error("Failed to resize image, upload cancelled.")
        return ""

    with io.BytesIO() as buffer:
        # Save the image to the buffer. 'JPEG' is efficient for photos.
        # Use format='PNG' if you need transparency.
        resized_image_obj.save(buffer, format="JPEG")
        image_bytes_to_upload = buffer.getvalue()

    try:
        unique_filename = f"{product_id.replace(' ', '_').lower()}-{uuid.uuid4()}.jpg"
        
        res = supabase.storage.from_(SUPABASE_BUCKET_NAME).upload(
            path=unique_filename,
            file=image_bytes_to_upload,
            file_options={"content-type": "image/jpeg"} # Match the format saved
        )
        
        public_url = supabase.storage.from_(SUPABASE_BUCKET_NAME).get_public_url(unique_filename)
        
        st.success(f"Image uploaded successfully!")
        return public_url

    except Exception as e:
        st.error(f"Error during Supabase Storage upload: {e}")
        return ""
    

