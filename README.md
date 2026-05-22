# 🛒 Apna Bazaar - E-Commerce Platform

A complete Flipkart-like e-commerce application built with Python and Streamlit, featuring product browsing, shopping cart, user authentication, order management, and an admin dashboard.

## 🌟 Features

### Customer Features
- **Product Browsing**: Browse products by category with search and filter options
- **Advanced Search**: Search products by title and description
- **Sorting Options**: Sort by Featured, Price (Low/High), and Customer Rating
- **Product Details**: View detailed product information with images
- **Shopping Cart**: Add/remove items, adjust quantities
- **User Authentication**: Login and registration system
- **Order Placement**: Complete checkout process with multiple payment options
- **Order Tracking**: View order history and status
- **Product Reviews**: Read and write customer reviews

### Admin Features
- **Analytics Dashboard**: View business metrics and KPIs
- **Revenue Analytics**: Revenue by category and trend analysis
- **Order Management**: View and manage all orders, update status
- **Product Management**: Add, edit, and delete products
- **Image Upload**: Support for local image uploads and URL images
- **Inventory Management**: Track stock levels

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone or download the project**
   ```bash
   cd Apna_Bazaar
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   The database will be automatically initialized when you run the application for the first time.

## 🎯 Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:8501`

## 👤 Default Accounts

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@apnabazaar.com`

### Customer Account
- **Username**: `priya`
- **Password**: `customer123`
- **Email**: `priya@gmail.com`

## 📁 Project Structure

```
Apna_Bazaar/
├── app.py              # Main customer-facing application
├── admin.py            # Admin dashboard
├── database.py         # Database operations and initialization
├── styles.py           # Custom CSS styling
├── requirements.txt    # Python dependencies
├── apna_bazaar.db     # SQLite database (auto-created)
├── images/            # Directory for uploaded product images
└── README.md          # This file
```

## 🗄️ Database Schema

The application uses SQLite with the following tables:

- **users**: User accounts with authentication
- **products**: Product catalog with images and details
- **reviews**: Customer product reviews
- **orders**: Customer orders
- **order_items**: Individual items in each order

## 🎨 Features Overview

### Product Management
- Add products with title, description, price, category, and images
- Upload local images or provide image URLs
- Edit product details
- Delete products
- Manage stock levels

### Shopping Experience
- Category-based browsing
- Real-time search
- Price range filtering
- Multiple sorting options
- Responsive product grid
- Add to cart functionality
- Quantity adjustment

### Checkout Process
- Address and phone number validation
- Multiple payment methods (UPI, Credit Card, Debit Card, Net Banking, COD)
- Order confirmation
- Automatic stock deduction

### Admin Analytics
- Total revenue tracking
- Order count and status distribution
- Product count
- Customer count
- Revenue by category charts
- Revenue trend over time
- Order status pie chart

## 🔧 Customization

### Adding New Categories
Edit the category dropdown in `app.py` and `admin.py` to add new product categories.

### Modifying Styling
Custom CSS is defined in `styles.py`. Modify the `get_custom_css()` function to change colors, fonts, and layouts.

### Database Configuration
Database settings are in `database.py`. The default SQLite database file is `apna_bazaar.db`.

## 📸 Image Handling

The application supports two image sources:
1. **Local Upload**: Images are saved to the `images/` directory
2. **URL**: Direct image URLs (e.g., from Unsplash)

Default placeholder images are used if no image is provided.

## 🔐 Security Notes

- Passwords are hashed using SHA-256
- Session management uses Streamlit's session state
- Admin-only pages are protected
- Input validation on forms

## 🐛 Troubleshooting

### Database Errors
If you encounter database errors, delete `apna_bazaar.db` and restart the application to reinitialize.

### Image Upload Issues
Ensure the `images/` directory exists and has write permissions.

### Port Already in Use
If port 8501 is in use, specify a different port:
```bash
streamlit run app.py --server.port 8502
```

## 📝 Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation
- **plotly**: Interactive charts
- **pillow**: Image processing

## 🎯 Future Enhancements

- Email notifications for orders
- Wishlist functionality
- Product comparison
- Advanced search filters
- Payment gateway integration
- Multi-language support
- Mobile app version

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a complete e-commerce solution demonstrating Python and Streamlit capabilities.

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Unsplash for placeholder images
- Flipkart for design inspiration

---

**Happy Shopping! 🛍️**
