import React from "react";
import ReactDOM from "react-dom";
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  withRouter
} from "react-router-dom";

import {
  DASHBOARD_DAILY_OVERVIEW_ANALYTICS_URL,
  DASHBOARD_INDEX_URL,
  DASHBOARD_PRODUCTIVITY_ANALYTICS_URL,
  DASHBOARD_PRODUCTIVITY_LOGS_URL,
  DASHBOARD_SLEEP_ANALYTICS_URL,
  DASHBOARD_SLEEP_LOGS_URL,
  DASHBOARD_SUPPLEMENT_OVERVIEW_ANALYTICS_URL,
  DASHBOARD_SUPPLEMENT_REMINDERS_URL,
  DASHBOARD_SUPPLEMENTS_EVENTS_LOGS_URL,
  DASHBOARD_SUPPLEMENTS_URL,
  DASHBOARD_USER_ACTIVITIES_EVENTS_LOGS_URL,
  DASHBOARD_USER_ACTIVITIES_URL,
  DEMO_SIGNUP_URL,
  EXPORT_ALL_DATA_URL,
  HOME_URL,
  LOGIN_URL,
  LOGOUT_URL,
  SETTINGS_URL,
  SIGNUP_URL
} from "./constants/urls";

import { Authenticator } from "./authentication/auth";
import { HomePage } from "./home/home";
import { Dashboard } from "./dashboard";
import { LogoutView } from "./authentication/logout";
import { SupplementView } from "./supplements/supplements_view";
import {
  UserActivitiesLogView
} from "./user_activities_log/user_activities_view";
import { SignupView } from "./signup/signup";
import { CreateDemoUserView } from "./create_demo_user/create_demo_user";
import { SleepEventsLogView } from "./sleep_log/sleep_events_view";
import { UserSettingsView } from "./user_settings/user_settings";
import { ProductivityAnalyticsView } from "./analytics/productivity";
import { SupplementLogView } from "./supplement_log/supplement_log_view";
import {
  ProductivityLogView
} from "./productivity_log/productivity_event_view";
import { SleepAnalyticsView } from "./analytics/sleep";
import {
  UserActivitiesEventsLogView
} from "./user_activities_events_log/user_activites_events_view";
import { LoginView } from "./authentication/login";
import { UserExportAllDataView } from "./export/export";
import {
  DailyOverviewAnalyticsView
} from "./daily_overview/daily_overview_view";
import { SupplementsOverview } from "./supplement_overview/supplement_overview";
import {
  SupplementRemindersView
} from "./supplement_reminders/supplement_reminders_view";

const BetterSelfRouter = () => (
  <Router>
    <div>
      {/*Public Routes*/}
      <Route exact path={HOME_URL} component={HomePage} />
      <Route
        exact
        path={SIGNUP_URL}
        component={e => <Dashboard view={SignupView} />}
      />
      <Route
        exact
        path={DEMO_SIGNUP_URL}
        component={e => <Dashboard view={CreateDemoUserView} />}
      />
      <Route exact path={LOGIN_URL} component={LoginView} />
      <Route exact path={LOGOUT_URL} component={LogoutView} />
      {/*Private Routes*/}
      <PrivateRoute
        exact
        path={DASHBOARD_INDEX_URL}
        component={e => <Dashboard view={ProductivityAnalyticsView} />}
      />
      {/*Analytics*/}
      <PrivateRoute
        path={DASHBOARD_SLEEP_ANALYTICS_URL}
        component={e => <Dashboard view={SleepAnalyticsView} />}
      />
      <PrivateRoute
        path={DASHBOARD_PRODUCTIVITY_ANALYTICS_URL}
        component={e => <Dashboard view={ProductivityAnalyticsView} />}
      />
      <PrivateRoute
        path={`${DASHBOARD_DAILY_OVERVIEW_ANALYTICS_URL}:date`}
        component={DailyOverviewAnalyticsView}
      />
      <PrivateRoute
        path={`${DASHBOARD_SUPPLEMENT_OVERVIEW_ANALYTICS_URL}:supplementUUID`}
        component={SupplementsOverview}
      />
      <PrivateRoute
        exact
        path={DASHBOARD_DAILY_OVERVIEW_ANALYTICS_URL}
        component={DailyOverviewAnalyticsView}
      />
      <PrivateRoute
        path={DASHBOARD_SUPPLEMENTS_EVENTS_LOGS_URL}
        component={e => <Dashboard view={SupplementLogView} />}
      />
      <PrivateRoute
        path={DASHBOARD_SUPPLEMENTS_URL}
        component={e => <Dashboard view={SupplementView} />}
      />
      <PrivateRoute
        path={DASHBOARD_PRODUCTIVITY_LOGS_URL}
        component={e => <Dashboard view={ProductivityLogView} />}
      />
      <PrivateRoute
        path={DASHBOARD_USER_ACTIVITIES_EVENTS_LOGS_URL}
        component={e => <Dashboard view={UserActivitiesEventsLogView} />}
      />
      <PrivateRoute
        path={DASHBOARD_USER_ACTIVITIES_URL}
        component={e => <Dashboard view={UserActivitiesLogView} />}
      />
      <PrivateRoute
        path={DASHBOARD_SUPPLEMENT_REMINDERS_URL}
        component={e => <Dashboard view={SupplementRemindersView} />}
      />
      <PrivateRoute
        path={DASHBOARD_SLEEP_LOGS_URL}
        component={e => <Dashboard view={SleepEventsLogView} />}
      />
      <PrivateRoute
        path={SETTINGS_URL}
        component={e => <Dashboard view={UserSettingsView} />}
      />
      <PrivateRoute
        path={EXPORT_ALL_DATA_URL}
        component={e => <Dashboard view={UserExportAllDataView} />}
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
