# Image Annotation Generation System

![Application Preview](https://github.com/abhishekchauhan062003/Image-Annotation-Generation-System/blob/main/public/logo.png)

A full-stack web application for creating and managing image annotations with AI capabilities, featuring a React frontend and Flask backend.

## ✨ Features

- Interactive image annotation canvas
- AI-powered annotation suggestions
- Multi-user collaboration support
- Export annotations in multiple formats
- Responsive web design

## 🚀 Quick Start

### Prerequisites
- Node.js v16+
- Python 3.8+
- Git (optional)

### Installation
```bash
# Clone the repository
git clone https://github.com/abhishekchauhan062003/Image-Annotation-Generation-System
cd Image-Annotation-Generation-System
```

# Install backend dependencies
```bash
cd api
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
cd ..
```

# Install frontend dependencies
npm install

### Running the Application
#### Windows:
```powershell
# Using PowerShell
.\start.ps1

# OR using batch file
start.bat
```
### Linux
```bash
# Start backend (in one terminal)
cd api
source venv/bin/activate
flask run --port 5000

# Start frontend (in another terminal)
npm start
```
# 🔧 Project Structure
```
.
├── api/                    # Flask backend
│   ├── api-env/               # Python virtual environment
│   ├── app.py              # Main application file
│   ├── requirements.txt    # Python dependencies
│   └── ...                 # Other backend files
├── models/                 # Machine learning models
│   └── ...                 # Model files
├── public/                 # Static assets
│   ├── camera.jpg          # Sample image
│   ├── favicon.ico         # Browser icon
│   ├── index.html          # Main HTML template
│   └── ...                 # Other assets
├── src/                    # React application
│   ├── components/         # React components
│   ├── App.js              # Main component
│   └── ...                 # Other source files
├── .gitignore
├── package.json            # Frontend dependencies
├── package-lock.json
├── README.md               # This file
├── start.ps1               # PowerShell launcher
└── start.bat               # Batch file launcher
```
# 🤝 Contributing
Fork the repository

- Create your feature branch (git checkout -b feature/AmazingFeature)

- Commit your changes (git commit -m 'Add some AmazingFeature')

- Push to the branch (git push origin feature/AmazingFeature)

- Open a Pull Request
# 📧 Team

| Member | Role | Contact |
|--------|------|---------|
| [@lokeshjoshi](https://github.com/lucky-2104) | Backend Developer | lokesh2104joshi@gmail.com |
| [@ashutoshupreti](https://github.com/AshutoshUpreti096) | Frontend Developer | ashutoshupreti096@gmail.com |
| [@abhishekchauhan](https://github.com/abhishekchauhan062003) | ML Engineer | abhic062003@email.com |


