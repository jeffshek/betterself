import { Link, Redirect } from "react-router-dom";
import React, { Component, PropTypes } from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import { saveAs } from "file-saver";
import { DASHBOARD_USER_ACTIVITIES_EVENTS_LOGS_URL } from "../constants/urls";

export class UserExportAllDataView extends Component {
  constructor() {
    super();
    this.state = {
      loaded: false
    };
  }
  componentDidMount() {
    // get the download data and then immediately save it
    // after this happens, render happens to another page
    this.getData();
  }

  getData() {
    fetch("/api/v1/user/export-data", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.blob();
      })
      .then(blob => {
        saveAs(blob, "historical_data.xlsx");
        this.setState({ loaded: true });
      });
  }

  render() {
    const loaded = this.state.loaded;

    return (
      <div>
        {loaded
          ? <Redirect to={DASHBOARD_USER_ACTIVITIES_EVENTS_LOGS_URL} />
          : <div />}
      </div>
    );
  }
}
