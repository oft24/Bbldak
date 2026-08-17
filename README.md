# BuldakShop

Interactive Flask shop with product-specific Buldak details, cooking directions, serving photography and pairing recommendations.

## Local development

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python app.py
```

Open `http://127.0.0.1:5000`.

## Vercel

The root `app.py` exports the Flask WSGI application Vercel detects automatically.
Static files live in `public/` so Vercel can serve them from its CDN.
