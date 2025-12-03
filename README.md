# Live Scream Detection App

**Short description**
A Flask-based web application that detects screams from audio (file uploads and live microphone recordings). When a scream is detected, the app saves the audio, logs detection metadata (confidence, timestamp, location) to PostgreSQL, and automatically sends the user's live location to a configured WhatsApp number. Includes a dashboard for viewing detections, managing users, and reviewing recorded audio.

---

## Key Features

* Detect screams from audio files (upload) and from live microphone recordings (5-second automatic recordings).
* Uses a trained ML model (TensorFlow/PyTorch — replace with your model file) for scream classification.
* Saves audio files to `recordings/` (configurable folder).
* Logs detection events to PostgreSQL (timestamp, confidence, latitude, longitude, audio path, user id).
* Sends alert (location + optional audio link) to a WhatsApp number when a scream is detected.
* User authentication (signup/login with phone number) and a simple admin dashboard.
* Dashboard: list detections, listen to saved clips, filter by confidence/time.

---

## Tech Stack

* Backend: Flask
* ML: TensorFlow / Keras (or PyTorch — configure accordingly)
* Audio capture: PyAudio (for server-side microphone) or browser JS recorder (if used)
* Database: PostgreSQL
* Messaging: WhatsApp API / Twilio / 3rd-party integration (configurable)
* Frontend: HTML, CSS, JavaScript (basic templates), Bootstrap (optional)

---

## Prerequisites

* Python 3.8+ (recommend 3.9 or 3.10)
* PostgreSQL instance
* `ffmpeg` installed on the server (for audio conversions)
* If using server-side mic capture: system audio input and `PyAudio`
* A WhatsApp messaging account/credentials (Twilio/Business API or custom webhook)

---

## Install & Setup (Local)

1. Clone the repo

```bash
git clone <https://github.com/mahadev19/Scream-Detection-App>
cd scream-detection-app
```

2. Create and activate a virtual environment

```bash
python -m venv venv
# windows
venv\Scripts\activate
# linux / mac
source venv/bin/activate
```

3. Install Python dependencies

```bash
pip install -r requirements.txt
```

4. Create required folders

```bash
mkdir recordings
mkdir logs
```

5. Database setup

* Create a PostgreSQL database and user.
* Apply migrations (if using Flask-Migrate)

```bash
export DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DBNAME"
flask db upgrade
```

6. Add your model file

Place your trained model in `models/` (for example `models/scream_model.h5`) and update the model path in config.

---

## Configuration (.env)

Create a `.env` file in the project root with the following variables (example):

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=replace_this_with_a_secure_key
DATABASE_URL=postgresql://user:pass@localhost:5432/scream_db
MODEL_PATH=models/scream_model.h5
RECORDINGS_FOLDER=recordings
WHATSAPP_API_URL=https://your-whatsapp-api.example/send
WHATSAPP_TOKEN=your_whatsapp_token_here
DEFAULT_ALERT_NUMBER=+911234567890
SAMPLE_RATE=16000
RECORD_SECONDS=5
MIN_CONFIDENCE=0.6
```

> **Note:** Do not commit `.env` or secrets to version control.

---

## How it Works (high level)

1. **File upload detection** — User uploads an audio file via the web UI. Backend converts/normalizes the audio, runs the model inference, stores the file and logs the event. If confidence >= `MIN_CONFIDENCE`, the WhatsApp alert is triggered.

2. **Live microphone detection** — The server (or browser) records 5-second audio snippets. Each snippet is processed the same as a file upload. On detection, the app fetches the user's current location (from client or server), logs it, and triggers WhatsApp.

3. **WhatsApp alert** — A POST request is sent to the configured WhatsApp API endpoint with the alert payload (number, message, optional audio link). The endpoint and payload format are configurable.

---

## Routes / Endpoints (example)

* `GET /` — Home / info page
* `GET /dashboard` — Admin dashboard (requires auth)
* `POST /upload` — Upload an audio file for detection
* `POST /live-record` — Endpoint to trigger a 5s server-side recording and detection (if using server mic)
* `POST /signup`, `POST /login` — Authentication
* `GET /detections` — List detections (supports filters)
* `GET /audio/<filename>` — Serve saved audio clips (protected)

Adjust routes to match your implementation.

---

## Model Integration

* The project expects a function like `predict_scream(audio_path) -> (label, confidence)` in `app/predict.py` or similar.
* Example pseudocode:

```python
from tensorflow.keras.models import load_model
model = load_model(app.config['MODEL_PATH'])

