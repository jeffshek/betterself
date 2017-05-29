import React, { Component } from "react";
import { Link } from "react-router-dom";
import {
  DASHBOARD_INDEX_URL,
  DASHBOARD_CHARTS_URL,
  DASHBOARD_SUPPLEMENTS_EVENTS_LOGS_URL,
  DASHBOARD_HEART_RATE_LOGS_URL,
  DASHBOARD_SUPPLEMENTS_URL,
  DASHBOARD_PRODUCTIVITY_LOGS_URL,
  DASHBOARD_EVENTS_LOGS_URL
} from "../urls/constants";

const DashboardButton = () => (
  <li className="nav-item">
    <Link to={DASHBOARD_INDEX_URL} className="nav-link">
      <i className="icon-speedometer" />
      Dashboard
      <NewStatus />
    </Link>
  </li>
);

const NewStatus = () => <span className="badge badge-info">NEW</span>;

const NavigationTitle = props => (
  <li className="nav-title">
    {props.title}
  </li>
);

const NavigationLink = props => (
  <li className="nav-item">
    <Link className="nav-link" to={props.link}>
      <i className={props.iconName} /> {props.label}
    </Link>
  </li>
);

const ExternalDataMenu = props => (
  <div>
    <NavigationTitle title="Data Sources" />
    <ExternalVendorsLinks />
  </div>
);

const ExternalVendorsLinks = () => (
  <div>
    <NavigationLink
      iconName="icon-list"
      label="Supplements"
      link={DASHBOARD_SUPPLEMENTS_URL}
    />
    <NavigationLink
      iconName="icon-rocket"
      label="FitBit"
      link={DASHBOARD_CHARTS_URL}
    />
    <NavigationLink
      iconName="icon-social-github"
      label="GitHub"
      link={DASHBOARD_CHARTS_URL}
    />
    <NavigationLink
      iconName="icon-target"
      label="RescueTime"
      link={DASHBOARD_CHARTS_URL}
    />
  </div>
);

const ExportSidebar = () => (
  <div>
    <NavigationTitle title="Export Data" />
    <NavigationLink
      iconName="icon-cloud-download"
      label="All Data"
      link={DASHBOARD_CHARTS_URL}
    />
  </div>
);

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

          <NavigationTitle title="Log" />
          <NavigationLink
            iconName="icon-note"
            label="Events"
            link={DASHBOARD_EVENTS_LOGS_URL}
          />
          <NavigationLink
            iconName="icon-heart"
            label="Heart Rate"
            link={DASHBOARD_HEART_RATE_LOGS_URL}
          />
          <NavigationLink
            iconName="icon-graph"
            label="Productivity"
            link={DASHBOARD_PRODUCTIVITY_LOGS_URL}
          />
          <NavigationLink
            iconName="icon-volume-off"
            label="Sleep"
            link={DASHBOARD_HEART_RATE_LOGS_URL}
          />
          <NavigationLink
            iconName="icon-chemistry"
            label="Supplements"
            link={DASHBOARD_SUPPLEMENTS_EVENTS_LOGS_URL}
          />

          <li className="divider" />

          <NavigationTitle title="Analytics" />
          <NavigationLink
            iconName="icon-chart"
            label="Productivity"
            link={DASHBOARD_CHARTS_URL}
          />

          <li className="divider" />
          <ExternalDataMenu onClick={this.handleClick.bind(this)} />

          <li className="divider" />
          <ExportSidebar />

        </ul>
      </nav>
    );
  }
}

export default Sidebar;
