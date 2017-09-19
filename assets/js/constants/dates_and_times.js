export const YEAR_MONTH_DAY_FORMAT = "MMMM Do YYYY";
export const READABLE_DATE_TIME_FORMAT = "dddd, MMMM Do YYYY, h:mm:ss a";
export const READABLE_TIME_FORMAT = "h:mm:ss a";
export const DATE_REQUEST_FORMAT = "YYYY-MM-DD";
export const DATETIME_CREATED_FORMAT = "l - h:mm:ss a";

// 12/5/2016 Tu (this is what it looks like)
export const ABBREVIATED_CHART_DATE = "l dd";

export const minutesToHours = (minutes, decimal_places = 2) => {
  return (minutes / 60).toFixed(decimal_places);
};
