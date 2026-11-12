import { useQuery } from "@tanstack/react-query";
import { getUserData } from "../api/auth.js";

export const USER_DATA_QUERY_KEY = ["userData"];

export const useUserData = () => {
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: USER_DATA_QUERY_KEY,
    queryFn: getUserData,
    staleTime: 5 * 60 * 1000,
    retry: false,
  });

  return {
    user: data,
    isLoggedIn: !!data,
    isLoading,
    isError,
    refetch,
  };
};
