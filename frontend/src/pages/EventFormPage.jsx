import {} from "@material-tailwind/react";
import { useParams, useNavigate } from "react-router";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getCategories,
  getEvent,
  createEvent,
  updateEvent,
  deleteEvent,
} from "../api/events.js";
import { useForm } from "react-hook-form";
import {
  toFormValues,
  toPayload,
  applyServerErrors,
} from "../utils/eventForm.js";
import { useUserData } from "../hooks/useUserData.js";
import OrganizerHeader from "../components/OrganizerHeader.jsx";

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
    enabled: isEdit,
  });

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm({
    values: event ? toFormValues(event) : undefined,
  });

  const save = useMutation({
    mutationFn: (form) =>
      isEdit ? updateEvent(id, toPayload(form)) : createEvent(toPayload(form)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["myEvents"] });
      queryClient.invalidateQueries({ queryKey: ["event", id] });
      navigate("/organizer/events");
    },
    onError: (error) => {
      if (!applyServerErrors(error, setError)) {
        setError("root", {
          message: "Something went wrong. Please try again.",
        });
      }
    },
  });

  const remove = useMutation({
    mutationFn: () => deleteEvent(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["myEvents"] });
      navigate("/organizer/events");
    },
    onError: () => {
      setError("root", { message: "Could not delete the event." });
    },
  });

  function handleDelete() {
    if (window.confirm("Delete this event?") === true) remove.mutate();
  }

  const inputBox =
    "border border-accent-grey bg-inverse-text rounded px-3 py-2 text-primary-text ";

  return (
    <div className="min-h-screen bg-primary-background">
      <OrganizerHeader current={isEdit ? "edit event" : "create event"} />
      <main className="px-40 py-8">
        <div className="flex flex-col gap-2">
          <h1 className="text-4xl text-primary-text">
            {isEdit ? "Edit your event" : "Create a new event"}
          </h1>
          <p className=" text-primary-text text-2xl">
            {isEdit
              ? " Update your event information below."
              : "Fill in your event information below."}
          </p>
        </div>

        <form
          onSubmit={handleSubmit((form) => save.mutate(form))}
          className="flex flex-col gap-10 py-5"
        >
          <section className="border-2 rounded-md bg-inverse-text border-accent-grey p-6 mb-6 flex flex-col gap-5">
            <h2 className="text-2xl text-primary-foreground">
              01 - Basic information
            </h2>
            <div className="flex flex-col gap-2">
              <label className="text-xl  text-primary-text">Event title</label>
              <input
                placeholder="Enter event title"
                className={inputBox} 
                {...register("event_name", {
                  required: "Event name is required",
                })}
              />
              {errors.event_name && <span>{errors.event_name.message}</span>}
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xl  text-primary-text">Description</label>
              <textarea
                placeholder="Enter description"
                className={inputBox}
                rows={3}
                {...register("event_description")}
              />
            </div>
            <div className="grid grid-cols-3 gap-6">
              <div className="flex flex-col">
                <label className="text-xl  text-primary-text">Category</label>
                <select
                  className={inputBox}
                  {...register("category_id", {
                    required: "Category is required",
                  })}
                >
                  <option value="">Select category</option>
                  {categories.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.category_name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex flex-col opacity-60">
                <label className="text-xl  text-primary-text">Organizer</label>
                <input
                  className={inputBox}
                  value={user.organization ?? ""}
                  readOnly
                />
              </div>
              <div className="flex flex-col">
                <label className="text-xl  text-primary-text">Price</label>
                <input
                  className={inputBox}
                  type="number"
                  step="0.01"
                  {...register("entry_price")}
                />
              </div>
            </div>
          </section>

          <section className="border-2 rounded-md bg-inverse-text border-accent-grey p-6 flex flex-col gap-5">
            <h2 className="text-2xl text-primary-foreground">
              02 - Date and location
            </h2>

            <div className="grid grid-cols-2 gap-6">
              <div className="flex flex-col gap-2">
                <label className="text-xl text-primary-text">Start date</label>
                <input
                  type="date"
                  className={inputBox}
                  {...register("start_date", {
                    required: "Start date is required",
                  })}
                />
                {errors.start_date && <span>{errors.start_date.message}</span>}
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xl text-primary-text">Start time</label>
                <input
                  type="time"
                  className={inputBox}
                  {...register("start_time", {
                    required: "Start time is required",
                  })}
                />
                {errors.start_time && <span>{errors.start_time.message}</span>}
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-xl text-primary-text">End date</label>
                <input
                  type="date"
                  className={inputBox}
                  {...register("end_date", {
                    required: "End date is required",
                  })}
                />
                {errors.end_date && <span>{errors.end_date.message}</span>}
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xl text-primary-text">End time</label>
                <input
                  type="time"
                  className={inputBox}
                  {...register("end_time", {
                    required: "End time is required",
                  })}
                />
                {errors.end_time && <span>{errors.end_time.message}</span>}
              </div>

              <div className="flex flex-col gap-2 col-span-2">
                <label className="text-xl text-primary-text">Location</label>
                <input
                  placeholder="Search for a venue/address"
                  className={inputBox}
                  {...register("location", {
                    required: "Location is required",
                  })}
                />
                {errors.location && <span>{errors.location.message}</span>}
              </div>
            </div>
          </section>

          <div className="flex items-center justify-between">
            <button
              type="button"
              onClick={() => navigate("/organizer/events")}
              className="text-accent-red font-medium cursor-pointer text-xl!"
            >
              Cancel
            </button>

            <div className="flex items-center gap-4">
              {isEdit && (
                <button
                  type="button"
                  onClick={handleDelete}
                  className="bg-accent-red text-inverse-text text-xl! rounded-full px-8 py-2 font-medium cursor-pointer"
                >
                  Delete event
                </button>
              )}
              <button
                type="submit"
                disabled={save.isPending}
                className="bg-primary-foreground text-inverse-text text-2xl! rounded-full px-15 py-2 font-medium cursor-pointer disabled:opacity-50"
              >
                {isEdit ? "Save" : "Publish"}
              </button>
            </div>
          </div>
          {errors.root && (
            <p className="text-accent-red">{errors.root.message}</p>
          )}
        </form>
      </main>
    </div>
  );
}
