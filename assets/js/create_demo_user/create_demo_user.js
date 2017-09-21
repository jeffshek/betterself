import React, { Component } from "react";
import { DASHBOARD_INDEX_URL } from "../constants/urls";

export class CreateDemoUserView extends Component {
  constructor() {
    super();

    // Okay this obviously doesn't need any real state, but I'm going to keep this here
    // while I refactor dynamic logins. This once had a lot of logic to create demo users, but
    // its all done magically via celery
    this.createDemoUser();
  }

  createDemoUser() {
    return fetch("/api/v1/user-signup-demo/", {
      method: "GET"
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        if ("token" in responseData) {
          // If the token is in the response, set localStorage correctly
          // and then redirect to the dashboard
          localStorage.token = responseData["token"];
          localStorage.userName = responseData["username"];
          window.location.assign(DASHBOARD_INDEX_URL);
        }
        return responseData;
      });
  }
}
