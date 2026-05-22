def get_custom_css():
    return """
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        /* Base styles */
        * {
            font-family: 'Outfit', sans-serif !important;
        }
        
        .main {
            background-color: #F1F3F6;
        }

        /* Top Header Styling (Flipkart Blue) */
        .app-header {
            background-color: #2874F0;
            padding: 1rem 2rem;
            color: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px rgba(40, 116, 240, 0.15);
        }
        .app-header h1 {
            color: white !important;
            margin: 0;
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        .app-header span {
            color: #FFE500;
            font-style: italic;
            font-weight: 700;
        }

        /* Banner Carousel Mockup */
        .banner-carousel {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .banner-carousel::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 80%);
            pointer-events: none;
        }

        /* Product Cards Grid */
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 1.5rem;
            padding: 1rem 0;
        }
        
        .product-card {
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            border: 1px solid #E0E0E0;
            display: flex;
            flex-direction: column;
            height: 100%;
            position: relative;
        }
        
        .product-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
            border-color: #2874F0;
        }
        
        .product-img-container {
            width: 100%;
            height: 200px;
            background-color: #f9f9f9;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
            padding: 10px;
        }
        
        .product-img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            transition: transform 0.5s ease;
        }
        
        .product-card:hover .product-img {
            transform: scale(1.05);
        }
        
        .product-info {
            padding: 1.2rem;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        
        .product-title {
            font-size: 1rem;
            font-weight: 600;
            color: #212121;
            margin-bottom: 0.5rem;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            height: 2.8rem;
        }
        
        .product-category {
            font-size: 0.8rem;
            color: #878787;
            text-transform: uppercase;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        
        .rating-badge {
            background-color: #388E3C;
            color: white;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 2px 6px;
            border-radius: 4px;
            display: inline-flex;
            align-items: center;
            gap: 2px;
            width: fit-content;
            margin-bottom: 0.5rem;
        }
        
        .price-row {
            display: flex;
            align-items: baseline;
            gap: 8px;
            margin-top: auto;
        }
        
        .price-current {
            font-size: 1.3rem;
            font-weight: 700;
            color: #212121;
        }
        
        .price-original {
            font-size: 0.9rem;
            color: #878787;
            text-decoration: line-through;
        }
        
        .price-discount {
            font-size: 0.9rem;
            color: #388E3C;
            font-weight: 600;
        }

        /* Sidebar Glassmorphism */
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #E0E0E0;
            box-shadow: 2px 0 10px rgba(0,0,0,0.02);
        }
        
        /* Custom Buttons styling */
        .stButton>button {
            border-radius: 6px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        
        .buy-now-btn button {
            background-color: #FF9F00 !important;
            color: white !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            width: 100% !important;
            font-size: 1rem !important;
        }
        
        .buy-now-btn button:hover {
            background-color: #f39700 !important;
            box-shadow: 0 4px 8px rgba(255, 159, 0, 0.3) !important;
        }
        
        .add-to-cart-btn button {
            background-color: #FF5722 !important;
            color: white !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            width: 100% !important;
            font-size: 1rem !important;
        }
        
        .add-to-cart-btn button:hover {
            background-color: #e64a19 !important;
            box-shadow: 0 4px 8px rgba(255, 87, 34, 0.3) !important;
        }

        /* Admin KPI Cards */
        .kpi-container {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        
        .kpi-card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            border: 1px solid #eef2f6;
            flex: 1;
            min-width: 200px;
            text-align: center;
        }
        
        .kpi-title {
            font-size: 0.9rem;
            color: #878787;
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: #2874F0;
        }

        /* Checkout summary */
        .checkout-box {
            background-color: white;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .checkout-header {
            font-size: 1.1rem;
            font-weight: 700;
            color: #878787;
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 0.8rem;
            margin-bottom: 1rem;
            text-transform: uppercase;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px 4px 0px 0px;
            gap: 9px;
            font-weight: 600;
            font-size: 1rem;
            color: #212121;
        }

        .stTabs [aria-selected="true"] {
            border-bottom-color: #2874F0 !important;
            color: #2874F0 !important;
        }
        
        /* Order status timeline badge */
        .status-badge {
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            display: inline-block;
        }
        
        .status-pending { background-color: #FFF9C4; color: #F57F17; }
        .status-shipped { background-color: #E3F2FD; color: #0D47A1; }
        .status-delivered { background-color: #E8F5E9; color: #1B5E20; }
        .status-cancelled { background-color: #FFEBEE; color: #B71C1C; }

    </style>
    """
