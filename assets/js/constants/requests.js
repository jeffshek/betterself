export const JSON_HEADERS = {
  Accept: "application/json",
  "Content-Type": "application/json"
};

export const JSON_AUTHORIZATION_HEADERS = {
  Authorization: `Token ${localStorage.token}`
};

export const JSON_POST_AUTHORIZATION_HEADERS = {
  Accept: "application/json",
  "Content-Type": "application/json",
  Authorization: `Token ${localStorage.token}`
};
