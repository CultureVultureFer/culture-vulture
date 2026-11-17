import Header from "../../components/Header.jsx";
import Footer from "../../components/Footer.jsx";
import Filters from "./Filters";
import Events from "./Events";
import { useQuery } from "@tanstack/react-query";
import { getEvents } from "../../api/events.js";

function HomePage() {
  const { data, isLoading, isError, error, isSuccess } = useQuery({
    queryKey: ["events"],
    queryFn: getEvents,
  });

  return (
    <>
      <Header></Header>

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
