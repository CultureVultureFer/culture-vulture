import Header from "../../components/Header.jsx";
import Footer from "../../components/Footer.jsx";
import Filters from "./Filters";
import Events from "./Events";
import { useQuery } from "@tanstack/react-query";
import { getEvents } from "../../api/events.js";
import { useState } from "react";

function HomePage() {
  const [search, setSearch] = useState("");
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["events", search],
    queryFn: () => getEvents(search),
  });

  return (
    <div className="flex flex-col min-h-screen">
      <Header onSearch={setSearch}></Header>

      <main className="flex-grow">
        <Filters></Filters>
        <Events
          data={data}
          error={error}
          isError={isError}
          isLoading={isLoading}
        ></Events>
      </main>

      <Footer></Footer>
    </div>
  );
}

export default HomePage;
