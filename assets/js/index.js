import React, { PropTypes, Component } from "react";
import ReactDOM from "react-dom";
import {
  BrowserRouter as Router,
  Route,
  Redirect,
  withRouter
} from "react-router-dom";

import {
  DASHBOARD_INDEX_URL,
  LOGIN_URL,
  HOME_URL,
  LOGOUT_URL,
  DASHBOARD_CHARTS_URL,
  DASHBOARD_SUPPLEMENTS_EVENTS_LOGS_URL,
  DASHBOARD_HEART_RATE_LOGS_URL,
  DASHBOARD_SUPPLEMENTS_URL,
  DASHBOARD_PRODUCTIVITY_LOGS_URL,
  DASHBOARD_EVENTS_LOGS_URL,
  DASHBOARD_USER_ACTIVITIES_URL
} from "./urls/constants";

import { Authenticator } from "./authentication/auth";
import LoginView from "./authentication/login";
import { HomePage } from "./home/home";
import { Dashboard } from "./dashboard";
import { LogoutView } from "./authentication/logout";

import SupplementsLogView from "./supplement_event_log/supplement_events_view";
import ChartsView from "./productivity_charts/productivity_charts";
import HeartRateLogView from "./heart_rate_log/heart_rate_log";
import UserActivitiesEventLogView
  from "./user_activities_events/user_activites_events_view";
import { SupplementView } from "./supplements/supplements_view";
import ProductivityLogView
  from "./productivity_log/productivity_event_log_view";
import { UserActivitiesLogView } from "./user_activities/user_activities_view";

const DashboardSupplementLogView = () => (
  <Dashboard view={SupplementsLogView} />
);
const DashboardChartsView = () => <Dashboard view={ChartsView} />;
const DashboardHeartRateView = () => <Dashboard view={HeartRateLogView} />;
const DashboardSupplementsView = () => <Dashboard view={SupplementView} />;
const DashboardProductivityLogView = () => (
  <Dashboard view={ProductivityLogView} />
);
const DashboardUserEventLogView = () => (
  <Dashboard view={UserActivitiesEventLogView} />
);
const DashboardUserActivityView = () => (
  <Dashboard view={UserActivitiesLogView} />
);

const BetterSelfRouter = () => (
  <Router>
    <div>
      {/*Public Routes*/}
      <Route exact path={HOME_URL} component={HomePage} />
      <Route exact path={LOGIN_URL} component={LoginView} />
      <Route exact path={LOGOUT_URL} component={LogoutView} />

      {/*Private Routes*/}
      <PrivateRoute
        path={DASHBOARD_INDEX_URL}
        component={DashboardChartsView}
      />
      <PrivateRoute
        path={DASHBOARD_CHARTS_URL}
        component={DashboardChartsView}
      />
      <PrivateRoute
        path={DASHBOARD_SUPPLEMENTS_EVENTS_LOGS_URL}
        component={DashboardSupplementLogView}
      />
      <PrivateRoute
        path={DASHBOARD_HEART_RATE_LOGS_URL}
        component={DashboardHeartRateView}
      />

      <PrivateRoute
        path={DASHBOARD_SUPPLEMENTS_URL}
        component={DashboardSupplementsView}
      />

      <PrivateRoute
        path={DASHBOARD_PRODUCTIVITY_LOGS_URL}
        component={DashboardProductivityLogView}
      />

      <PrivateRoute
        path={DASHBOARD_EVENTS_LOGS_URL}
        component={DashboardUserEventLogView}
      />

      <PrivateRoute
        path={DASHBOARD_USER_ACTIVITIES_URL}
        component={DashboardUserActivityView}
      />

    </div>
  </Router>
);

const PrivateRoute = ({ component, ...rest }) => (
  <Route
    {...rest}
    render={props =>
      (Authenticator.isAuthenticated
        ? React.createElement(component, props)
        : <Redirect
            to={{
              pathname: LOGIN_URL,
              state: { from: props.location }
            }}
          />)}
  />
);

ReactDOM.render(<BetterSelfRouter />, document.getElementById("root"));
