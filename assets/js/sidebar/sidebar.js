import React, { Component } from "react";
import { Link } from "react-router-dom";

const DashboardButton = () => (
  <li className="nav-item">
    <Link to={"/dashboard"} className="nav-link">
      <i className="icon-speedometer" />
      Dashboard
      <NewStatus/>
    </Link>
  </li>
)

const NewStatus = () => (
  <span className="badge badge-info">NEW</span>
)

const NavigationTitle = props => (
  <li className="nav-title">
    {props.title}
  </li>
)

const NavigationLink = props => (
  <li className="nav-item">
    <a className="nav-link">
      <i className="icon-note" /> {props.label}
      </a>
  </li>
)


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
            <DashboardButton />

            <NavigationTitle title="Log"/>
            <NavigationLink label="Events"/>
            <NavigationLink label="Heart Rate"/>
            <NavigationLink label="Productivity"/>
            <NavigationLink label="Sleep"/>
            <NavigationLink label="Supplements"/>

            <li className="divider" />

            <NavigationTitle title="Analytics"/>
            <NavigationLink label="Productivity"/>

            <li className="divider" />
            <NavigationTitle title="Data Sources"/>

            <li className="nav-item nav-dropdown">
              <a
                className="nav-link nav-dropdown-toggle"
                href="#"
                onClick={this.handleClick.bind(this)}
              >
                <i className="icon-star" /> External
              </a>

            <ul className="nav-dropdown-items">
              <NavigationLink label="Bose"/>
              <NavigationLink label="FitBit"/>
              <NavigationLink label="Garmin"/>
              <NavigationLink label="GitHub"/>
              <NavigationLink label="RescueTime"/>
            </ul>

              <NavigationLink label="Export"/>

            </li>
          </ul>
        </nav>
      </div>
    );
  }
}

export default Sidebar;
