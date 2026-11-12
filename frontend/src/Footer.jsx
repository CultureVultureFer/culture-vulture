import "./Footer.css"
import logo2 from "./assets/logo2.svg"
function Footer(){
    return (
        <footer>
            <div className="fdiv2">
            <img
            src={logo2}
            alt="CultureVulture2"
            className="logo2"/>
            <div className="fdiv1">
            <p className="p3">CultureVulture</p>
            <p>Culture from a bird's eye view.</p>
            <p>Discover what's happening near you, all in one place.</p>
            </div>
            </div>
            <hr className="line"></hr>
            <p className="temp">&copy; CultureVulture 2026</p>
        </footer>
    )
}
export default Footer