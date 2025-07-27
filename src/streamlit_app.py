import streamlit as st

# Setup navigation pages in this file
pages = [
    st.Page(
        "main.py",
        title="Product List",
        icon=":material/home:",
    ),
    st.Page(
        "add_product.py",
        title="Add Product",
        icon=":material/add:",
    ),
    st.Page(
        "update_product.py",
        title="Update Product",
        icon=":material/edit:",
    )
]

page = st.navigation(pages)
page.run()