import React, { Component } from "react";
import { Link } from "react-router-dom";

class Sidebar extends Component {
  handleClick(e) {
    e.preventDefault();
    e.target.parentElement.classList.toggle("open");
  }

  render() {
    return (
      <div className="sidebar">
        <nav className="sidebar-nav">
          <ul className="nav">
            <li className="nav-item">
              <Link to={"/dashboard"} className="nav-link">
                <i className="icon-speedometer" />
                Dashboard
                <span className="badge badge-info">
        NEW
        </span>
              </Link>
            </li>
            <li className="nav-title">
              Log
            </li>
            <li className="nav-item nav-dropdown">
              <a className="nav-link"><i className="icon-note" /> Events</a>
            </li>
            <li className="nav-item nav-dropdown">
              <a className="nav-link"><i className="icon-note" /> Heart Rate</a>
              <a className="nav-link">
                <i className="icon-note" /> Productivity
              </a>
              <a className="nav-link"><i className="icon-note" /> Sleep</a>
              <a className="nav-link">
                <i className="icon-note" /> Supplements
              </a>
            </li>
            <li className="divider" />
            <li className="nav-title">
              Analytics
            </li>
            <li className="nav-item">
              <Link to={"/widgets"} className="nav-link">
                <i className="icon-calculator" /> Productivity{" "}
              </Link>
            </li>
            <li className="divider" />
            <li className="nav-title">
              Data Sources
            </li>
            <li className="nav-item nav-dropdown">
              <a
                className="nav-link nav-dropdown-toggle"
                href="#"
                onClick={this.handleClick.bind(this)}
              >
                <i className="icon-star" /> External
              </a>
              <ul className="nav-dropdown-items">
                <Link to={"/plugins/loading-buttons"} className="nav-link">
                  <i className="icon-cursor" /> Bose
                </Link>
                <Link to={"/plugins/loading-buttons"} className="nav-link">
                  <i className="icon-cursor" /> FitBit
                </Link>
                <Link to={"/plugins/loading-buttons"} className="nav-link">
                  <i className="icon-cursor" /> Garmin
                </Link>
                <Link to={"/plugins/loading-buttons"} className="nav-link">
                  <i className="icon-cursor" /> GitHub
                </Link>
                <Link to={"/plugins/loading-buttons"} className="nav-link">
                  <i className="icon-cursor" /> RescueTime
                </Link>
              </ul>
              <li className="nav-item nav-dropdown">
                <a className="nav-link"><i className="icon-note" /> Export</a>
              </li>
            </li>
          </ul>
        </nav>
      </div>
    );
  }
}

export default Sidebar;
