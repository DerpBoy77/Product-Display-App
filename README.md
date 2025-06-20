# Product Management App

## 🚀 Project Overview

This is a simple yet effective web application for managing product information, allowing users to add, view, search, and delete product details along with their associated images. It's built for ease of use, providing a clean interface for quick product data management.

## 🌟 How to Use

The application is straightforward to navigate and use:

1.  **View Products (Main Page):**
    * Upon launching the app, you'll see a list of all existing products.
    * Each product displays its ID, Mould Number, Description, Weight details, and an associated image.
    * **Search Bar:** Use the search bar at the top to filter products by Product ID, Mould Number, or Description.
    * **Delete Button:** Each product entry has a "Delete" button. Clicking it will prompt a confirmation to remove the product and its image permanently.

2.  **Add New Product (Sidebar):**
    * Navigate to the "Add New Product" page using the sidebar.
    * Fill in the required product details (Product ID, Mould Number, Description, Weights).
    * **Image Upload:** You can upload an image for the product. The application automatically processes (resizes and crops to a uniform size) the image before storing it.
    * Click "Add Product" to save the new entry.

## 🛠️ How It Was Created

This application is a full-stack project utilizing modern, open-source technologies:

* **Frontend:** Developed using **Streamlit**, a Python library that enables rapid creation of interactive web applications.
* **Backend:** Powered by **Supabase**, an open-source platform providing:
    * A **PostgreSQL Database** for structured product data.
    * **Supabase Storage** for efficient storage and retrieval of product images.
    * **Row Level Security (RLS)** is configured on both the database and storage to manage access permissions.
* **Image Processing:** Python's **Pillow (PIL)** library is used server-side to standardize image sizes during upload, ensuring a consistent display across all product photos.

## 📦 Project Structure