import CalendarIcon from "./CalendarIcon";
import './EventLocation.css';
import MapPlaceholder from './../../assets/map-placeholder.png'

function EventLocation({ eventData }){

    return(
        <section className="event-location-container">
            <h2 className="event-location-name">Event location</h2>
            <div className="event-location-map">
                <img src={MapPlaceholder} alt="Map location" />
            </div>
            <p className="event-full-adress">{eventData.fullLocation}</p>
            <button className="add-to-calendar-btn"><CalendarIcon /> Add to Google Calendar</button>
        </section>

    );
}

export default EventLocation;