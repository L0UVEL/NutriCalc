# NutriCalc — Recipe Nutritional Calculator

Two connected Django web apps: **App A (Ingredient DB)** and **App B (Cookbook)**. App B calls App A's REST API to calculate full nutrition for any saved recipe.

---

## Setup (already done — just run the servers)

A shared `venv/` is located in the root `WEB APP KAY SIR RM/` folder.

### Start App A — Ingredient DB (port 8000)
```powershell
cd ingredient_db
..\venv\Scripts\python manage.py runserver 8000
```
Open → **http://localhost:8000**

### Start App B — Cookbook (port 8001)
Open a **second terminal**, then:
```powershell
cd cookbook
..\venv\Scripts\python manage.py runserver 8001
```
Open → **http://localhost:8001**

> ⚠️ App A **must be running** for nutrition calculations and ingredient autocomplete to work in App B.

---

## API Endpoints (App A)

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/ingredients/?q=chicken` | Search ingredients for autocomplete |
| POST | `/api/calculate/` | Calculate nutrition from ingredient list |

**POST `/api/calculate/` body:**
```json
{
  "ingredients": [
    {"name": "Chicken Breast (cooked)", "quantity_g": 150},
    {"name": "Broccoli", "quantity_g": 80}
  ]
}
```

---

## Admin Panels

Create superuser for each app separately:

**App A admin:**
```powershell
cd ingredient_db
..\venv\Scripts\python manage.py createsuperuser
```
→ http://localhost:8000/admin/

**App B admin:**
```powershell
cd cookbook
..\venv\Scripts\python manage.py createsuperuser
```
→ http://localhost:8001/admin/

---

## Project Structure

```
WEB APP KAY SIR RM/
├── venv/                  ← Shared virtual environment
├── ingredient_db/         ← App A (port 8000)
│   ├── ingredients/       ← Django app with Ingredient model + REST API
│   │   ├── models.py
│   │   ├── views.py       (CRUD + /api/calculate/ + /api/ingredients/)
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── management/commands/seed_ingredients.py
│   ├── templates/
│   └── static/css/style_a.css
│
└── cookbook/              ← App B (port 8001)
    ├── recipes/            ← Django app with Recipe + RecipeIngredient models
    │   ├── models.py
    │   ├── views.py        (CRUD + AI Guide + calls App A API)
    │   ├── forms.py
    │   └── urls.py
    ├── templates/
    └── static/css/style_b.css
```

---

## Features

- **App A**: Browse, search, add, edit, delete ingredients with full macronutrient data (calories, protein, carbs, fat, fiber, sugar, sodium). 66 ingredients pre-seeded.
- **App B**: Create, view, edit, delete recipes. On the recipe detail page, nutrition is fetched live from App A and displayed. The **AI Nutrition Guide** provides:
  - 🏥 Health Score (0–100)
  - Tips for balanced macros
  - Warnings for high sodium/fat/calories
  - Suggestions for ingredient substitutions
- **Autocomplete**: When adding ingredients to a recipe, a live dropdown suggests names from the Ingredient DB.
