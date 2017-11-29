import React from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/requests";
import { LOGOUT_URL } from "../constants/urls";

export const getFetch = url => {
  return fetch(url, {
    method: "GET",
    headers: JSON_AUTHORIZATION_HEADERS
  });
};

export const getFetchJSONAPI = url => {
  return getFetch(url).then(response => {
    // If not authenticated, means token has expired
    // force a hard logout
    if (response.status == 403) {
      window.location.assign(LOGOUT_URL);
    }
    const results = response.json();
    return results;
  });
};

export const postFetchJSONAPI = (url, postParams) => {
  return fetch(url, {
    method: "POST",
    headers: JSON_POST_AUTHORIZATION_HEADERS,
    body: JSON.stringify(postParams)
  }).then(response => {
    if (!response.ok) {
      alert("Invalid Request Entered");
    }
    return response.json();
  });
};
