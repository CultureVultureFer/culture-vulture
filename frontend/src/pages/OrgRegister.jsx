import { Button, Grid, TextField } from "@mui/material";
import { Link } from "react-router"
import { Controller, useForm } from "react-hook-form";

function TextInput({ error, label, ...field }) {
  return <TextField error={!!error} helperText={error?.message} label={label} variant="standard" size="small" {...field} />
}

function OrgRegister() {
  const { handleSubmit, formState: { errors }, control } = useForm({
    defaultValues: {
      name: "",
      email: "",
      password: "",
      passwordrepeated: ""
    }
  });

  const onSubmit = (data) => {
    console.log(data)
  }

  return (
    <div className="flex flex-col gap-2 items-center justify-center self-center h-screen">
      <form onSubmit={handleSubmit(onSubmit)} className="text-xl justify-center bg-white border-blue-700 border-2 flex flex-col gap-5 p-5 shadow-blue-300 shadow-md w-100 rounded-md">
        <h1 className="text-blue-700 text-center">Organizator Sign Up</h1>
        <Controller rules={{ required: "Organization name is required" }} name="name" control={control} render={
          ({ field }) => <TextInput error={errors.name} label="Organization name" {...field} ></TextInput>} />
        <Controller rules={{ required: "Organization email is required" }} name="email" control={control} render={
          ({ field }) => <TextInput error={errors.email} label="Organization email" {...field} />} />
        <Controller rules={{ required: "Organization password is required" }} name="password" control={control} render={
          ({ field }) => <TextInput error={errors.password} label="Password" {...field} />} />
        <Controller rules={{ required: "Organization password confirmation is required" }} name="passwordrepeated" control={control} render={
          ({ field }) => <TextInput error={errors.passwordrepeated}
            label="Password confirmation" {...field} />} />
        <Grid container>
          <Grid size={8}>
            <Link className="text-xs text-blue-500 underline" to="/org/signin">Already have an account? Sign In here</Link>
          </Grid>
          <Grid offset={"auto"}>
            <Button type="submit" sx={{ backgroundColor: "var(--color-blue-500)", color: "white" }} color="primary" className="self-end bg-blue-50">Sign Up</Button>
          </Grid>
        </Grid>
        <Link to="/signup" className="text-sm text-blue-500 underline">Looking for normal user sign up?</Link>
      </form>
    </div>
  );
}

export default OrgRegister;


