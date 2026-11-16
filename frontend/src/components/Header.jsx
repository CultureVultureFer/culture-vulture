import "./Header.css";
import logo1 from "../assets/logo1.svg";
import SearchBar from "./SearchBar";

function Header({isSearchable = true}) {
  return (
    <header className="header">
      <div className="hdiv2">
        <img src={logo1} alt="CultureVulture" className="logo1" />
        <p className="p1">Culture from a bird's eye view.</p>
      </div>
      {isSearchable && 
      <SearchBar></SearchBar>
      }
      <div className="hdiv1">
        <button className="button">map</button>
      </div>
    </header>
  );
}
export default Header;
