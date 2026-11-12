import { useEffect, useState } from "react";
import "./Events.css";

function Events() {
    const[events, setEvents] = useState([])
    const[loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function getEvents() {
            try{
           const response = await fetch("/api/events/");

                if(!response.ok){
                    throw new Error("Failed to load events");
                }
                const data = await response.json();
                setEvents(data);
            }
            catch(error){
                setError(error.message);
            }
            finally {
                setLoading(false);
            }
        }
        getEvents();
    }, []);
    if (loading){
        return <p>Loading...</p>;
    }
    if (error){
        return <p>Error: {error}</p>;
    }


    return(
        <div className="evdiv1">
            {events.map((event) => (
                <div className="evdiv2" key={event.event_id}>
                    <h2>{event.event_name}</h2>

                     <p>{event.event_description}</p>

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
                        {event.entry_price !== null
                            ?
                            <>
                            {event.entry_price} {event.price_currency}
                            </>
                            : "Price unknown"}
                    </p>

                    </div>
            ))}
        </div>

    );







}

export default Events;