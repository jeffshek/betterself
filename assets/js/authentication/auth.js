import React from "react";
import {
  JSON_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/requests";
import {
  REST_API_LOGIN_URL,
  REST_API_LOGOUT_URL,
  SESSION_LOGOUT_URL
} from "../constants/urls";

export const Authenticator = {
  isAuthenticated: !!localStorage.token,
  token: localStorage.token,

  login(username, password, cb) {
    if (localStorage.token) {
      this.isAuthenticated = true;
      return;
    }

    this.getToken(username, password, res => {
      if (res.authenticated) {
        this.isAuthenticated = true;
        localStorage.token = res.token;
        localStorage.userName = username;
        if (cb) cb(true);
      } else {
        if (cb) cb(false);
      }
    });
  },

  logout(cb) {
    // This could be much much cleaner, but here do a three step process to logout.
    // 1. Use a django rest-point to invalidate the login session / API
    // 2. Delete the localstorages, so it won't keep trying with the token
    // 3. Then redirect to a page that will invalidate any cookies just to be sure nothing gets stuck.
    fetch(REST_API_LOGOUT_URL, {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      credentials: "same-origin"
    })
      .then(response => {
        delete localStorage.token;
        delete localStorage.userName;
        this.isAuthenticated = false;
        return response.json();
      })
      .then(responseData => {
        window.location.assign(SESSION_LOGOUT_URL);
      });
  },

  getToken(username, pass, cb) {
    let credentials = {
      username: username,
      password: pass
    };

    // Don't use the standard fetchPostUtils because the headers would be blank
    fetch(REST_API_LOGIN_URL, {
      method: "POST",
      headers: JSON_HEADERS,
      body: JSON.stringify(credentials)
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        if ("key" in responseData) {
          cb({
            authenticated: true,
            token: responseData.key
          });
        } else {
          alert("Invalid Login Error");
          cb({
            authenticated: false
          });
        }
      })
      .catch(error => {
        alert("Network Issue Encountered");
        cb({
          authenticated: false
        });
      });
  }
};
