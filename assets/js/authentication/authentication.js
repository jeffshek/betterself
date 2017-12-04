import React, { Component } from "react";
import { USER_INFO_URL } from "../constants/urls";

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
      .then(e => {
        console.log(e);
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
