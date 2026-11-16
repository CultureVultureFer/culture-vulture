import { useNavigate } from "react-router";
import "./Events.css";

function Events({ isError, isLoading, error, data }) {
  const navigate = useNavigate();

  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (isError) {
    const message = error.response?.data?.error ?? error.message;
    return <p>Error: {message}</p>;
  }
  return (
    <div className="evdiv1">
      {data.data.map((event) => (
        <div className="evdiv2" key={event.event_id}>
          <h2>{event.event_name}</h2>

          {/*<p>{event.event_description}</p>*/}

          <p>
            <strong>Date: </strong>
            {new Date(event.start).toLocaleDateString()}
          </p>

          <p>
            <strong>Location: </strong>
            {event.location}
          </p>

          <p>
            <strong>Price: </strong>
            {event.entry_price !== null ? (
              <>
                {event.entry_price} {event.price_currency}
              </>
            ) : (
              "Price unknown"
            )}
          </p>
          <button className="buttons" onClick={() => navigate(`/events/${event.event_id}`)}>Show details</button>
        </div>
      ))}
    </div>
  );
}

export default Events;
