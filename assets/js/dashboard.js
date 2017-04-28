import React, { Component } from "react";
import Sidebar from "./fragments/sidebar"

export class Dashboard extends Component {
  render() {
    return (
      <div className="container body">
        <div className="main_container">
          <div className="col-md-3 left_col">
            <div className="left_col scroll-view">
              <Sidebar/>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
