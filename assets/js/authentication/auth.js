import React from "react";
import { JSON_HEADERS } from "../constants/requests";

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
    delete localStorage.token;
    delete localStorage.userName;
    this.isAuthenticated = false;
    setTimeout(cb, 100);

    // This is pretty subpar, but there's a few CSS issues I need to work out
    window.location.assign("/");
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
            token: responseData.token
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
