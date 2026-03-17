# NutriCalc — Recipe Nutritional Calculator

A unified Django web application that allows users to manage a comprehensive ingredient database and create recipes with real-time nutritional calculations and an AI-powered Health Score. It handles CRUD operations for both ingredients and recipes, and features live ingredient autocomplete.

---

### Start the Application
```powershell
cd nutri_calc
..\venv\Scripts\python manage.py runserver
```
Open → **http://localhost:8000**

---

## Admin Panel

Create a superuser to access the Django admin panel:

```powershell
cd nutri_calc
..\venv\Scripts\python manage.py createsuperuser
```
→ http://localhost:8000/admin/

---

## Project Structure

```text
WEB APP KAY SIR RM/
├── venv/                  ← Shared virtual environment
├── README.md              ← Project documentation
├── requirements.txt       ← Python dependencies
└── nutri_calc/            ← Main Django Project
    ├── db.sqlite3         ← Unified SQLite database
    ├── manage.py          
    ├── nutri_calc/        ← Project settings and main urls
    ├── ingredients/       ← App for Ingredient models, views, and APIs
    │   ├── models.py
    │   ├── views.py       (CRUD + /api/calculate/ + /api/ingredients/)
    │   └── ...
    ├── recipes/           ← App for Recipe models and views
    │   ├── models.py
    │   ├── views.py       (CRUD + AI guide)
    │   └── ...
    ├── templates/         ← Global and app-specific templates
    └── static/            ← Static CSS and JS assets
```

---

## Features

- **Ingredient (`ingredients` app)**: Browse, search, add, edit, delete ingredients with full macronutrient data (calories, protein, carbs, fat, fiber, sugar, sodium). Dozens of ingredients are pre-seeded.
- **Cookbook (`recipes` app)**: Create, view, edit, delete recipes. On the recipe detail page, nutrition is calculated directly from the database and displayed. The **AI Nutrition Guide** provides:
  - 🏥 Health Score (0–100)
  - Tips for balanced macros
  - Warnings for high sodium/fat/calories
  - Suggestions for ingredient substitutions
- **Autocomplete**: When adding ingredients to a recipe, a live dropdown fetches and suggests names from the unified Ingredient DB.
