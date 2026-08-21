# dangokobox.com

Catálogo mayorista Flask de dangoko, conectado a Supabase y preparado para Railway.

## Vista en vivo

[![Abrir dangokobox.com](https://img.shields.io/badge/VER%20SITIO%20EN%20VIVO-000000?style=for-the-badge&logo=railway&logoColor=white)](https://dangokobox.com/)

[![Vista previa de dangoko](docs/buldakshop-vercel.png)](https://dangokobox.com/)

## Estructura

- `backend/`: API Flask, checkout demo y acceso a Supabase.
- `frontend/`: plantillas, estilos, JavaScript e imágenes.
- `supabase/migrations/`: esquema y datos iniciales del catálogo.

La raíz `app.py` es el punto de entrada WSGI. Railway ejecuta Gunicorn según `railway.json` y valida cada despliegue en `/api/health`.

## Despliegue en Railway

1. Crea un proyecto desde este repositorio de GitHub.
2. Railway detectará `railway.json`, instalará `requirements.txt` e iniciará `gunicorn app:app` en el puerto asignado.
3. Agrega `dangokobox.com` como dominio personalizado en el servicio.
4. Copia exactamente los registros CNAME y TXT que Railway muestre a la zona DNS de Cloudflare. No inventes ni reutilices valores de otro proyecto.
5. Mantén el CNAME de la raíz con proxy de Cloudflare y crea `www` como CNAME hacia `dangokobox.com` si deseas servir ambas variantes.

## Desarrollo local

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python app.py
```

Copia `.env.example` a un archivo local ignorado por Git y agrega las variables públicas de Supabase para usar la base remota durante el desarrollo. Sin esas variables, la aplicación usa el mismo catálogo incluido como respaldo local.
