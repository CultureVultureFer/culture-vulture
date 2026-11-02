import { Button, Grid, TextField } from "@mui/material";
import { Link, useNavigate } from "react-router";
import { Controller, useForm } from "react-hook-form";
import { useMutation } from "@tanstack/react-query";

function TextInput({ error, label, type = "text", ...field }) {
  return (
    <TextField
      type={type}
      error={!!error}
      helperText={error?.message}
      label={label}
      variant="standard"
      size="small"
      {...field}
    />
  );
}

const mockedOkRequest = () =>
  new Promise((resolve) => setTimeout(() => resolve({ ok: true }), 2000));
const mockedErrorRequest = () =>
  new Promise((_, reject) =>
    setTimeout(
      () =>
        reject({ error: true, message: "Org with that name already exists" }),
      2000,
    ),
  );

function OrgRegister() {
  const navigate = useNavigate();
  const mutation = useMutation({
    mutationFn: mockedOkRequest,
    onSuccess: () => navigate("/hello"),
  });
  const {
    handleSubmit,
    formState: { errors },
    control,
  } = useForm({
    defaultValues: {
      name: "",
      email: "",
      password: "",
      passwordrepeated: "",
    },
  });

  const onSubmit = (data) => {
    mutation.mutate(data);
  };

  return (
    <div className="flex flex-col gap-2 items-center justify-center self-center h-screen">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="text-xl justify-center content-center bg-white border-blue-700 border-2 flex flex-col gap-5 p-5 shadow-blue-300 shadow-md w-100 rounded-md"
      >
        <h1 className="text-blue-700 text-center">Organizator Sign Up</h1>
        {mutation.isError && (
          <p className="text-red-600 self-center text-sm p-2 border-red-400 border-2 rounded-md shadow-red-300 shadow-sm">
            An error occured... Please try again
          </p>
        )}
        <Controller
          rules={{ required: "Organization name is required" }}
          name="name"
          control={control}
          render={({ field }) => (
            <TextInput
              error={errors.name}
              label="Organization name"
              {...field}
            ></TextInput>
          )}
        />
        <Controller
          rules={{
            required: "Organization email is required",
            validate: {
              isEmail: (email) => {
                const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!email.match(pattern))
                  return "Please provide a valid email";
              },
            },
          }}
          name="email"
          control={control}
          render={({ field }) => (
            <TextInput
              error={errors.email}
              label="Organization email"
              type="email"
              {...field}
            />
          )}
        />
        <Controller
          rules={{
            required: "Organization password is required",
            validate: {
              strongEnoguh: (password) => {
                const uppercase = /[A-Z]/.test(password);
                const lowercase = /[a-z]/.test(password);
                const special = /[@$!%*#?&]/.test(password);
                const digit = /\d/.test(password);
                const long = password.length >= 8;
                if (!long) return "Password must be at least 8 characters long";
                if (!uppercase)
                  return "Password must contain at least one uppercase letter";
                if (!lowercase)
                  return "Password must contain at least one lowercase letter";
                if (!special)
                  return "Password must contain at least one speccial letter (@,$,!...)";
                if (!digit) return "Password must contain at least one number";
              },
            },
          }}
          name="password"
          control={control}
          render={({ field }) => (
            <TextInput
              error={errors.password}
              label="Password"
              type="password"
              {...field}
            />
          )}
        />
        <Controller
          rules={{
            required: "Organization password confirmation is required",
            validate: {
              passwordsMatch: (passwordrepeated, { password }) => {
                if (passwordrepeated != password) {
                  return "Passwords must match";
                }
              },
            },
          }}
          name="passwordrepeated"
          control={control}
          render={({ field }) => (
            <TextInput
              error={errors.passwordrepeated}
              label="Password confirmation"
              type="password"
              {...field}
            />
          )}
        />
        <Grid container>
          <Grid size={8}>
            <Link className="text-xs text-blue-500 underline" to="/org/signin">
              Already have an account? Sign In here...
            </Link>
          </Grid>
          <Grid offset={"auto"}>
            <Button
              loading={mutation.isPending}
              type="submit"
              sx={{ backgroundColor: "var(--color-blue-500)", color: "white" }}
              color="primary"
              className="self-end bg-blue-50"
            >
              Sign Up
            </Button>
          </Grid>
        </Grid>
        <Link to="/signup" className="text-sm text-blue-500 underline">
          Looking for normal user sign up?
        </Link>
      </form>
    </div>
  );
}

export default OrgRegister;
