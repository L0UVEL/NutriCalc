# How to Update NutriCalc on PythonAnywhere

Follow these steps to update your deployed web application on PythonAnywhere without changing the overall deployment structure.

## Step 1: Push Local Changes to GitHub
Ensure all your local changes (including the new `admin.py` configurations and any other updates) are committed and pushed to your GitHub repository.

```powershell
git add .
git commit -m "Update NutriCalc: Added admin configs and teacher account"
git push origin main
```

## Step 2: Pull Changes on PythonAnywhere
1. Log in to your [PythonAnywhere Dashboard](https://www.pythonanywhere.com/).
2. Open a **Bash Console**.
3. Navigate to your project directory.
4. Pull the latest code:

```bash
cd ~/WEB-APP-KAY-SIR-RM
git pull origin main
```

## Step 3: Update Dependencies (If needed)
If you added any new packages to `requirements.txt`:

```bash
# Activate your virtualenv (usually something like venv or your-app-name)
source venv/bin/activate
pip install -r requirements.txt
```

## Step 4: Apply Database Migrations
Run migrations to ensure the database schema matches your models.

```bash
cd ~/WEB-APP-KAY-SIR-RM/nutri_calc
python manage.py makemigrations
python manage.py migrate
```

## Step 5: Refresh the Web App
1. Go to the **Web** tab on PythonAnywhere.
2. Find your web app in the list.
3. Click the green **Reload [yourdomain].pythonanywhere.com** button.

---

### Creating the Teacher Account on PythonAnywhere
Since you are on the free tier, you can easiest create it from the Bash console:

1. Open a **Bash Console** on PythonAnywhere.
2. Run the Django shell:
   ```bash
   cd ~/WEB-APP-KAY-SIR-RM/nutri_calc
   python manage.py shell
   ```
3. Copy and paste the following into the shell (make sure there are no leading spaces on the first line):
   ```python
from django.contrib.auth.models import User
if not User.objects.filter(username='sirrm').exists():
    User.objects.create_superuser('sirrm', 'rommelmanuquil.rm@gmail.com', 'P@ssword123')
    print("Superuser 'sirrm' created!")
else:
    u = User.objects.get(username='sirrm')
    u.set_password('P@ssword123')
    u.save()
    print("Password updated for 'sirrm'!")
exit()
   ```

> [!TIP]
> If you get an `IndentationError`, it's usually because some extra spaces were included at the beginning of the lines when pasting. Try copying the code again, or type the lines one by one.
