import React, { Component, PropTypes } from "react";
import { Link, Redirect, withRouter } from "react-router-dom";

import { Authenticator } from "./auth";

export class LogoutView extends Component {
  render(cb) {
    Authenticator.logout(cb);
    // This is pretty subpar, but there's a few CSS issues I need to work out
    window.location.assign("/");
    // Per React spec return back an empty page even though the location will be changing so quickly
    return <div />;
  }
}
