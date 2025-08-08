# TodoShare

A modern productivity platform for teams and individuals to organize, collaborate, and deliver exceptional results.

## Features

- 🎯 **Smart Task Management** - Create, assign, and track tasks with priorities and due dates
- 👥 **Team Collaboration** - Share projects, leave comments, and track progress in real-time  
- 📊 **Advanced Analytics** - Get insights into team productivity with detailed reports
- 📱 **Mobile Ready** - Fully responsive design that works on all devices
- ⚡ **Lightning Fast** - Built with modern technology for instant loading
- 🔒 **Secure & Private** - Enterprise-grade security with encrypted data

## Tech Stack

### Frontend
- Vue 3 + TypeScript
- Tailwind CSS
- Pinia (State Management)
- Vite

### Backend  
- FastAPI (Python)
- JWT Authentication
- Mock Storage (Development)

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.8+

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd todo-share
```

2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

3. Setup Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Development URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
.
├── frontend/           # Vue 3 frontend application
│   ├── src/
│   │   ├── components/ # Reusable components
│   │   ├── views/      # Page components
│   │   ├── stores/     # Pinia stores
│   │   └── services/   # API services
│   └── ...
├── backend/            # FastAPI backend
│   ├── app/
│   │   ├── api/        # API routes
│   │   ├── core/       # Core functionality
│   │   └── models/     # Data models
│   └── ...
└── docs/              # Development tickets and documentation
```

## Development

This project was built following an MVP approach with structured development tickets. See the `/docs` folder for the complete development process and requirements.

## License

This project is licensed under the MIT License.
EOF < /dev/null