import { getNewCsrf } from "../api/auth.js";
import { useQuery } from "@tanstack/react-query";

const getCookie = async () => {
  const csrfCookie = await cookieStore.get("csrftoken");
  const isValid = csrfCookie !== null && csrfCookie?.expires > Date.now();

  if (!isValid) {
    return getNewCsrf();
  }
  return true;
};

export const useCsrf = () => {
  const { isError, isLoading } = useQuery({
    queryKey: ["csrfToken"],
    queryFn: getCookie,
  });

  return { isError, isLoading };
};
