import { loginWithGoogle } from "./api/auth";
import { BACKEND_URL } from "./utils/constants";

function HelloWorld() {
  const handleClick = async () => {
    const res = await fetch(`${BACKEND_URL}/auth/me`);
    console.log(await res.json());
  };

  return <button onClick={loginWithGoogle}>Log in with Google...</button>;
}
export default HelloWorld;