def predict_scream(wav_path):
    # load audio, convert to model input, run inference
    # return ('scream' / 'no_scream', confidence)
    pass
```

* Ensure you apply the same preprocessing used during model training (sample rate, chunk length, mel spectrogram, normalization, etc.).

---

## WhatsApp Integration (example)

* You can use Twilio's WhatsApp API, an official WhatsApp Business API endpoint, or a third-party service.
* The app makes a POST request to `WHATSAPP_API_URL` with `{ "to": number, "message": message, "media_url": optional_audio_url }` and an Authorization header `Bearer WHATSAPP_TOKEN`.
* For local testing, you may print the payload instead of sending.

---

## File storage & Security

* Store recordings in a folder outside the web root or protect access with authentication.
* Use signed URLs for audio file downloads when exposing them in alerts.
* Limit retention (e.g., remove clips older than X days) and log deletion events.

---

## Deployment tips

* Use a process manager (Gunicorn + systemd / Docker + uwsgi) for running Flask in production.
* If using server-side mic capture, ensure the host has an audio input device and the container (if Dockerized) has access to it.
* Use HTTPS for webhooks and messaging APIs.
* Use environment variables for all secrets and credentials; never bake them into the image.

---

## Troubleshooting

* **Model not loading**: Check `MODEL_PATH` and Python package versions (TensorFlow/PyTorch). Ensure model file matches the framework.
* **PyAudio errors**: Install correct system drivers, use matching wheel for your Python version, or use browser-based recorder to avoid server-side audio capture.
* **WhatsApp message not sent**: Verify credentials, check logs for API response, test the POST payload with `curl`.
* **Permission errors serving audio**: Ensure file permissions and flask route protection are correct.

---

## Project Structure (example)

```
├── app.py
├── requirements.txt
├── models/
│   └── scream_model.h5
├── recordings/
├── templates/
│   ├── index.html
│   └── dashboard.html
├── static/
│   ├── css/
│   └── js/
├── app/
│   ├── routes.py
│   ├── predict.py
│   └── db.py
├── migrations/
└── README.md
```

---

## Testing

* Unit test `predict_scream` with known positive and negative audio samples.
* E2E test: upload sample scream audio via `POST /upload` and confirm detection logged and alert triggered.

---

## Contributing

* Fork the repo, create a feature branch (`feat/your-feature`), commit, and open a PR.
* Keep model changes separate from app logic. Provide sample audio and expected labels for model-related PRs.

---

## License

This project is licensed under the MIT License — change as needed.

---

## Contact

If you need help customizing the README or adding CI/CD, send me details about how you run the app and I will update the docs.
Mahadev Bharat Pandharpote

Contact : gmail:- pandmahadev120@gmail.com

instagram :- https://www.instagram.com/mahadev_p19/

linkedin :- https://www.linkedin.com/in/mahadev-pandharpote-coder-developer/

some Screenshots: 
Lgin/Signup
![d48604e3-0579-4272-a361-744b6ef1007c](https://github.com/user-attachments/assets/61d137a7-788c-4ac2-9200-5a4908a42f55)
![30997500-ae27-4307-a853-3c68f88cd191](https://github.com/user-attachments/assets/e3e0d781-0ba8-4e79-b15e-750ab989d3f4)
Dashboard
![1b5be47e-4300-40ed-ac91-245b8e056c31](https://github.com/user-attachments/assets/d3a58c18-a6ba-4677-b423-2ed97adb2201)
Live Detection
![cc0cca32-f1fc-4dfa-982f-1a7cc8f4d878](https://github.com/user-attachments/assets/534b6740-f9b6-49be-87a3-599fd141476c)
![682b2f2d-5b68-4959-873c-d6631deca01c](https://github.com/user-attachments/assets/2f761747-f6b9-44b2-bdb9-15b218ccd5e8)
![b343f27d-3555-40fa-a75b-b0056df3b6cb](https://github.com/user-attachments/assets/d18f4d23-4d48-4d12-9509-d725c5db2af3)
File Upload
![3f7717b5-e54d-4c79-bf3c-13b8f0cb1a36](https://github.com/user-attachments/assets/056f139b-1f46-4c8e-8789-fce2b83b6684)
![0569c38a-574a-4721-94cd-9c43ca34d4fd](https://github.com/user-attachments/assets/00103865-8858-4094-863e-1981a616bfa6)




