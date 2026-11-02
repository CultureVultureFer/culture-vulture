import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { BrowserRouter, Route, Routes } from "react-router"
import HelloWorld from "./HelloWorld.jsx"
import OrgRegister from "./pages/OrgRegister.jsx"
import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'

const queryClient = new QueryClient();

function App() {
  return (
    <div className='bg-blue-50'>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<App />} />
            <Route path="hello" element={<HelloWorld />} />
            <Route path="org/register" element={<OrgRegister />} />
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </div>
  )
}

export default App
