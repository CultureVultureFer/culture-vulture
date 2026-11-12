import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { BrowserRouter, Route, Routes } from "react-router";
import HelloWorld from "./HelloWorld.jsx";
import Login from "./pages/Login.jsx";
import RegisterOrg from "./pages/RegisterOrg.jsx";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Authenticated,
  CsrfGuard,
  GuestOnly,
} from "./components/RouteGuards.jsx";

const queryClient = new QueryClient();

function App() {
  return (
    <div className="w-screen h-screen bg-primary-background">
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route element={<CsrfGuard />}>
              <Route element={<GuestOnly />}>
                <Route path="login" element={<Login />} />
                <Route path="org/register" element={<RegisterOrg />} />
              </Route>

              <Route element={<Authenticated />}>
                <Route path="/" element={<HelloWorld />} />
                <Route path="hello" element={<HelloWorld />} />
              </Route>
            </Route>
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </div>
  );
}

export default App;
