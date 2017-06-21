import React from "react";
import { withRouter, Redirect } from "react-router-dom";
import { JSON_HEADERS } from "../constants/util_constants";

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

        // TODO - Just delete the entire localStorage
        localStorage.token = res.token;
        localStorage.userName = res.userName;
        localStorage.timezone = res.timezone;

        if (cb) cb(true);
      } else {
        if (cb) cb(false);
      }
    });
  },

  logout(cb) {
    delete localStorage.token;
    delete localStorage.userName;
    delete localStorage.timezone;

    this.isAuthenticated = false;
    setTimeout(cb, 100);
  },

  getToken(username, pass, cb) {
    let credentials = {
      username: username,
      password: pass
    };

    fetch("/api-token-auth/", {
      method: "POST",
      headers: JSON_HEADERS,
      body: JSON.stringify(credentials)
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        // Because these are promises second then means data has arrived
        if ("token" in responseData) {
          cb({
            authenticated: true,
            token: responseData.token,
            userName: responseData.username,
            timezone: responseData.timezone
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
