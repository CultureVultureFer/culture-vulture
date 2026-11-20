import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { BrowserRouter, Route, Routes } from "react-router";
import HomePage from "./pages/homepage/HomePage.jsx";
import Login from "./pages/Login.jsx";
import RegisterOrg from "./pages/RegisterOrg.jsx";
import EventFormPage from "./pages/EventFormPage.jsx";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Authenticated,
  CsrfGuard,
  GuestOnly,
} from "./components/RouteGuards.jsx";
import EventPage from "./pages/EventPage/EventPage.jsx";

const queryClient = new QueryClient();
function App() {
  return (
    <div className="w-full h-screen bg-primary-background">
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route element={<CsrfGuard />}>
              <Route element={<GuestOnly />}>
                <Route path="login" element={<Login />} />
                <Route path="org/register" element={<RegisterOrg />} />
              </Route>

              <Route element={<Authenticated />}>
                <Route path="/" element={<HomePage />} />
                <Route path="hello" element={<HomePage />} />
                <Route path="events/:id" element={<EventPage />} />
              </Route>

              <Route element= {<Authenticated role="ORGANIZER" />}>
                <Route path="organizer/events/new" element={<EventFormPage />} />
                <Route path="organizer/events/:id/edit" element={<EventFormPage />} />
              </Route>
            </Route>
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </div>
  );
}

export default App;
