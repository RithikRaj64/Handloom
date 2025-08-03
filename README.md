## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/RithikRaj64/Handloom.git
cd Handloom
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## 💿 How to run the app

### 1. Ensure the environment is activated

```bash
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Start the fastapi app from the terminal

```bash
fastapi run ./app.py
```

> The fastapi application will be running on http://0.0.0.0:8000. The documentation of the api will be running on http://0.0.0.0:8000/docs.