import { Navigate, Outlet } from "react-router";
import { useCsrf } from "../hooks/useCsrf.js";
import { useUserData } from "../hooks/useUserData.js";

const FullScreenMessage = ({ children }) => (
  <div className="flex w-screen h-screen items-center justify-center">
    <p className="text-3xl">{children}</p>
  </div>
);

export const CsrfGuard = () => {
  const { isLoading, isError } = useCsrf();

  if (isLoading) return <FullScreenMessage>Loading...</FullScreenMessage>;
  if (isError)
    return <FullScreenMessage>An error occured...</FullScreenMessage>;

  return <Outlet />;
};

export const Authenticated = ({ role }) => {
  const { user, isLoading, isError } = useUserData();

  if (isLoading) return <FullScreenMessage>Loading...</FullScreenMessage>;
  if (isError)
    return <FullScreenMessage>An error occured...</FullScreenMessage>;

  if (!user) return <Navigate to="/login" replace />;

  if (role && user.role !== role) return <Navigate to="/" replace />;

  return <Outlet />;
};

export const GuestOnly = () => {
  const { user, isLoading, isError } = useUserData();

  if (isLoading) return <FullScreenMessage>Loading...</FullScreenMessage>;
  if (isError)
    return <FullScreenMessage>An error occured...</FullScreenMessage>;

  if (user) return <Navigate to="/" replace />;

  return <Outlet />;
};
