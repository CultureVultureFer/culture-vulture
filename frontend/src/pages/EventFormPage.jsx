import { Typography } from "@material-tailwind/react";
import { useParams, useNavigate } from "react-router";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getCategories, getEvent, createEvent, updateEvent, deleteEvent } from "../api/events.js";
import { useForm } from "react-hook-form";
import { toFormValues, toPayload, applyServerErrors } from "../utils/eventForm.js";
import { useUserData } from "../hooks/useUserData.js";

export default function EventFormPage() {
    const { user } = useUserData();
    const queryClient = useQueryClient();
    const { id } = useParams();
    const navigate = useNavigate();
    const isEdit = !!id;

    const { data: categories = [] } = useQuery({
        queryKey: ["categories"],
        queryFn: getCategories,
    });

    const { data: event } = useQuery({
        queryKey: ["event", id],
        queryFn: () => getEvent(id),
        enabled: isEdit
    });

    const { register, handleSubmit, setError, formState: { errors } } = useForm({
        values: event ? toFormValues(event) : undefined,
    });
    
    const save = useMutation({
        mutationFn: (form) => isEdit ? updateEvent(id, toPayload(form)) : createEvent(toPayload(form)),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["myEvents"] });
            queryClient.invalidateQueries({ queryKey: ["event", id] });
            navigate("/organizer/events");
        },
        onError: (error) => {
            if (!applyServerErrors(error, setError)) {
                setError("root", { message: "Something went wrong. Please try again." });
            }
        }
    });

    const remove = useMutation({
        mutationFn: () => deleteEvent(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["myEvents"] });
            navigate("/organizer/events");
        },
        onError: () => {
            setError("root", { message: "Could not delete the event." });
        }
    });

    function handleDelete() {
        if (window.confirm("Delete this event?") === true) remove.mutate();
    }

    return (
        <div>
            <Typography variant="h1">
                {isEdit ? "Edit event" : "Create event"}
            </Typography>
            <form onSubmit={handleSubmit((form) => save.mutate(form))}>
                <input {...register("event_name", { required: "Event name is required"})} />
                {errors.event_name && <span>{errors.event_name.message}</span>}
                <textarea {...register("event_description")} />
                <select {...register("category_id", { required: "Category is required" })}>
                    <option value="">
                        Select category
                    </option>
                    {categories.map((c) => (
                        <option key={c.id} value={c.id}>{c.category_name}</option>
                    ))}
                </select>
                <input type="date" {...register("start_date", { required: "Start date is required"})} />
                {errors.start_date && <span>{errors.start_date.message}</span>}
                <input type="time" {...register("start_time", { required: "Start time is required"})} />
                <input type="date" {...register("end_date", { required: "End date is required"})} />
                {errors.end_date && <span>{errors.end_date.message}</span>}
                <input type="time" {...register("end_time", { required: "End time is required"})} />
                <input {...register("location", { required: "Location is required" })} />
                 {errors.location && <span>{errors.location.message}</span>}
                <input type="number" step="0.01" {...register("entry_price")} />
                <input value={user.organization ?? ""} readOnly />
                <button type="submit">{isEdit ? "Save" : "Publish"} </button>
                {isEdit && (
                    <button type="button" onClick={handleDelete}>Delete</button>
                )}
                {errors.root && <p>{errors.root.message}</p>}
            </form>
        </div>
    )
}