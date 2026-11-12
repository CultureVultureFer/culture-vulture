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
            <p3 className="p3">CultureVulture</p3>
            <p1>Culture from a bird's eye view.</p1>
            <p2>Discover what's happening near you, all in one place.</p2>
            </div>
            </div>
            <hr className="line"></hr>
            <p className="temp">&copy; CultureVulture 2026</p>
        </footer>
    )
}
export default Footer