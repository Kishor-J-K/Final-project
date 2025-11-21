# Audio Classification Web Application

This project is a web application for classifying audio files using a trained deep learning model. The application allows users to upload audio files, which are then processed and classified by the model, returning the predicted class name.

## Project Structure

```
audio-classification-webapp
├── app.py                # Main entry point of the web application
├── requirements.txt      # List of dependencies
├── model
│   └── sound_model.pth   # Trained model weights
├── src
│   ├── inference.py      # Functions for model inference
│   └── utils.py          # Utility functions for audio processing
├── templates
│   └── index.html        # HTML template for the main page
├── static
│   └── style.css         # CSS styles for the web application
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/Kishor-J-K/Final-project.git
   cd Final-project
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python app.py
   ```

5. **Access the web application:**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage Guidelines

- Use the provided form on the main page to upload an audio file in `.wav` format.
- After uploading, the application will process the audio and display the predicted class name.

## Deployment

This application can be deployed to various hosting platforms. The app is configured to work with:

### Railway
1. Push your code to GitHub
2. Go to [Railway](https://railway.app) and create a new project
3. Connect your GitHub repository
4. Railway will automatically detect the Flask app and deploy it

### Render
1. Push your code to GitHub
2. Go to [Render](https://render.com) and create a new Web Service
3. Connect your GitHub repository
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### Heroku
1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Push to Heroku: `git push heroku main`
5. The `Procfile` is already configured

### Important Notes for Deployment
- The model file (`sound_model.pth`) will be included in the repository. If it's very large (>100MB), consider using Git LFS or storing it in cloud storage.
- Ensure your hosting platform supports Python 3.12 (or update `runtime.txt` to match your platform's supported version)
- Some platforms may require additional configuration for audio processing libraries (librosa, pydub)

## Additional Information

- Ensure that the model weights (`sound_model.pth`) are located in the `model` directory.
- Modify the `requirements.txt` file to add any additional libraries as needed for your specific use case.
- The app uses environment variables: `PORT` (for port configuration) and `FLASK_ENV` (for debug mode)
