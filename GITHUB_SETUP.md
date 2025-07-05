# GitHub Setup Guide for iPhone Store

This guide will help you push your iPhone Store project to GitHub and set up all the necessary configurations.

## 🚀 Quick Setup

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name it `iphone-store`
5. Make it public or private (your choice)
6. **Don't** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

### 2. Initialize Local Git Repository

#### On Windows:
```bash
# Run the setup script
scripts\setup_git.bat
```

#### On macOS/Linux:
```bash
# Make the script executable
chmod +x scripts/setup_git.sh

# Run the setup script
./scripts/setup_git.sh
```

#### Manual Setup:
```bash
# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "feat: initial commit - iPhone Installment Store

- Complete Django application for iPhone installment management
- Document upload and verification system
- User registration and authentication
- Admin interface for application management
- Email notifications and security features
- Responsive Bootstrap UI
- Management commands for data setup"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/iphone-store.git

# Push to GitHub
git push -u origin main
```

## 📁 Files Added for GitHub

### Core Files
- ✅ `.gitignore` - Excludes sensitive and unnecessary files
- ✅ `README.md` - Comprehensive project documentation
- ✅ `LICENSE` - MIT License
- ✅ `requirements.txt` - Python dependencies
- ✅ `CHANGELOG.md` - Version history and changes

### Docker Support
- ✅ `Dockerfile` - Container configuration
- ✅ `docker-compose.yml` - Multi-container setup
- ✅ `.dockerignore` - Docker build exclusions

### CI/CD
- ✅ `.github/workflows/ci.yml` - GitHub Actions workflow
- ✅ `CONTRIBUTING.md` - Contribution guidelines

### Scripts
- ✅ `scripts/setup_git.sh` - Linux/macOS Git setup
- ✅ `scripts/setup_git.bat` - Windows Git setup

## 🔧 Configuration

### Environment Variables
Create a `.env` file in your project root:
```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/iphone_store

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### GitHub Repository Settings

1. **Go to Settings** in your GitHub repository
2. **Pages** (if you want GitHub Pages):
   - Source: Deploy from a branch
   - Branch: main
   - Folder: / (root)

3. **Secrets** (for CI/CD):
   - Go to Settings → Secrets and variables → Actions
   - Add repository secrets for production deployment

## 🚀 Deployment Options

### Option 1: Heroku
1. Install Heroku CLI
2. Create Heroku app:
   ```bash
   heroku create your-app-name
   ```
3. Add PostgreSQL:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```
4. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```

### Option 2: Railway
1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Deploy automatically on push

### Option 3: DigitalOcean App Platform
1. Connect your GitHub repository
2. Configure environment variables
3. Deploy with automatic updates

## 🔒 Security Checklist

Before pushing to GitHub, ensure:

- [ ] No sensitive data in code (passwords, API keys)
- [ ] `.env` file is in `.gitignore`
- [ ] `db.sqlite3` is in `.gitignore`
- [ ] No hardcoded secrets in code
- [ ] Environment variables properly configured
- [ ] Security settings enabled in Django

## 📊 GitHub Features to Enable

### 1. Issues
- Enable issues in repository settings
- Set up issue templates for bugs and features

### 2. Projects
- Create a project board for task management
- Set up automation rules

### 3. Discussions
- Enable discussions for community engagement
- Create categories for different topics

### 4. Wiki
- Enable wiki for detailed documentation
- Create pages for setup, deployment, etc.

## 🧪 Testing Before Push

### Local Testing
```bash
# Run Django tests
python manage.py test

# Check for linting issues
pip install flake8
flake8 .

# Security check
pip install bandit
bandit -r .
```

### Docker Testing
```bash
# Build and test Docker image
docker build -t iphone-store .
docker run -p 8000:8000 iphone-store
```

## 📈 Monitoring and Analytics

### GitHub Insights
- Go to Insights tab in your repository
- Monitor traffic, clones, and views
- Track contributor activity

### Code Quality
- Enable Dependabot for security updates
- Set up code scanning with CodeQL
- Configure branch protection rules

## 🎯 Next Steps

1. **Push to GitHub** using the setup scripts
2. **Set up GitHub Actions** for CI/CD
3. **Configure deployment** to your preferred platform
4. **Add collaborators** if working with a team
5. **Set up monitoring** and analytics
6. **Create releases** for version management

## 🆘 Troubleshooting

### Common Issues

**Git authentication error:**
```bash
# Use personal access token
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/iphone-store.git
```

**Django settings error:**
- Ensure all environment variables are set
- Check `DEBUG` setting for production

**Docker build fails:**
- Check Dockerfile syntax
- Ensure all dependencies are in requirements.txt

**GitHub Actions fail:**
- Check workflow syntax
- Ensure all secrets are configured
- Verify Python version compatibility

## 📞 Support

If you encounter issues:

1. Check the [GitHub documentation](https://docs.github.com/)
2. Review [Django deployment guide](https://docs.djangoproject.com/en/stable/howto/deployment/)
3. Create an issue in your repository
4. Ask questions in GitHub Discussions

---

**Happy coding! 🚀**

Your iPhone Store project is now ready for GitHub and deployment! 