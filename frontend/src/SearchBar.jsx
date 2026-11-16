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
                    <button className="search-button">
        Search
      </button>
        </div>



        
        </>
    )
}

export default SearchBar;