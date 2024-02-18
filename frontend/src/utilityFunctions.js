export const msToHours = (milliseconds) => {
  let seconds = Math.floor(milliseconds / 1000);
  let minutes = Math.floor(seconds / 60);
  let hours = Math.floor(minutes / 60);
  return hours;
};

export const secondsToHours = (seconds) => {
  let minutes = Math.floor(seconds / 60);
  let hours = Math.floor(minutes / 60);
  return hours;
};


export const formatDate = (dateString, withTime) => {
  let options = {
    year: "numeric",
    month: "numeric",
    day: "numeric",
  };

  if (withTime) {
    options.hour = "numeric";
    options.minute = "numeric";
  }

  return new Date(dateString).toLocaleString("en-US", options);
};
