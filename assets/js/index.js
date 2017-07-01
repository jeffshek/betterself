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
  DASHBOARD_ANALYTICS_SLEEP,
  DASHBOARD_SUPPLEMENTS_EVENTS_LOGS_URL,
  DASHBOARD_HEART_RATE_LOGS_URL,
  DASHBOARD_SUPPLEMENTS_URL,
  DASHBOARD_PRODUCTIVITY_LOGS_URL,
  DASHBOARD_EVENTS_LOGS_URL,
  DASHBOARD_USER_ACTIVITIES_URL,
  SIGNUP_URL,
  DEMO_SIGNUP_URL,
  DASHBOARD_SLEEP_LOGS_URL,
  SETTINGS_URL
} from "./constants/urls";

import { Authenticator } from "./authentication/auth";
import LoginView from "./authentication/login";
import { HomePage } from "./home/home";
import { Dashboard } from "./dashboard";
import { LogoutView } from "./authentication/logout";

import SupplementsLogView from "./supplement_events_log/supplement_events_view";
import ChartsView from "./analytics/sleep";
import HeartRateLogView from "./heart_rate_log/legacy_heart_rate_log";
import UserActivitiesEventLogView
  from "./user_activities_events_log/user_activites_events_view";
import { SupplementView } from "./supplements_log/supplements_view";
import ProductivityLogView from "./productivity_log/productivity_event_view";
import {
  UserActivitiesLogView
} from "./user_activities_log/user_activities_view";
import { SignupView } from "./signup/signup";
import { CreateDemoUserView } from "./create_demo_user/create_demo_user";
import { SleepEventsLogView } from "./sleep_log/sleep_events_view";
import { UserSettingsView } from "./user_settings/user_settings";

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
const DashboardSignupView = () => <Dashboard view={SignupView} />;
const DashboardDemoUserView = () => <Dashboard view={CreateDemoUserView} />;
const DashboardSleepView = () => <Dashboard view={SleepEventsLogView} />;
const DashboardSettingsView = () => <Dashboard view={UserSettingsView} />;

const BetterSelfRouter = () => (
  <Router>
    <div>
      {/*Public Routes*/}
      <Route exact path={HOME_URL} component={HomePage} />
      <Route exact path={SIGNUP_URL} component={DashboardSignupView} />
      <Route exact path={DEMO_SIGNUP_URL} component={DashboardDemoUserView} />
      <Route exact path={LOGIN_URL} component={LoginView} />
      <Route exact path={LOGOUT_URL} component={LogoutView} />

      {/*Private Routes*/}
      <PrivateRoute
        path={DASHBOARD_INDEX_URL}
        component={DashboardChartsView}
      />
      <PrivateRoute
        path={DASHBOARD_ANALYTICS_SLEEP}
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

      <PrivateRoute
        path={DASHBOARD_SLEEP_LOGS_URL}
        component={DashboardSleepView}
      />

      <PrivateRoute path={SETTINGS_URL} component={DashboardSettingsView} />

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
