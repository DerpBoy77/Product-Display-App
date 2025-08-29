# Product Management App

## 🚀 Project Overview

This is a secure, self-hosted web application for managing product information, allowing users to add, view, search, update, and delete product details along with their associated images. Built with security and ease of deployment in mind, it provides a clean interface for efficient product data management without requiring external services.

## ✨ Features

- **Product Management**: Add, view, update, and delete products
- **Image Upload**: Secure image handling with automatic resizing
- **Search Functionality**: Filter products by ID, mould number, or description
- **Self-Hosted**: No external dependencies - runs completely offline
- **Secure**: Input validation, SQL injection prevention, and path traversal protection
- **Lightweight**: Uses SQLite database and local file storage

## 🌟 How to Use

### Prerequisites
- Python 3.11 or higher
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Product-Display-App
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run src/streamlit_app.py
   ```

5. **Open your browser** and go to `http://localhost:8501`

### Using the Application

1. **View Products (Main Page):**
   - See a list of all existing products with images, details, and specifications
   - **Search Bar**: Filter products by Product ID, Mould Number, or Description
   - **Update Button**: Modify existing product information
   - **Delete Button**: Remove products with confirmation dialog

2. **Add New Product:**
   - Navigate to "Add Product" page using the sidebar
   - Fill in product details (Product ID is required and must be unique)
   - **Image Upload**: Upload product images (JPG, JPEG, PNG) - automatically resized
   - Form validation ensures data integrity

3. **Update Product:**
   - Select a product from the main list to update
   - Modify any field including uploading a new image
   - Previous image is preserved if no new image is uploaded

## 🛠️ How It Was Created

This application is a full-stack project utilizing modern, secure technologies:

* **Frontend:** Developed using **Streamlit**, a Python library that enables rapid creation of interactive web applications.
* **Backend:** Powered by **SQLite**, a lightweight, serverless database providing:
    * A **local SQLite Database** for structured product data storage
    * **Local file storage** for efficient storage and retrieval of product images
    * **Secure parameterized queries** to prevent SQL injection attacks
    * **Input validation** and **path traversal protection**
* **Image Processing:** Python's **Pillow (PIL)** library handles server-side image processing:
    * Automatic image resizing to standardize display
    * Format conversion to JPEG for optimal storage
    * File size validation (5MB maximum)

## 🔒 Security Features

- **SQL Injection Prevention**: All database queries use parameterized statements
- **Path Traversal Protection**: Secure file upload and display with path validation
- **Input Validation**: Comprehensive validation for all user inputs
- **File Type Restrictions**: Only image files (JPG, JPEG, PNG) allowed
- **File Size Limits**: Maximum 5MB per image upload
- **Secure File Permissions**: Database and image files have restricted access
- **XSRF Protection**: Cross-Site Request Forgery protection enabled

## 📁 Project Structure

```
Product-Display-App/
├── src/
│   ├── streamlit_app.py    # Main application entry point
│   ├── main.py             # Product list and display logic
│   ├── add_product.py      # Add new product functionality
│   ├── update_product.py   # Update existing product functionality
│   └── utils.py            # Database and utility functions
├── data/
│   ├── products.db         # SQLite database (auto-created)
│   ├── images/             # Product images storage (auto-created)
│   └── products.csv        # Sample data (optional)
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── Dockerfile             # Container deployment
└── README.md              # This file
```

## 🐳 Docker Deployment

Build and run with Docker:

```bash
# Build the image
docker build -t product-display-app .

# Run the container
docker run -p 8501:8501 -v $(pwd)/data:/app/data product-display-app
```

The volume mount ensures your data persists between container restarts.

## 🔧 Configuration

The application is configured via `.streamlit/config.toml`:
- XSRF protection enabled
- Minimal toolbar mode
- Optimized for production deployment

## 📝 Data Schema

The SQLite database uses the following schema:

```sql
CREATE TABLE products (
    id TEXT PRIMARY KEY,        -- Unique product identifier
    mould_no TEXT,             -- Mould number
    description TEXT,          -- Product description
    image_url TEXT,            -- Path to product image
    location TEXT,             -- Storage location/rack
    hook TEXT,                 -- Hook type (Plastic/Metal)
    cavaties INTEGER,          -- Number of cavities
    part_wt REAL,             -- Part weight in grams
    short_wt REAL             -- Shot weight in grams
);
```

## 🚀 Deployment Options

1. **Local Development**: Run directly with `streamlit run src/streamlit_app.py`
2. **Docker**: Use the provided Dockerfile for containerized deployment
3. **Cloud Platforms**: Deploy to any platform supporting Python/Streamlit (Heroku, Railway, etc.)
4. **Self-Hosted**: Run on any server with Python support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

- **Database issues**: Delete `data/products.db` to reset the database
- **Image display problems**: Check that `data/images/` directory exists and has proper permissions
- **Port conflicts**: Change the port in `.streamlit/config.toml` if 8501 is in use
- **Permission errors**: Ensure the application has read/write access to the `data/` directory