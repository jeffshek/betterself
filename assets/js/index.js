import React, { PropTypes, Component } from "react";
import ReactDOM from "react-dom";
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from "react-router-dom";

import {
  DASHBOARD_INDEX_URL,
  LOGIN_URL,
  HOME_URL,
  LOGOUT_URL
} from "./urls/constants";
import { Authenticator } from "./authentication/auth";
import LoginView from "./authentication/login";
import Header from "./fragments/header";
import Footer from "./fragments/footer";
import { HomePage } from "./home/home";
import { Dashboard } from "./dashboard";
import { LogoutView } from "./authentication/logout";

const BetterSelfRouter = () => (
  <Router>
    <div>
      <Header />

      {/*Public Routes*/}
      <Route exact path={HOME_URL} component={HomePage} />

      <Route path={LOGIN_URL} component={LoginView} />
      <Route path={LOGOUT_URL} component={LogoutView} />

      {/* TODO Routes and Components */}
      {/*<Route path={SETTINGS_URL} component={LoggedOutView} />*/}
      {/*<Route path={DASHBOARD_OVERVIEW_URL} component={LoggedOutView} />*/}

      {/*Private Routes*/}
      <PrivateRoute path={DASHBOARD_INDEX_URL} component={Dashboard} />

      <Footer />
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
