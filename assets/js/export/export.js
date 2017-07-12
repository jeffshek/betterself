import React, { Component, PropTypes } from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";

export class UserExportAllDataView extends Component {
  getData() {
    fetch("/api/v1/user/export-data", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        console.log(responseData);
      });
  }

  render() {
    return <div />;
  }
}
