// Purpose: Main entrypoint for bootstrapping the React application.
// Responsibilities: Hooks the root React App component to the index.html template and mounts it in StrictMode.

import { StrictMode } from 'react'

import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
