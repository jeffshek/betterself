import React, { Component } from "react";
import { Link } from "react-router-dom";
import {
  DASHBOARD_INDEX_URL,
  DASHBOARD_SLEEP_ANALYTICS_URL,
  DASHBOARD_SUPPLEMENTS_EVENTS_LOGS_URL,
  DASHBOARD_HEART_RATE_LOGS_URL,
  DASHBOARD_SUPPLEMENTS_URL,
  DASHBOARD_PRODUCTIVITY_LOGS_URL,
  DASHBOARD_USER_ACTIVITIES_EVENTS_LOGS_URL,
  DASHBOARD_USER_ACTIVITIES_URL,
  DASHBOARD_SLEEP_LOGS_URL,
  DASHBOARD_PRODUCTIVITY_ANALYTICS_URL,
  EXPORT_ALL_DATA_URL,
  DASHBOARD_DAILY_OVERVIEW_ANALYTICS_URL,
  DASHBOARD_SUPPLEMENT_REMINDERS_URL,
  DASHBOARD_SUPPLEMENTS_STACKS_URL
} from "../constants/urls";

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
      {props.isNew ? <span className="badge badge-info"> NEW</span> : <span />}
    </Link>
  </li>
);

const DataSourcesMenu = props => (
  <div>
    <NavigationTitle title="Data Sources" />
    <DataSourcesMenuLinks />
  </div>
);

const DataSourcesMenuLinks = () => (
  <div>
    <NavigationLink
      iconName="icon-calendar"
      label="Text Reminders"
      link={DASHBOARD_SUPPLEMENT_REMINDERS_URL}
    />
    <NavigationLink
      iconName="icon-calendar"
      label="Supp. Stacks"
      link={DASHBOARD_SUPPLEMENTS_STACKS_URL}
      isNew={true}
    />
    <NavigationLink
      iconName="icon-list"
      label="Activity Types"
      link={DASHBOARD_USER_ACTIVITIES_URL}
    />
    <NavigationLink
      iconName="icon-list"
      label="Supplements"
      link={DASHBOARD_SUPPLEMENTS_URL}
    />
  </div>
);

const ExportSidebar = () => (
  <div>
    <NavigationTitle title="Export Data" />
    <NavigationLink
      iconName="icon-cloud-download"
      label="All Data"
      link={EXPORT_ALL_DATA_URL}
    />
  </div>
);

const LogSidebar = () => {
  return (
    <div>
      <NavigationTitle title="Log" />
      <NavigationLink
        iconName="icon-chemistry"
        label="Supplements"
        link={DASHBOARD_SUPPLEMENTS_EVENTS_LOGS_URL}
      />
      <NavigationLink
        iconName="icon-note"
        label="Events"
        link={DASHBOARD_USER_ACTIVITIES_EVENTS_LOGS_URL}
      />
      {/*<NavigationLink*/}
      {/*iconName="icon-heart"*/}
      {/*label="Heart Rate"*/}
      {/*link={DASHBOARD_HEART_RATE_LOGS_URL}*/}
      {/*/>*/}
      <NavigationLink
        iconName="icon-graph"
        label="Productivity"
        link={DASHBOARD_PRODUCTIVITY_LOGS_URL}
      />
      <NavigationLink
        iconName="icon-volume-off"
        label="Sleep"
        link={DASHBOARD_SLEEP_LOGS_URL}
      />
      <NavigationLink
        iconName="icon-volume-off"
        label="Mood"
        link={DASHBOARD_SLEEP_LOGS_URL}
        isNew={true}
      />
    </div>
  );
};

const AnalyticsSidebar = () => {
  return (
    <div>
      <NavigationTitle title="Analytics" />
      <NavigationLink
        iconName="icon-chart"
        label="Sleep"
        link={DASHBOARD_SLEEP_ANALYTICS_URL}
      />
      <NavigationLink
        iconName="icon-speedometer"
        label="Productivity"
        link={DASHBOARD_PRODUCTIVITY_ANALYTICS_URL}
      />
      <NavigationLink
        iconName="icon-clock"
        label="Daily Overview"
        link={DASHBOARD_DAILY_OVERVIEW_ANALYTICS_URL}
      />
    </div>
  );
};

const Sidebar = () => {
  return (
    <nav className="sidebar sidebar-nav">
      <ul className="nav">
        <LogSidebar />
        <li className="divider" />
        <AnalyticsSidebar />
        <li className="divider" />
        <DataSourcesMenu />
        <li className="divider" />
        <ExportSidebar />

      </ul>
    </nav>
  );
};

export default Sidebar;
