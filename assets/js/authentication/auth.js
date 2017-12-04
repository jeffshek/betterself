import React from "react";
import { JSON_HEADERS } from "../constants/requests";
import { postFetchJSONAPI } from "../utils/fetch_utils";
import { REST_API_LOGOUT_URL, REST_API_LOGIN_URL } from "../constants/urls";

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

  redirectHome() {
    window.location.assign("/");
  },

  logout(cb) {
    postFetchJSONAPI(REST_API_LOGOUT_URL).then(responseData => {
      delete localStorage.token;
      delete localStorage.userName;
      this.isAuthenticated = false;
      setTimeout(this.redirectHome, 500);
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
          console.log(responseData);
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
