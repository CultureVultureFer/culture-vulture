import { Button } from "@material-tailwind/react";
import { loginWithGoogle } from "../api/auth";

export default function Login() {
  return (
    <div className="flex w-full h-full justify-center items-center">
      <div
        className="w-[50vw] h-[50vh] bg-secondary-background pt-14 shadow-2xl shadow-black rounded-sm
        flex flex-col items-center gap-20"
      >
        <div className="text-inverse-text flex gap-4 justify-center items-center">
          <img src="./logo.svg" className="h-20"></img>
          <div>
            <h1 className="text-3xl font-semibold">Welcome!</h1>
            <p className="text-xl">Sign in or make an account!</p>
          </div>
        </div>
        <Button
          variant="outlined"
          size="lg"
          className="flex h-12 items-center justify-center gap-2 self-center bg-white p-5 rounded-sm"
          onClick={loginWithGoogle}
        >
          <img
            src={`https://www.material-tailwind.com/logos/logo-google.png`}
            alt="google"
            className="h-6 w-6"
          />{" "}
          sign in with google
        </Button>
      </div>
    </div>
  );
}
