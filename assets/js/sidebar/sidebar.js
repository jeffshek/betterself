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
      <i className={props.iconName} /> {props.label}
      </a>
  </li>
)

const ExternalDataMenu = props => (
  <div>
    <NavigationTitle title="Data Sources"/>
    <ExternalVendorsLinks />
  </div>
)

const ExternalVendorsLinks = () => (
  <div>
    <NavigationLink iconName="icon-earphones" label="Bose"/>
    <NavigationLink iconName="icon-rocket" label="FitBit"/>
    <NavigationLink iconName="icon-chart" label="Garmin"/>
    <NavigationLink iconName="icon-social-github" label="GitHub"/>
    <NavigationLink iconName="icon-target" label="RescueTime"/>
  </div>
)

const ExportSidebar = () => (
  <div>
    <NavigationTitle title="Export Data"/>
    <NavigationLink iconName="icon-cloud-download" label="All Data"/>
  </div>
)

class Sidebar extends Component {
  handleClick(e) {
    e.preventDefault();
    e.target.parentElement.classList.toggle("open");
  }

  render() {
    return (
      <nav className="sidebar sidebar-nav">
        <ul className="nav">
          <DashboardButton />

          <NavigationTitle title="Log"/>
          <NavigationLink iconName="icon-note" label="Events"/>
          <NavigationLink iconName="icon-heart" label="Heart Rate"/>
          <NavigationLink iconName="icon-graph" label="Productivity"/>
          <NavigationLink iconName="icon-volume-off" label="Sleep"/>
          <NavigationLink iconName="icon-chemistry" label="Supplements"/>

          <li className="divider" />

          <NavigationTitle title="Analytics"/>
          <NavigationLink iconName="icon-chart" label="Productivity"/>

          <li className="divider" />
          <ExternalDataMenu onClick={this.handleClick.bind(this)}/>

          <li className="divider" />
          <ExportSidebar/>

        </ul>
      </nav>
    );
  }
}

export default Sidebar;
