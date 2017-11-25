import React from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/requests";

export const getFetch = url => {
  return fetch(url, {
    method: "GET",
    headers: JSON_AUTHORIZATION_HEADERS
  });
};

export const getFetchJSONAPI = url => {
  return fetch(url, {
    method: "GET",
    headers: JSON_AUTHORIZATION_HEADERS
  }).then(response => {
    return response.json();
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
