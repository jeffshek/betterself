import React, { PropTypes, Component } from "react";
import { withRouter, Redirect, Link } from "react-router-dom";

import { Authenticator } from "./auth";
import { HOME_URL } from "../urls/constants";

export class LogoutView extends Component {
  render(cb) {
    Authenticator.logout(cb);
    // This is pretty subpar, but there's a few CSS issues I need to work out
    window.location.assign("/");
  }
}
