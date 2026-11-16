import CalendarIcon from './CalendarIcon';
import './EventInfo.css';
import LinkIcon from './LinkIcon';
import MapIcon from './MapIcon';
import ImagePlaceholder from '../../assets/image-placeholder.png'

function EventInfo({ eventData }){

    return (
        <section className="event-container">
            <div className="event-image-placeholder">
                <img className="event-image" src={ImagePlaceholder} alt="Image of event"></img> 
            </div>
            <div className="event-category-and-stars-container">
                <div className="event-category-placeholder">
                    <span className="event-category-name">{eventData.category}</span>
                </div>
                {/* --- Dovrsiti kada budu review dostupan ---
                <div className="event-rating-container">
                    <p className="event-rating">{eventData.rating} ⭐ </p>
                    <p className="event-review-number">({eventData.reviews} {eventData.reviews == 1 ? "review" : "reviews"})</p>
                </div>
                */}
            </div>
            <div className="event-info-container">
                <div className="event-info">
                    <h1 className="event-name">{eventData.name}</h1>
                    <p className="event-organizer">{eventData.organizer}</p>
                    <p className="event-date-and-time"><CalendarIcon />{eventData.date} | {eventData.time}</p>
                    <p className="event-location"><MapIcon />{eventData.fullLocation}</p>
                    <div className="price-and-link-container">
                        <span className="event-price">{eventData.price} {eventData.priceCurrency}</span>
                        <button className="get-tickets-btn"><LinkIcon />Get tickets</button>
                    </div>
                </div>
                <div className="about-event-container">
                    <h3 className="about-event-title">About this event</h3>
                    <p className="about-event-text">{eventData.aboutText}</p>
                </div>
            </div>
        </section>
    )

};




export default EventInfo;