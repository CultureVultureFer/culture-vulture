import "../components/Header.css";
import {} from "react-router";
import logo1 from "../assets/logo1.svg";

//to be added: functional link for organizer and my events
export default function OrganizerHeader({ current }) {
  return (
    <header className="header">
      <div className="hdiv2">
        <img src={logo1} alt="CultureVulture" className="logo1" />
        <nav className="p1 flex gap-2">
          <span>organizer</span>
          <span>/</span>
          <span>my events</span>
          <span>/</span>
          <span>{current}</span>
        </nav>
      </div>
    </header>
  );
}
