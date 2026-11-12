import "./SearchBar.css"
function SearchBar(){
    return(
        <>
        <div className="sdiv">
            <input
            type="text"
            className="search-input"
            placeholder="Search"
            />
        </div>


        <button className="search-button">
        Search
      </button>
        
        </>
    )
}

export default SearchBar;