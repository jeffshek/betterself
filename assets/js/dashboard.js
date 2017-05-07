import React, { Component } from "react";
import Sidebar from "./sidebar/sidebar"
import LoggedInHeader from "./header/internal_header"

export class Dashboard extends Component {
  render() {
    return (
      <div>
        <LoggedInHeader />
        <Sidebar/>
      </div>
    )
  }
}
