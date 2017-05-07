import React, { Component } from "react";
import Sidebar from "./sidebar/sidebar.js"
import LoggedInHeader from "./header/internal_header"
import Charts from './charts/charts'

export class Dashboard extends Component {
  render() {
    return (
      <div className="app">
        <LoggedInHeader />
        <div className="app-body">
          <Sidebar />
          <main className="main">
            <Charts/>
          </main>
        </div>
      </div>
    )
  }
}
