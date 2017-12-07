import React, { Component } from "react";
import { DJANGO_BASE_LOGIN } from "../constants/urls";

// After a bit of debate, just switch back to using a Django form for a login to make it all easier
export class LoginView extends Component {
  constructor() {
    super();

    window.location.assign(DJANGO_BASE_LOGIN);
  }

  render() {
    <div />;
  }
}
