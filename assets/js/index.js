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
  DASHBOARD_SUPPLEMENT_LOGS_URL
} from "./urls/constants";

import { Authenticator } from "./authentication/auth";
import LoginView from "./authentication/login";
import { HomePage } from "./home/home";
import { Dashboard } from "./dashboard";
import { LogoutView } from "./authentication/logout";
import SupplementsLogView from './supplements/supplements'
import Charts from './charts/charts'

const SupplementLogView = () => <Dashboard view={SupplementsLogView}/>
const BetterSelfRouter = () => (
  <Router>
    <div>
      {/*Public Routes*/}
      <Route exact path={HOME_URL} component={HomePage} />
      <Route exact path={LOGIN_URL} component={LoginView} />
      <Route exact path={LOGOUT_URL} component={LogoutView} />

      {/*Private Routes*/}
      <PrivateRoute path={DASHBOARD_INDEX_URL} component={ChartsView} />
      <PrivateRoute path={DASHBOARD_CHARTS_URL} component={ChartsView} />
      <PrivateRoute path={DASHBOARD_SUPPLEMENT_LOGS_URL} component={SupplementLogView} />

    </div>
  </Router>
);

const ChartsView = () => <Dashboard view={Charts}/>

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
