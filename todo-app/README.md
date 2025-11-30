# 📝 Django TODO Application

A modern, full-featured TODO application built with Django 5.2.8. Create, manage, and track your tasks with a beautiful, responsive UI.

## ✨ Features

- ✅ **CRUD Operations** - Create, Read, Update, and Delete TODOs
- 📅 **Due Dates** - Assign and track due dates for tasks
- ✓ **Mark as Resolved** - Toggle completion status with visual indicators
- 🎯 **Priority Levels** - Organize tasks by Low, Medium, or High priority
- 🔍 **Filtering** - View All, Active, or Completed TODOs
- ⚠️ **Overdue Detection** - Automatic highlighting of overdue tasks
- 📱 **Responsive Design** - Beautiful UI that works on all devices
- 🎨 **Modern Interface** - Clean, intuitive design with smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- pip

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd todo-app
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create admin user (optional):**
```bash
python manage.py createsuperuser
```
Default credentials (already created):
- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`

6. **Start the development server:**
```bash
python manage.py runserver
```

7. **Open your browser:**
- Main app: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📖 Usage Guide

### Creating a TODO
1. Click the **"+ New TODO"** button in the navigation bar
2. Fill in the title (required)
3. Optionally add description, due date, and priority
4. Click **"Create TODO"**

### Viewing TODOs
- **List View**: See all your TODOs in a card layout
- **Detail View**: Click on any TODO card to see full details
- **Filtering**: Use tabs to filter by All, Active, or Completed

### Editing a TODO
1. Click the **"Edit"** button on any TODO card
2. Modify the fields as needed
3. Click **"Update TODO"**

### Marking as Complete
- Click the **"Complete"** button to mark a TODO as done
- Completed TODOs show with a strikethrough and checkmark
- Click **"Reopen"** to mark it as active again

### Deleting a TODO
1. Click the **"Delete"** button
2. Confirm deletion on the confirmation page

## 🏗️ Project Structure

```
todo-app/
├── todo_project/          # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py
├── todos/                # TODO app
│   ├── models.py         # Todo model
│   ├── views.py          # Class-based views
│   ├── forms.py          # TodoForm
│   ├── urls.py           # App URL patterns
│   └── admin.py          # Admin configuration
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   └── todos/
│       ├── todo_list.html
│       ├── todo_detail.html
│       ├── todo_form.html
│       └── todo_confirm_delete.html
├── static/               # Static files
│   └── css/
│       └── style.css     # Modern CSS styling
├── manage.py
├── requirements.txt
└── README.md
```

## 🎨 Features in Detail

### Todo Model Fields
- **Title**: Main task description (required)
- **Description**: Detailed notes (optional)
- **Due Date**: Target completion date (optional)
- **Priority**: Low, Medium, or High
- **Is Resolved**: Completion status
- **Created At**: Auto-timestamp
- **Updated At**: Auto-timestamp

### Priority System
- 🟢 **Low**: Non-urgent tasks
- 🟡 **Medium**: Regular priority (default)
- 🔴 **High**: Urgent tasks

### Visual Indicators
- Completed tasks show with strikethrough
- Overdue tasks highlighted in red
- Priority badges color-coded
- Statistics showing total, active, and completed counts

## 🛠️ Development Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Run tests
python manage.py test

# Deactivate virtual environment
deactivate
```

## 📱 Screenshots

The application features:
- Clean, modern card-based layout
- Responsive design for mobile and desktop
- Smooth animations and transitions
- Intuitive navigation
- Beautiful color scheme

## 🔐 Admin Interface

Access the Django admin panel at http://127.0.0.1:8000/admin/

Features:
- Manage all TODOs
- Search and filter capabilities
- Quick edit for resolved status
- Date hierarchy navigation

## 🤝 Contributing

This is a learning project. Feel free to:
- Add new features
- Improve the UI/UX
- Optimize performance
- Add tests

## 📄 License

This project is open source and available for educational purposes.

## 🎯 Future Enhancements

Potential features to add:
- User authentication (multi-user support)
- Categories/tags for TODOs
- Search functionality
- Pagination for large lists
- Export to CSV/PDF
- Email notifications for due dates
- Dark mode toggle
- Drag-and-drop reordering

## 📞 Support

For issues or questions, please refer to the Django documentation:
- Django Docs: https://docs.djangoproject.com/
- Django Tutorial: https://docs.djangoproject.com/en/5.2/intro/tutorial01/

---

**Built with ❤️ using Django 5.2.8**

