import React, { Component } from "react";
import {
  DASHBOARD_INDEX_URL,
  HOME_URL,
  USER_INFO_URL
} from "../constants/urls";
import LoggedInHeader from "../header/internal_header";
import Sidebar from "../sidebar/sidebar";

// For any pages that are already SessionAuthenticated

export class AuthenticationView extends Component {
  constructor() {
    super();

    fetch(USER_INFO_URL, {
      method: "GET",
      credentials: "same-origin"
    })
      .then(responseData => {
        return responseData.json();
      })
      .then(responseData => {
        if ("token" in responseData) {
          localStorage.token = responseData.token;
          localStorage.userName = responseData.username;
        } else {
          alert("Error. Unable to login. Please contact support.");
          window.location.assign(HOME_URL);
        }
      })
      .then(e => {
        window.location.assign(DASHBOARD_INDEX_URL);
      });
  }

  render() {
    return (
      <div className="app">
        <LoggedInHeader />
        <div className="app-body">
          <Sidebar />
          <main className="main" />
        </div>
      </div>
    );
  }
}
