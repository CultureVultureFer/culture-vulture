import { useParams } from 'react-router';
import EventInfo from './EventInfo';
import EventLocation from './EventLocation';
import EventReview from './EventReview';
import { useQuery } from '@tanstack/react-query';
import { getEvent } from '../../api/events';
import { fromApiDateTime } from '../../utils/eventForm';
import Header from '../../components/Header';
import './EventPage.css'


function EventPage(){

    const { id } = useParams();

    const{ data, isLoading, isError, error } = useQuery({
        queryKey: ["event", id],
        queryFn: () => getEvent(id),
    });

    if (isLoading) {
        return <p>Loading...</p>;
    }

    if (isError) {
        const message = error.response?.data?.error ?? error.message;
        return <p>Error: {message}</p>;
    }

    const { date, time } = fromApiDateTime(data.start);

    // --- dodat endTIme ---
    const eventData = {
        name: data.event_name,
        rating: null,
        reviews: null,
        category: data.categories?.[0]?.name ?? "Uncategorized",
        organizer: data.organizer ?? "Organizer unknown",
        date,
        time,
        fullLocation: data.location,
        price: data.entry_price ?? "Price unknown",
        priceCurrency: data.price_currency ?? "",
        aboutText: data.event_description ?? "No description available"
    }


    return (
    <div className="event-page">
        <Header isSearchable={false} />
        <main className="event-page-content">
            <EventInfo eventData={eventData} />
            <EventLocation eventData={eventData} />
            <EventReview />
            
            
        </main>
    </div>
    );
}

export default EventPage;