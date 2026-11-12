import { Button, Card, Typography } from "@material-tailwind/react";
import { Link } from "react-router";
import { loginWithGoogle } from "../api/auth";

export default function Login() {
  return (
    <div className="flex w-full h-full justify-center items-center">
      <Card className="w-[40vw] bg-secondary-background py-8 flex items-center gap-5">
        <div className="text-inverse-text flex gap-4 justify-center items-center">
          <img src="./logo.svg" className="h-20"></img>
          <div>
            <Typography variant="h1" className="text-3xl">
              Welcome!
            </Typography>
            <Typography variant="h4">Sign in or make an account!</Typography>
          </div>
        </div>
        <Button
          variant="outlined"
          size="lg"
          className="flex h-12 items-center justify-center gap-2 self-center bg-white"
          onClick={() => loginWithGoogle()}
        >
          <img
            src={`https://www.material-tailwind.com/logos/logo-google.png`}
            alt="google"
            className="h-6 w-6"
          />{" "}
          sign in with google
        </Button>
        <Link
          to="/org/register"
          className="font-medium text-secondary-foreground hover:underline"
        >
          Want to become an organizer? Register here
        </Link>
        <Typography
          variant="small"
          className="text-accent-grey text-center px-8"
        >
          By signing in, you agree to our{" "}
          <a href="#" className="text-secondary-foreground hover:underline">
            Terms of Service
          </a>{" "}
          and{" "}
          <a href="#" className="text-secondary-foreground hover:underline">
            Privacy Policy
          </a>
          .
        </Typography>
        <div className="w-4/5 border-t border-accent-green/50 pt-4 flex justify-between text-xs text-accent-grey">
          <span>© {new Date().getFullYear()} CultureVulture</span>
          <a href="#" className="hover:text-inverse-text">
            Need help?
          </a>
        </div>
      </Card>
    </div>
  );
}
