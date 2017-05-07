import React, { Component } from "react";
import Sidebar from "./sidebar/sidebar.js"
import LoggedInHeader from "./header/internal_header"

export class Dashboard extends Component {
  render() {
    return (
      <div className="app">
        <LoggedInHeader />
        <Sidebar />
      </div>
    )
  }
}
