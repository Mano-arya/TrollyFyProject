# Trollyfy - Campus Second-Hand Marketplace

**HS3052 Capstone Project | Group 08**

## 👥 Credits
*   **Manorath Aryal**
*   **Suyok Neupane**
*   **Nikhil Patel**
*   **Dipesh Panday**

---

## 📝 Project Overview
Trollyfy is a web-based marketplace specifically designed for university students to exchange second-hand items within their campus community. It addresses the lack of a safe, localized platform for students to buy and sell textbooks, electronics, and furniture, reducing waste and facilitating affordable campus living.

## 🛠️ Technology Stack
*   **Backend**: Python 3.x with Django (MVT Architecture)
*   **Database**: PostgreSQL
*   **Frontend**: HTML5, CSS3, JavaScript, and Bootstrap 5
*   **Image Processing**: Pillow
*   **Environment Management**: python-dotenv

## 🚀 Key Features
*   **Secure Authentication**: Custom User Model extending `AbstractUser` to support campus-specific identifiers.
*   **Advanced Discovery**: Intelligent search using Django `Q` objects and category-based filtering.
*   **Seller CRUD**: Full management suite for sellers, including a requirement-enforced 3-image upload system.
*   **Security & Protection**: Strict ownership verification using `UserPassesTestMixin` to prevent unauthorized item modifications.
*   **Optimization**: Implemented `prefetch_related` and `select_related` to minimize database hits and maximize performance.

## ⚙️ Local Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.10+ and PostgreSQL installed.

### 2. Installation
```powershell
# Clone the repository
git clone https://github.com/your-repo/trollyfy.git
cd trollyfy

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database & Secret Configuration
Create a `.env` file in the root directory:
```env
DB_NAME=trollyfy_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
SECRET_KEY=your_secret_key
```

### 4. Run Migrations & Start Server
```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py run_server
```
Visit `http://127.0.0.1:8000/` to view the platform.
