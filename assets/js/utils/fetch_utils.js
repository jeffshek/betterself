import React from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";

export const getFetchJSONAPI = url => {
  return fetch(url, {
    method: "GET",
    headers: JSON_AUTHORIZATION_HEADERS
  }).then(response => {
    return response.json();
  });
};
