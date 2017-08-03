import React, { Component } from "react";
import Sidebar from "./sidebar/sidebar.js";
import LoggedInHeader from "./header/internal_header";

export class Dashboard extends Component {
  // This was a really regrettable idea now that I'm struggling to figure out how to get my Routing
  // parameters
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="app">
        <LoggedInHeader />
        <div className="app-body">
          <Sidebar />
          <main className="main">
            <this.props.view />
          </main>
        </div>
      </div>
    );
  }
}
