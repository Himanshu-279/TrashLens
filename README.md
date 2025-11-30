# ♻️ TrashLens - Smart Waste Classification System

**TrashLens** is an ML(CNN) -powered web application built with **Django** that helps users classify waste into different categories (Recyclable, Organic, Hazardous) to promote proper disposal and environmental sustainability.

It uses Machine Learning to identify waste types from images and helps users locate nearby recycling centers.

---

## 🚀 Features

* **🔍 AI Waste Detection:** Upload an image of trash, and the system predicts its type (e.g., Plastic, Paper, Metal).
* **📍 Recycling Center Locator:** Uses `centers.csv` data to help users find the nearest recycling facilities.
* **🐳 Dockerized:** Fully containerized application for easy deployment.
* **☁️ Cloud Ready:** Optimized for deployment on platforms like **Render**.
* **📱 Responsive UI:** Clean interface for both mobile and desktop users.

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **ML/AI:** TensorFlow/Keras (or Scikit-learn) integration
* **Database:** SQLite (Default) / PostgreSQL
* **Containerization:** Docker
* **Deployment:** Render

---

## 📂 Project Structure

```bash
trashlens/
├── core/                  # Main application logic
├── trashlens_project/     # Project settings and configuration
├── centers.csv            # Dataset for recycling centers
├── Dockerfile             # Docker configuration for containerization
├── manage.py              # Django command-line utility
├── requirements.txt       # Python dependencies
└── build.sh               # Build script for Render deployment
⚡ How to Run Locally
1. Clone the Repository
Bash

git clone [https://github.com/Himanshu-279/trashlens-django.git](https://github.com/Himanshu-279/trashlens-django.git)
cd trashlens-django
2. Create Virtual Environment
Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Apply Migrations
Bash

python manage.py migrate
5. Run Server
Bash

python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.

🐳 Run using Docker
If you have Docker installed, you can simply run:

Bash

# Build the image
docker build -t trashlens .

# Run the container
docker run -p 8000:8000 trashlens
🌍 Deployment (Render)
This project includes a build.sh script and is configured for seamless deployment on Render.

Connect your GitHub repo to Render.

Select Web Service.

Use Build Command: ./build.sh

Use Start Command: gunicorn trashlens_project.wsgi:application

🤝 Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📬 Contact
Himanshu Verma

LinkedIn: Himanshu Verma 1711

GitHub: Himanshu-279
