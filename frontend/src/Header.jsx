import "./Header.css"
import logo1 from "./assets/logo1.svg"
import SearchBar from "./SearchBar"

function Header(){

    return(
        <header>



            <div className="hdiv2">
                            
                <img
                src={logo1}
                alt="CultureVulture"
                className="logo1"/>
                <p className="p1">Culture from a bird's eye view.</p>
            </div>
            
            <SearchBar></SearchBar>

            <div className="hdiv1">
                <button id="b1">map</button>
                <button id="b2">sign in</button>
            </div>

            
                
            
            
        </header>
    )
}
export default Header