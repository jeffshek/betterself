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
  DASHBOARD_SUPPLEMENTS_URL
} from "./urls/constants";

import { Authenticator } from "./authentication/auth";
import LoginView from "./authentication/login";
import { HomePage } from "./home/home";
import { Dashboard } from "./dashboard";
import { LogoutView } from "./authentication/logout";

import SupplementsLogView
  from "./supplements_events_log/supplements_events_log_view";
import ChartsView from "./productivity_charts/productivity_charts";
import HeartRateLogView from "./heart_rate_log/heart_rate_log";
import { SupplementView } from "./supplements/supplements";

const DashboardSupplementLogView = () => (
  <Dashboard view={SupplementsLogView} />
);
const DashboardChartsView = () => <Dashboard view={ChartsView} />;
const DashboardHeartRateView = () => <Dashboard view={HeartRateLogView} />;
const DashboardSupplementsView = () => <Dashboard view={SupplementView} />;

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
