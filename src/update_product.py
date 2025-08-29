import time
import streamlit as st
import os
from utils import get_product_by_id, update_product_in_db, upload_image_to_local

st.set_page_config(page_title="Update Product", page_icon="📦", layout="centered")

def update_product_page():
    st.title("Update Product")

    # Check if product_id is passed in query params
    product_id = st.session_state.get("product_id")

    if not product_id:
        st.error("No product ID provided. Please select a product to update from the Product List page.")
        st.stop()

    # Fetch the existing product data
    existing_product = get_product_by_id(product_id)
    
    if not existing_product:
        st.error(f"Product with ID '{product_id}' not found.")
        st.stop()

    st.info(f"Updating product: **{product_id}**")

    with st.form("update_product_form"):
        st.subheader("Product Details")

        # Pre-populate form fields with existing data
        mould_no = st.text_input("Mould Number", value=existing_product.get('mould_no', '')).strip()
        description = st.text_area("Description", value=existing_product.get('description', ''), height=68).strip()

        location = st.text_input("Location", value=existing_product.get('location', ''), help="Rack").strip()
        
        # Handle hook selection with safe indexing
        hook_options = ["Plastic", "Metal"]
        current_hook = existing_product.get('hook', 'Plastic')
        hook_index = 0 if current_hook == "Plastic" else (1 if current_hook == "Metal" else 0)
        hook = st.selectbox("Hook", options=hook_options, index=hook_index).strip()
        cavaties = st.number_input("Cavities", min_value=1, max_value=100, 
                                  value=int(existing_product.get('cavaties', 1)), step=1)
        part_wt = st.number_input("Part Weight (g)", min_value=0.0, 
                                 value=float(existing_product.get('part_wt', 0.0)), step=0.1)
        short_wt = st.number_input("Shot Weight (g)", min_value=0.0, 
                                  value=float(existing_product.get('short_wt', 0.0)), step=0.1)

        # Show current image if exists
        current_image_url = existing_product.get('image_url', '')
        if current_image_url:
            st.subheader("Current Image")
            # Convert relative path to absolute path for local images
            if not current_image_url.startswith(('http://', 'https://')):
                # It's a local file path - validate it's safe
                absolute_path = os.path.join(os.path.dirname(__file__), current_image_url)
                absolute_path = os.path.abspath(absolute_path)
                images_dir_abs = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/images'))
                
                # Ensure path is within images directory (security check)
                if absolute_path.startswith(images_dir_abs) and os.path.exists(absolute_path):
                    st.image(absolute_path, caption="Current Product Image", width=200)
                else:
                    st.warning("Current image file not found.")
            else:
                # It's a URL
                st.image(current_image_url, caption="Current Product Image", width=200)
        
        uploaded_image = st.file_uploader("Upload New Product Image (Optional - leave empty to keep current image)", 
                                        type=["jpg", "jpeg", "png"])
        
        st.markdown("---")
        submitted = st.form_submit_button("Update Product", type="primary")

        if submitted:
            image_url_to_save = current_image_url  # Keep current image by default

            # If a new image is uploaded, upload it and update the URL
            if uploaded_image is not None:
                uploaded_url = upload_image_to_local(uploaded_image, product_id)
                if uploaded_url:
                    image_url_to_save = uploaded_url
                else:
                    st.warning("Failed to upload new image. Keeping the current image.")
            
            updated_product_data = {
                'mould_no': mould_no,
                'description': description,
                'image_url': image_url_to_save,
                'location': location,
                'hook': hook,
                'cavaties': int(cavaties),
                'part_wt': round(float(part_wt), 2),
                'short_wt': round(float(short_wt), 2)
            }
            
            if update_product_in_db(product_id, updated_product_data):
                st.success(f"Product '{product_id}' updated successfully!")
                # Clear the id query param when going back
                st.session_state["product_id"] = None
                st.balloons()

                time.sleep(1)
                st.switch_page("main.py")
            else:
                st.error(f"Failed to update product '{product_id}'.")

    # Add a back button outside the form
    st.markdown("---")
    if st.button("← Back to Product List", type="secondary"):
        # Clear query params and go back
        if "id" in st.query_params:
            del st.query_params["id"]
        st.switch_page("main.py")

if __name__ == "__main__":
    update_product_page()
