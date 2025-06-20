import streamlit as st
from utils import load_data, add_product_to_db, upload_image_to_supabase

st.set_page_config(page_title="Add New Product", page_icon="➕")

def add_product_page():
    st.title("Add New Product")

    # Load data to check for ID uniqueness (from Supabase via load_data)
    df = load_data()

    with st.form("new_product_form", clear_on_submit=True):
        st.subheader("Product Details")

        product_id = st.text_input("Product ID (Unique Identifier)*", help="e.g., PROD001, ITEM_XYZ").strip()
        mould_no = st.text_input("Mould Number").strip()
        description = st.text_area("Description").strip()

        weight_pp = st.number_input("Weight PP (grams)", min_value=0.0, format="%.2f", value=0.0)
        weight_hip = st.number_input("Weight HIP (grams)", min_value=0.0, format="%.2f", value=0.0)

        uploaded_image = st.file_uploader("Upload Product Image (Optional)", type=["jpg", "jpeg", "png"])
        
        st.markdown("---")
        submitted = st.form_submit_button("Add Product")

        if submitted:
            # Basic validation
            if not product_id:
                st.error("Product ID is a required field.")
            elif product_id in df['id'].values: # Still check local DataFrame for immediate feedback
                st.error(f"Product with ID '{product_id}' already exists. Please use a unique ID.")
            else:
                image_url_to_save = ""

                if uploaded_image is not None:
                    uploaded_url = upload_image_to_supabase(uploaded_image, product_id)
                    if uploaded_url:
                        image_url_to_save = uploaded_url
                    else:
                        st.warning("Failed to upload image to Supabase Storage. Product will be added without an image URL.")
                
                new_product_data = { # Prepare data for Supabase insert
                    'id': product_id,
                    'mould_no': mould_no,
                    'description': description,
                    'weight_pp': float(weight_pp), # Ensure numeric types for DB
                    'weight_hip': float(weight_hip), # Ensure numeric types for DB
                    'image_url': image_url_to_save
                }
                
                # --- CHANGE HERE: Call the new DB add function ---
                if add_product_to_db(new_product_data):
                    st.success(f"Product '{product_id}' added successfully to Supabase!")
                else:
                    st.error(f"Failed to add product '{product_id}' to Supabase.")

if __name__ == "__main__":
    add_product_page()