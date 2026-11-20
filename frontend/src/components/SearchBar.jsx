import "./SearchBar.css";
import { useState } from "react";

function SearchBar({ className = "", onSearch }) {
  const [input, setInput] = useState("");
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch?.(input);
  };

  return (
    <form onSubmit={handleSubmit} className={`sdiv ${className}`.trim()}>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        type="text"
        className="search-input"
        placeholder="Search"
      />
      <button type="submit" className="search-button">
        Search
      </button>
    </form>
  );
}

export default SearchBar;
