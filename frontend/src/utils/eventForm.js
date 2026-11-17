const pad = (n) => String(n).padStart(2, "0");

export function toApiDateTime(date, time) {
    const dateFormat = `${date}T${time}`;
    return new Date(dateFormat).toISOString();
}

export function fromApiDateTime(iso) {
    const dateIso = new Date(iso);
    const date = `${dateIso.getFullYear()}-${pad(dateIso.getMonth() + 1)}-${pad(dateIso.getDate())}`;
    const time = `${pad(dateIso.getHours())}:${pad(dateIso.getMinutes())}`;
    return { date, time };
}

export function toPayload(form) {
    return {
        event_name: form.event_name,
        event_description: form.event_description || null,
        category_ids: [Number(form.category_id)],
        start: toApiDateTime(form.start_date, form.start_time),
        end: toApiDateTime(form.end_date, form.end_time),
        location: form.location,
        entry_price: (form.entry_price == null || form.entry_price === "") ? null : form.entry_price,
    };
}

export function toFormValues(event) {
    const start = fromApiDateTime(event.start);
    const end = fromApiDateTime(event.end);
    return {
        event_name: event.event_name,
        event_description: event.event_description ?? "",
        category_id: event.categories[0]?.id ?? "",
        start_date: start.date,
        start_time: start.time,
        end_date: end.date,
        end_time: end.time,
        location: event.location ?? "",
        entry_price: event.entry_price ?? "",
    };
}
const FIELD_MAP = {
    category_ids: "category_id",
    start: "start_date",
    end: "end_date",
};
export function applyServerErrors(error, setError) {
    const data = error?.response?.data;
    if (error?.response?.status !== 400 || !data) return false;
    for (const [field, messages] of Object.entries(data)) {
        setError(FIELD_MAP[field] ?? field, { type: "server", message: [].concat(messages)[0] });
    }
    return true;
}

