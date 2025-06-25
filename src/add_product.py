import streamlit as st
from utils import load_data, add_product_to_db, upload_image_to_supabase

st.set_page_config(page_title="Add New Product", page_icon="📦", layout="centered")

def add_product_page():
    st.title("Add New Product")

    df = load_data()

    with st.form("new_product_form", clear_on_submit=True):
        st.subheader("Product Details")

        product_id = st.text_input("Product ID (Unique Identifier)*", help="e.g., PROD001, ITEM_XYZ").strip()
        mould_no = st.text_input("Mould Number").strip()
        description = st.text_area("Description", height=68).strip()

        location = st.text_input("Location", help="Rack").strip()
        hook = st.selectbox("Hook", options=["Plastic", "Metal"]).strip()
        cavaties = st.number_input("Cavities", min_value=1, max_value=100, value=1, step=1)
        part_wt = st.number_input("Part Weight (g)", min_value=0.0, value=0.0, step=0.1)
        short_wt = st.number_input("Short Weight (g)", min_value=0.0, value=0.0, step=0.1)

        uploaded_image = st.file_uploader("Upload Product Image (Optional)", type=["jpg", "jpeg", "png"])
        
        st.markdown("---")
        submitted = st.form_submit_button("Add Product", type="primary")

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
                
                new_product_data = { 
                    'id': product_id,
                    'mould_no': mould_no,
                    'description': description,
                    'image_url': image_url_to_save,
                    'location': location,
                    'hook': hook,
                    'cavaties': int(cavaties),
                    'part_wt': round(float(part_wt), 2),
                    'short_wt': round(float(short_wt), 2)
                }
                
                if add_product_to_db(new_product_data):
                    st.success(f"Product '{product_id}' added successfully to Supabase!")
                else:
                    st.error(f"Failed to add product '{product_id}' to Supabase.")

if __name__ == "__main__":
    add_product_page()