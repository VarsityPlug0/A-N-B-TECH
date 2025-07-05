@echo off
REM iPhone Store Git Setup Script for Windows
REM This script helps set up the Git repository for the iPhone Store project

echo 🚀 Setting up Git repository for iPhone Store...

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

REM Initialize Git repository (if not already initialized)
if not exist ".git" (
    echo 📁 Initializing Git repository...
    git init
) else (
    echo ✅ Git repository already initialized
)

REM Add all files to Git
echo 📝 Adding files to Git...
git add .

REM Create initial commit
echo 💾 Creating initial commit...
git commit -m "feat: initial commit - iPhone Installment Store

- Complete Django application for iPhone installment management
- Document upload and verification system
- User registration and authentication
- Admin interface for application management
- Email notifications and security features
- Responsive Bootstrap UI
- Management commands for data setup"

REM Add remote repository (user needs to update URL)
echo 🔗 Setting up remote repository...
echo Please update the remote URL with your GitHub repository:
echo git remote add origin https://github.com/yourusername/iphone-store.git
echo.
echo Then push to GitHub:
echo git push -u origin main
echo.
echo ✅ Git setup complete!
echo.
echo 📋 Next steps:
echo 1. Create a new repository on GitHub
echo 2. Update the remote URL above
echo 3. Push your code to GitHub
echo 4. Set up GitHub Actions (optional)
echo 5. Configure deployment settings
pause 