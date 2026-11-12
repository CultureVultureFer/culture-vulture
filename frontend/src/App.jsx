import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { BrowserRouter, Route, Routes } from "react-router";
import HelloWorld from "./HelloWorld.jsx";
import Login from "./pages/Login.jsx";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { CsrfComponent } from "./components/CsrfComponent.jsx";

const queryClient = new QueryClient();

function App() {
  return (
    <div className="w-screen h-screen bg-primary-background">
      <QueryClientProvider client={queryClient}>
        <CsrfComponent>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<HelloWorld />} />
              <Route path="hello" element={<HelloWorld />} />
              <Route path="login" element={<Login />} />
            </Routes>
          </BrowserRouter>
        </CsrfComponent>
      </QueryClientProvider>
    </div>
  );
}

export default App;
