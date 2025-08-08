# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TodoShare - 個人のタスク管理を効率化し、必要に応じて他者とタスクを共有・依頼できるWebアプリケーション（MVP版）

## Technical Stack

### Frontend
- **Framework**: Vue 3 + Composition API
- **State Management**: Pinia
- **UI Library**: Vuetify 3 or PrimeVue
- **Build Tool**: Vite
- **Language**: TypeScript

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy
- **Authentication**: JWT + OAuth2.0 (Google)
- **Validation**: Pydantic

### Infrastructure & Database
- **Database**: PostgreSQL (Supabase)
- **Authentication**: Supabase Auth
- **Real-time**: Supabase Realtime (for notifications)
- **Storage**: Supabase Storage (for profile images)

## Core Features

### 1. Authentication
- Email/password registration and login
- Google OAuth integration
- Password reset functionality

### 2. Todo Management
- CRUD operations with title, description, due date, priority, categories, recurring settings
- Status management (pending/completed)
- Priority levels (high/medium/low)
- Multiple category assignment
- Recurring tasks (daily/weekly/monthly)

### 3. Sharing & Request Features
- **Sharing**: Generate shareable links for read-only access
- **Requests**: Send todo requests to other users with approval/rejection flow
- In-app notifications for requests and reminders

### 4. Search & Filter
- Keyword search (title, description)
- Filters by status, priority, category, due date
- Sort by creation date, due date, priority, title

## Database Schema

### Main Tables
- **Users**: id, email, username, password_hash, profile_image_url, timestamps
- **Todos**: id, user_id, title, description, status, due_date, priority, recurring_pattern, timestamps
- **Categories**: id, user_id, name, color, created_at
- **TodoCategories**: todo_id, category_id (many-to-many)
- **TodoShares**: id, todo_id, share_token, expires_at, created_at
- **TodoRequests**: id, from_user_id, to_user_id, todo_id, message, status, rejection_reason, timestamps
- **Notifications**: id, user_id, type, title, message, is_read, related_id, created_at

## Development Phases

### Phase 1: Foundation (2 weeks)
- Environment setup
- Authentication implementation
- Basic Todo CRUD

### Phase 2: Core Features (2 weeks)
- Category management
- Due dates and priorities
- Search and filter functionality
- Recurring tasks

### Phase 3: Sharing & Requests (2 weeks)
- Sharing functionality
- Request system
- Notification system

### Phase 4: Quality Improvement (1 week)
- Bug fixes
- UI/UX improvements
- Performance optimization

## Development Commands

```bash
# Frontend (Vue)
npm install           # Install dependencies
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run linter
npm run type-check   # Run TypeScript type checking

# Backend (FastAPI)
pip install -r requirements.txt    # Install dependencies
uvicorn main:app --reload          # Start development server
python -m pytest                   # Run tests
python -m black .                  # Format code
python -m flake8                   # Run linter
```

## API Structure

- `/api/auth/*` - Authentication endpoints
- `/api/todos/*` - Todo CRUD operations
- `/api/categories/*` - Category management
- `/api/shares/*` - Sharing functionality
- `/api/requests/*` - Request management
- `/api/notifications/*` - Notification system

## Security Considerations

- HTTPS communication required
- Password hashing with bcrypt
- SQL injection prevention through parameterized queries
- XSS protection with proper input sanitization
- CSRF protection with tokens
- JWT authentication for API access

## Performance Targets

- Page load time: < 3 seconds
- API response time: < 1 second
- Concurrent users: 100 (MVP stage)
- Uptime: 99%+ (MVP stage)

## Current Structure

The repository contains:
- `.specstory/`: SpecStory extension artifacts for AI chat history (auto-saved markdown files)
- `.cursorindexingignore`: Excludes SpecStory files from Cursor indexing

## Development Tickets

チケットは `/docs` ディレクトリに分割されています：

1. **001_project_setup.md** - プロジェクトセットアップ
2. **002_authentication.md** - 認証機能
3. **003_todo_crud.md** - Todo CRUD機能
4. **004_category_management.md** - カテゴリ管理機能
5. **005_priority_due_date.md** - 優先度・期限機能
6. **006_search_filter.md** - 検索・フィルター機能
7. **007_recurring_tasks.md** - 繰り返しタスク機能
8. **008_share_todo.md** - Todo共有機能
9. **009_todo_request.md** - Todo依頼機能
10. **010_notifications.md** - 通知機能
11. **011_testing_deployment.md** - テスト・デプロイ機能

## Todo Management in Tickets

各チケット内でのTodo管理：
- `- [ ]` 未完了タスク
- `- [x]` 完了タスク

**重要**: タスク完了時は `- [ ]` を `- [x]` に変更してください。

## Notes

- SpecStory history files in `.specstory/history/` contain previous AI coding sessions
- These files are excluded from Cursor indexing but can be referenced explicitly with @ mentions
- Default categories: "仕事", "プライベート", "買い物", "その他"
- Notifications are in-app only for MVP (no email notifications)