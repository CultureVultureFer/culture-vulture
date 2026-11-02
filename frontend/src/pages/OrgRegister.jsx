import { Button, Grid, TextField } from "@mui/material";
import { Link } from "react-router"

function OrgRegister() {
  return (
    <div className="flex flex-col gap-2 items-center justify-center self-center h-screen">
      <div className="text-xl justify-center bg-white border-blue-700 border-2 flex flex-col gap-5 p-5 shadow-blue-300 shadow-md w-100 rounded-md">
        <h1 className="text-blue-700 text-center">Organizator Sign Up</h1>
        <TextField size="small" id="org-name" label="Organization name" variant="standard" autoFocus />
        <TextField size="small" id="org-email" label="Organization email" variant="standard" />
        <TextField size="small" id="org-password" label="Password" variant="standard" />
        <TextField size="small" id="org-repeat-password" label="Repeat password" variant="standard" />
        <Grid container>
          <Grid size={8}>
            <Link className="text-xs text-blue-500 underline" to="/org/signin">Already have an account? Sign In here</Link>
          </Grid>
          <Grid offset={"auto"}>
            <Button sx={{ backgroundColor: "var(--color-blue-500)", color: "white" }} color="primary" className="self-end bg-blue-50">Sign Up</Button>
          </Grid>
        </Grid>
      </div>
      <Link to="/signup" className="text-sm text-blue-500 underline">Looking for normal user sign up?</Link>
    </div>
  );
}

export default OrgRegister;


