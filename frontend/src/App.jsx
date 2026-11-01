import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { CssBaseline } from '@mui/material';
import { BrowserRouter, Route, Routes } from "react-router"
import HelloWorld from "./HelloWorld.jsx"
import Register from "./pages/Register"

function App() {
  return (
    <>
      <CssBaseline />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="hello" element={<HelloWorld />} />
          <Route path="register" element={<Register />} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
