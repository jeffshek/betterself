import React, { PropTypes, Component } from "react";
import { withRouter, Redirect } from "react-router-dom";

import { Authenticator } from "./auth";
import { HOME_URL } from "../urls/constants";

export class LogoutView extends Component {
  render(cb) {
    Authenticator.logout(cb);
    return <Redirect to={HOME_URL} />;
  }
}
