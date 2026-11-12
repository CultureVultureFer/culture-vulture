import { useState } from "react";
import {
  Button,
  Card,
  Step,
  Stepper,
  Typography,
} from "@material-tailwind/react";
import { Link } from "react-router";
import { registerOrgWithGoogle } from "../api/auth";

const stepStyle = {
  className: "bg-accent-green text-inverse-text",
  activeClassName: "!bg-secondary-foreground !text-primary-text",
  completedClassName: "!bg-primary-foreground",
};

export default function RegisterOrg() {
  const [step, setStep] = useState(0);
  const [orgName, setOrgName] = useState("");

  return (
    <div className="flex w-full h-full justify-center items-center">
      <Card className="w-[40vw] min-w-80 bg-secondary-background p-10 flex flex-col gap-8">
        <div className="flex items-center justify-center gap-4 text-inverse-text">
          <img src="/logo.svg" className="h-16" alt="logo" />
          <div>
            <Typography variant="h3">Become an organizer</Typography>
            <Typography className="text-accent-grey">
              {step === 0 ? "What's your organization called?" : "Almost done!"}
            </Typography>
          </div>
        </div>

        <Stepper
          activeStep={step}
          lineClassName="bg-accent-green"
          activeLineClassName="!bg-primary-foreground"
          className="w-2/3 self-center"
        >
          <Step {...stepStyle}>1</Step>
          <Step {...stepStyle}>2</Step>
        </Stepper>

        {step === 0 ? (
          <>
            <label className="flex flex-col gap-2 text-sm text-accent-grey">
              Organizer name
              <input
                autoFocus
                placeholder="e.g. City Theatre Zagreb"
                className="h-12 rounded-lg bg-primary-background px-4 text-base text-primary-text outline-none focus:ring-2 focus:ring-secondary-foreground"
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
              />
            </label>
            <Button
              size="lg"
              className="bg-secondary-foreground text-primary-text"
              disabled={!orgName.trim()}
              onClick={() => setStep(1)}
            >
              Continue
            </Button>
          </>
        ) : (
          <>
            <Typography className="text-inverse-text text-center">
              Connect a Google account for{" "}
              <span className="text-secondary-foreground font-bold">
                {orgName}
              </span>
            </Typography>
            <Button
              size="lg"
              variant="outlined"
              className="flex items-center justify-center gap-2 bg-white"
              onClick={() => registerOrgWithGoogle(orgName.trim())}
            >
              <img
                src="https://www.material-tailwind.com/logos/logo-google.png"
                alt="google"
                className="h-6 w-6"
              />
              connect with google
            </Button>
            <Button variant="text" color="white" onClick={() => setStep(0)}>
              ← Back
            </Button>
          </>
        )}

        <Link
          to="/login"
          className="text-sm text-center text-accent-grey hover:text-secondary-foreground"
        >
          Already have an account? Sign in
        </Link>
      </Card>
    </div>
  );
}
