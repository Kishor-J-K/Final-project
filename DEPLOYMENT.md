# Deployment Guide

This guide will help you deploy your Audio Classification Web Application to various hosting platforms.

## Repository Status
✅ Code is pushed to: https://github.com/Kishor-J-K/Final-project.git

## Quick Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Railway** is the easiest platform for deploying Flask apps with minimal configuration.

#### Steps:
1. Go to [Railway.app](https://railway.app) and sign up/login
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `Kishor-J-K/Final-project`
5. Railway will automatically detect your Flask app
6. Click **"Deploy"** - Railway will:
   - Install dependencies from `requirements.txt`
   - Use the `Procfile` to start your app
   - Assign a public URL automatically
7. Your app will be live at `https://your-app-name.up.railway.app`

**Note:** Railway automatically handles:
- PORT environment variable
- Python version from `runtime.txt`
- Build and deployment process

---

### Option 2: Render

**Render** offers free tier hosting with automatic deployments from GitHub.

#### Steps:
1. Go to [Render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select repository: `Kishor-J-K/Final-project`
4. Configure the service:
   - **Name**: `audio-classification-app` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (or `audio-classification-webapp` if deploying from subdirectory)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Click **"Create Web Service"**
6. Your app will be live at `https://your-app-name.onrender.com`

**Note:** 
- Free tier apps spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Consider upgrading to paid tier for always-on service

---

### Option 3: Heroku

**Heroku** is a popular platform with a free tier (limited hours per month).

#### Prerequisites:
- Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

#### Steps:
1. Login to Heroku:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Set Python buildpack (if not auto-detected):
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. Deploy from GitHub:
   - Go to [Heroku Dashboard](https://dashboard.heroku.com)
   - Select your app
   - Go to **"Deploy"** tab
   - Connect to GitHub repository: `Kishor-J-K/Final-project`
   - Enable **"Automatic deploys"** (optional)
   - Click **"Deploy Branch"**

5. Your app will be live at `https://your-app-name.herokuapp.com`

**Note:**
- Free tier has limited dyno hours (550 hours/month)
- Apps sleep after 30 minutes of inactivity
- Consider upgrading for production use

---

### Option 4: PythonAnywhere

**PythonAnywhere** is great for Python web apps with a free tier.

#### Steps:
1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com) and sign up
2. Go to **"Web"** tab
3. Click **"Add a new web app"**
4. Choose **"Flask"** framework
5. Select Python version: **3.10** (or latest available)
6. Go to **"Files"** tab and clone your repo:
   ```bash
   cd ~
   git clone https://github.com/Kishor-J-K/Final-project.git
   ```
7. Go back to **"Web"** tab:
   - **Source code**: `/home/yourusername/Final-project`
   - **Working directory**: `/home/yourusername/Final-project`
   - **WSGI configuration file**: Edit and set:
     ```python
     import sys
     path = '/home/yourusername/Final-project'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import app as application
     ```
8. Click **"Reload"** button
9. Your app will be live at `https://yourusername.pythonanywhere.com`

---

## Important Notes for All Platforms

### Model File Size
- Your model file (`sound_model.pth`) is 90.14 MB
- This is within GitHub's 100MB limit, but close to the 50MB recommendation
- If you encounter issues, consider:
  - Using Git LFS for the model file
  - Storing the model in cloud storage (S3, Google Cloud Storage) and downloading it at runtime

### Dependencies
All required packages are listed in `requirements.txt`:
- Flask==3.0.3
- torch==2.8.0
- librosa==0.10.2.post1
- numpy==2.1.3
- scikit-learn==1.6.1
- matplotlib==3.10.1
- pydub==0.25.1

### Audio Processing Libraries
Some platforms may require additional system dependencies for audio processing:
- **ffmpeg** (for pydub/librosa)
- Most platforms (Railway, Render, Heroku) include ffmpeg by default
- If you encounter issues, you may need to add a buildpack or install script

### Environment Variables
The app uses these environment variables (all optional):
- `PORT` - Server port (automatically set by hosting platforms)
- `FLASK_ENV` - Set to `development` for debug mode (default: production)

### File Uploads
- Uploaded files are stored in the `uploads/` directory
- On most hosting platforms, this is ephemeral (files are lost on restart)
- For production, consider using cloud storage (AWS S3, Google Cloud Storage, etc.)

---

## Post-Deployment Checklist

After deploying, verify:
- [ ] App loads at the provided URL
- [ ] File upload functionality works
- [ ] Audio recording works (if using browser recording)
- [ ] Model predictions are accurate
- [ ] No errors in platform logs

---

## Troubleshooting

### Build Fails
- Check platform logs for specific error messages
- Verify all dependencies in `requirements.txt` are correct
- Ensure Python version in `runtime.txt` is supported

### App Crashes on Startup
- Check logs for import errors
- Verify model file is present in `model/sound_model.pth`
- Check if all required system libraries are available

### Audio Processing Errors
- Verify ffmpeg is available (most platforms include it)
- Check if uploaded file format is supported
- Review error logs for specific library issues

### Model Loading Errors
- Verify model file path is correct
- Check if model file was uploaded to the platform
- Ensure PyTorch version compatibility

---

## Need Help?

- Check platform-specific documentation
- Review application logs on your hosting platform
- Verify all files are committed and pushed to GitHub

