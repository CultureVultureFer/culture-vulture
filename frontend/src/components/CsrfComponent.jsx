import { useCsrf } from "../hooks/useCsrf";

export const CsrfComponent = ({ children }) => {
  const { isError, isLoading } = useCsrf();

  return (
    <>
      {isLoading ? (
        <div className="flex w-screen h-screen items-center justify-center">
          <p className="text-3xl">Loading...</p>
        </div>
      ) : (
        <>
          {isError ? (
            <div className="flex w-screen h-screen items-center justify-center">
              <p className="text-3xl">An error occured...</p>
            </div>
          ) : (
            <>{children}</>
          )}
        </>
      )}
    </>
  );
};
