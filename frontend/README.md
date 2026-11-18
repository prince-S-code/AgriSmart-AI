# AgriSmart AI Frontend

**Author and Maintainer: Prince Shukla**

This is the React and TypeScript frontend for AgriSmart AI. It provides farmer authentication, the dashboard, crop recommendation, disease image analysis, history, and persistent light/dark themes.

## Development

```powershell
npm install
npm run dev -- --host 127.0.0.1
```

Open http://127.0.0.1:5173.

Set `VITE_API_URL` if the FastAPI backend runs at another address.

## Production Build

```powershell
npm run build
npm run preview
```

## Project Structure

- `src/App.tsx`: application views and farmer workflows
- `src/App.css`: AgriSmart light and dark design system
- `src/api.ts`: FastAPI service calls
- `src/main.tsx`: React entry point

This frontend should communicate with the FastAPI backend rather than loading or processing ML models in the browser.
