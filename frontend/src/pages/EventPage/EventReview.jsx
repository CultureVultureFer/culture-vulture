import { Typography } from "@material-tailwind/react";

export function EventReview() {
  return (
    <div className="w-full pt-5 mt-8 border-t border-gray-200">
      <Typography variant="h3" color="blue-gray" className="mb-4 font-semibold">
        Reviews and comments
      </Typography>
      <div className="mb-8">
        <textarea
          disabled
          className="w-full border border-gray-500 rounded-md p-3 text-base focus:outline-none focus:border-gray-500 resize-none h-32 placeholder:text-base"
          placeholder="Write a comment or leave a review"
        ></textarea>
      </div>
      <div className="flex items-center gap-4 mb-6">
        <Typography variant="h4" color="blue-gray" className="font-semibold">
          Comments
        </Typography>
      </div>
      <div className="py-10 text-center">
        <Typography className="!text-xl font-normal !text-gray-500">
          No comments currently.
        </Typography>
      </div>
    </div>
  );
}

export default EventReview;