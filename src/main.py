import streamlit as st
import pandas as pd
from utils import load_data, delete_product_from_db

st.set_page_config(page_title="Product List", page_icon="📦", layout="wide")


# Function to delete a product and manage state/rerun (NOW from Supabase)
def delete_product_and_clear_state(product_id_to_delete):
    if delete_product_from_db(product_id_to_delete):
        st.success(f"Product with ID '{product_id_to_delete}' deleted successfully from Supabase!")
    else:
        st.error(f"Product with ID '{product_id_to_delete}' not found or failed to delete from Supabase.")

    # IMPORTANT: Clear state variables *before* the rerun
    if 'show_confirm_dialog' in st.session_state:
        del st.session_state['show_confirm_dialog']
    if 'confirm_delete_id' in st.session_state:
        del st.session_state['confirm_delete_id']
    st.rerun()

def display_products():

    st.title("Product Information Display")

    if 'show_confirm_dialog' in st.session_state and st.session_state['show_confirm_dialog']:
        if 'confirm_delete_id' in st.session_state:
            st.warning(f"Are you sure you want to delete product: **{st.session_state['confirm_delete_id']}**?")
            col_confirm_yes, col_confirm_no = st.columns(2)
            with col_confirm_yes:
                if st.button("Yes, Delete", key="confirm_yes_top", type="primary"):
                    delete_product_and_clear_state(st.session_state['confirm_delete_id'])
            with col_confirm_no:
                if st.button("No, Cancel", key="confirm_no_top"):
                    st.info("Deletion cancelled.")
                    del st.session_state['show_confirm_dialog']
                    if 'confirm_delete_id' in st.session_state:
                        del st.session_state['confirm_delete_id']
                    st.rerun()

    df = load_data()

    if df.empty:
        st.info("No products found. Please add some products using the 'Add New Product' page.")
        return

    search_query = st.text_input("Search products (ID, Mould No., Description ...)", "").lower()

    if search_query:
        # Ensure that you're converting to string and handling NaN values
        df_filtered = df[
            df.apply(lambda row: row.astype(str).str.lower().str.contains(search_query, na=False).any(), axis=1)
        ]
    else:
        df_filtered = df

    if df_filtered.empty:
        st.warning("No products matching your search query.")
    else:
        for index, row in df_filtered.iterrows():
            st.subheader(f"Product ID: {row['id']}")
            col1, col2, col3, col4 = st.columns([1, 1, 1, 0.5])

            with col1:
                image_url = row['image_url'] if pd.notna(row['image_url']) and row['image_url'].strip() else None
                
                if image_url:
                    resized_image = image_url #resize_image(image_url, size=(200, 200))
                    st.image(resized_image, caption=f"ID: {row['id']}")
                else:
                    # Display a placeholder if no image URL
                    st.image("https://placehold.co/200x200?text=No+Image", caption=f"ID: {row['id']}")
            
            with col2:
                st.write(f"**Mould No.:** {row['mould_no']}")
                st.write(f"**Location:** {row['location']}")
                st.write(f"**Hook:** {row['hook']}") 
                st.write(f"**Description:** {row['description']}")
            
            with col3:
                st.write(f"**Cavities:** {row['cavaties']}")
                st.write(f"**Part Weight:** {row['part_wt']} g")
                st.write(f"**Shot Weight:** {row['short_wt']} g")

            with col4:
                delete_button_key = f"delete_button_{row['id']}"
                if st.button("Delete", key=delete_button_key):
                    st.session_state['confirm_delete_id'] = row['id']
                    st.session_state['show_confirm_dialog'] = True
                    st.rerun()

            st.markdown("---")

if __name__ == "__main__":
    display_products()