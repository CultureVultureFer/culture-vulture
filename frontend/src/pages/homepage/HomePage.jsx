import Header from "../../components/Header.jsx";
import Footer from "../../components/Footer.jsx";
import Filters from "./Filters";
import Events from "./Events";
import { useQuery } from "@tanstack/react-query";
import { getEvents } from "../../api/events.js";
import { useState } from "react";

function HomePage() {
  const [search, setSearch] = useState("");
  const { data, isLoading, isError, error, isSuccess } = useQuery({
    queryKey: ["events", search],
    queryFn: () => getEvents(search),
  });

  return (
    <>
      <Header onSearch={setSearch}></Header>

      <main>
        <Filters></Filters>
        <Events
          data={data}
          error={error}
          isError={isError}
          isLoading={isLoading}
        ></Events>
      </main>

      <Footer isSuccess={isSuccess}></Footer>
    </>
  );
}

export default HomePage;
