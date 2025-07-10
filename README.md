# IT Asset Management System

A comprehensive web-based IT asset management system built with FastAPI backend and modern frontend, designed to help organizations track, manage, and analyze their IT infrastructure assets.

## 🚀 Features

### Core Functionality
- **Asset Management**: Add, view, edit, and delete IT assets
- **Excel Upload**: Bulk import assets from Excel files with automatic data cleaning
- **User Authentication**: Secure login system with role-based access (Admin/Manager)
- **Real-time Analytics**: Interactive charts and visualizations for asset insights
- **Server Hierarchy**: Visual tree structure for master/slave server relationships

### Role-Based Access Control
- **Admin Users**: Full access to all features including asset upload, deletion, and user management
- **Manager Users**: View-only access to dashboard and analytics

### Analytics & Visualization
- **Asset Type Distribution**: Pie chart showing breakdown of asset types
- **Location Analysis**: Stacked bar charts for asset distribution by location and type
- **Server Tree Visualization**: Hierarchical view of master and slave servers
- **Interactive Charts**: Built with Chart.js for responsive and beautiful visualizations

### Data Management
- **Automatic Data Cleaning**: Removes duplicates and invalid entries during Excel upload
- **Validation**: Real-time form validation for asset addition
- **Database Support**: PostgreSQL with SQLAlchemy ORM
- **Excel Processing**: Pandas-based Excel file handling with data normalization

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Robust relational database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **Pandas**: Data manipulation and Excel processing
- **OpenPyXL**: Excel file handling

### Frontend
- **HTML5/CSS3**: Modern, responsive design
- **JavaScript**: Interactive functionality and API integration
- **Chart.js**: Beautiful and responsive charts
- **Bootstrap**: CSS framework for styling
- **Jinja2**: Template engine for dynamic content

### Security
- **Password Hashing**: bcrypt for secure password storage
- **JWT Authentication**: Stateless authentication system
- **Role-based Access**: Granular permissions system
- **Input Validation**: Comprehensive data validation

## 📋 Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher
- PostgreSQL database server
- pip (Python package installer)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ronitssaini/it_asset_management.git
cd it_asset_management
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Create PostgreSQL database
createdb it_asset_management

# Or using psql
psql -U postgres
CREATE DATABASE it_asset_management;
```

### 5. Environment Configuration
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/it_asset_management
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Initialize Database
```bash
cd backend
python reset_db.py
```

### 7. Create Admin User
```bash
python create_user.py
```

## 🏃‍♂️ Running the Application

### Start the Backend Server
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Application
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 Usage Guide

### 1. User Registration & Login
- Navigate to the registration page to create a new account
- Use the login page to access the system
- Admin users have additional privileges

### 2. Asset Management
- **Add Assets**: Use the "Add Asset" form for individual asset entry
- **Upload Excel**: Use the upload feature for bulk asset import
- **View Assets**: Access the dashboard to see all assets
- **Delete Assets**: Admin users can delete assets from the dashboard

### 3. Analytics Dashboard
- **Asset Overview**: View total assets and distribution
- **Interactive Charts**: Explore asset types and locations
- **Server Hierarchy**: Visualize master/slave server relationships

### 4. Excel Upload
- Prepare Excel file with asset data
- Upload through the web interface
- System automatically cleans and validates data
- Duplicates and invalid entries are removed

## 🔧 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Assets
- `GET /assets/` - Get all assets
- `POST /assets/` - Create new asset
- `DELETE /assets/{serial_number}` - Delete asset
- `GET /assets/analytics` - Get analytics data

### Upload
- `POST /upload/` - Upload Excel file

## 📁 Project Structure

```
it-asset-dashboard/
├── backend/
│   ├── auth/                 # Authentication modules
│   ├── database/             # Database configuration
│   ├── models/               # SQLAlchemy models
│   ├── routers/              # API route handlers
│   ├── services/             # Business logic
│   ├── utils/                # Utility functions
│   └── main.py              # FastAPI application
├── frontend/
│   ├── static/              # CSS, JS, images
│   └── templates/           # HTML templates
├── requirements.txt          # Python dependencies
├── clean_inventory_excel.py # Excel cleaning utility
└── README.md               # This file
```

## 🔒 Security Features

- **Password Security**: bcrypt hashing for password storage
- **JWT Tokens**: Secure stateless authentication
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents injection
- **Role-based Access**: Granular permission system

## 📈 Data Analytics

The system provides comprehensive analytics including:
- Asset type distribution
- Location-based asset analysis
- Server hierarchy visualization
- Interactive charts and graphs
- Real-time data updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the API documentation at `/docs`

## 🔄 Version History

- **v1.0.0**: Initial release with core asset management features
- Analytics dashboard with interactive charts
- Excel upload with automatic data cleaning
- Role-based access control system
- Server hierarchy visualization

---

**Built with ❤️ using FastAPI and modern web technologies**
