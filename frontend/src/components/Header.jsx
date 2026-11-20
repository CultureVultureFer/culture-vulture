import "./Header.css";
import logo1 from "../assets/logo1.svg";
import SearchBar from "./SearchBar";
import { Button, Chip } from "@material-tailwind/react";
import { logout } from "../api/auth";
import { useQueryClient } from "@tanstack/react-query";
import { USER_DATA_QUERY_KEY, useUserData } from "../hooks/useUserData";
import { useNavigate } from "react-router";

function Header() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { user } = useUserData();

  const handleEventPost = () => {
    navigate("/organizer/events/new");
  };

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

      <div className="hdiv1 flex gap-7 items-center">
        <div>
          <Chip
            size="lg"
            className="text-white"
            value={
              user.role == "ORGANIZER"
                ? `ORG: ${user.organization}`
                : `USER: ${user.username}`
            }
          ></Chip>
        </div>
        {user.role == "ORGANIZER" && (
          <Button size="sm" onClick={handleEventPost}>
            Post Event
          </Button>
        )}
        <Button size="sm" onClick={handleLogout}>
          Log out
        </Button>
      </div>
    </header>
  );
}
export default Header;
