import "./Header.css";
import logo1 from "../assets/logo1.svg";
import SearchBar from "./SearchBar";
import { Button } from "@material-tailwind/react";
import { logout } from "../api/auth";
import { useQueryClient } from "@tanstack/react-query";
import { USER_DATA_QUERY_KEY } from "../hooks/useUserData";

function Header() {
  const queryClient = useQueryClient();
  const handleLogout = async () => {
    await logout();
    queryClient.invalidateQueries({
      queryKey: USER_DATA_QUERY_KEY,
    });
  };

  return (
    <header className="header">
      <div className="hdiv2">
        <img src={logo1} alt="CultureVulture" className="logo1" />
        <p className="p1">Culture from a bird's eye view.</p>
      </div>

      <SearchBar></SearchBar>

      <div className="hdiv1 flex gap-3">
        <button className="button">map</button>
        <Button size="sm" onClick={handleLogout}>
          Log out
        </Button>
      </div>
    </header>
  );
}
export default Header;
