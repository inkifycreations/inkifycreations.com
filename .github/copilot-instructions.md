# Copilot Instructions for Inkify Creations

## What this project is
- A small hybrid app with a vanilla JavaScript SPA frontend plus a Django REST backend.
- Frontend lives in `index.html`, `index.css`, and `app.js` at the repo root.
- Backend lives under `backend/` and exposes REST endpoints under `backend/api/`.
- The backend uses a custom Django user model (`api.models.CustomUser`) keyed by mobile number.

## Key architecture
- `app.js` is the single client-side application engine: routing, cart state, auth, customization UI, and API integration.
- Backend endpoints are mounted under `/api/` in `backend/inkify_backend/urls.py`.
- The backend is primarily responsible for:
  - user registration/login with token auth
  - product listing
  - order creation and tracking
  - authenticated user order history
- Products are seeded by `backend/api/management/commands/seed_products.py` to match the static catalog in `app.js`.

## Data flow and integration points
- Frontend API base: `API_BASE_URL = 'http://localhost:8000/api'` in `app.js`.
- Requests use token auth; backend uses `rest_framework.authentication.TokenAuthentication` in `inkify_backend/settings.py`.
- Main API routes in `backend/api/urls.py`:
  - `auth/register/` → user signup
  - `auth/login/` → user login
  - `auth/register-login/` → combined login/register fallback
  - `products/` → product list
  - `orders/` → place order
  - `orders/track/<tracking_id>/` → order tracking
  - `orders/my/` → authenticated user orders
- Order payloads include `items` with `product_id`, `price`, and `customization` subfields.
- `OrderSerializer` returns order items and a simulated status via `Order.get_simulated_status()`.

## Important conventions
- `CustomUser` identity is mobile-only and mobile must be 10 digits.
- Passwords are expected to be at least 12 characters in registration flows.
- `Product.image` may store either an asset path or an SVG string.
- `OrderItem.customization_data` stores either text or base64 image payloads, and `customization_summary` is a short descriptive string.
- Frontend uses a static `CATALOG` in `app.js` that mirrors backend seeded products; keep these aligned when changing product data.

## Developer workflows
- Backend setup:
  - Create a virtual environment and install `backend/requirements.txt`.
  - Run Django migrations from `backend/` with `python manage.py migrate`.
  - Seed products with `python manage.py seed_products`.
  - Start backend server with `python manage.py runserver`.
- Tests:
  - Run backend API tests from `backend/` with `python manage.py test api`.
- Frontend debugging:
  - Open `index.html` in the browser or serve the root directory via a local static server.
  - Ensure `API_BASE_URL` matches backend host/port (`localhost:8000`).

## What to modify carefully
- Changes to `app.js` routing, auth flow, or cart state can break the SPA navigation and checkout flow.
- Changes to the backend auth endpoints must preserve token generation and mobile validation logic.
- Product catalog updates should be reflected in both `app.js` and `backend/api/management/commands/seed_products.py`.
- Order status is intentionally simulated in `api.models.Order.get_simulated_status()`; this is the source of status values returned by `/orders/track/`.

## Useful files
- `app.js` — core SPA engine and product/cart behavior
- `index.html` — markup for home, product, cart, tracking, auth UI
- `index.css` — styling and responsive theme
- `backend/api/models.py` — custom user, product, order, order item schema
- `backend/api/views.py` — REST API business logic and validation
- `backend/api/tests.py` — existing API integration tests
- `backend/api/management/commands/seed_products.py` — product seed data
- `backend/inkify_backend/settings.py` — Django auth/CORS/DRF config

## Agent guidance
- Prefer working with the frontend as a self-contained SPA before making backend changes.
- If modifying backend behavior, update tests in `backend/api/tests.py` and ensure API routes still match `app.js` expectations.
- Avoid introducing new backend frameworks or heavy libraries; the current stack is vanilla JS + Django REST Framework.
- Treat the project as a single deployable prototype, not a multi-service microservice.
