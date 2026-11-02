import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { BrowserRouter, Route, Routes } from "react-router"
import HelloWorld from "./HelloWorld.jsx"
import OrgRegister from "./pages/OrgRegister.jsx"

function App() {
  return (
    <div className='bg-blue-50'>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="hello" element={<HelloWorld />} />
          <Route path="org/register" element={<OrgRegister />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
