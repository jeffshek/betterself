import React, { Component } from "react";
import { EventLogView } from "../resources_table/resource_view";
import { AddUserActivityEvent } from "./add_user_activities_event";
import { UserActivityEventLogTable } from "./user_activities_events_table";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";

export class UserActivitiesEventsLogView extends EventLogView {
  constructor() {
    super();
    this.resourceName = "user_activity_events";
    // Set the state so ActivityTypes
    this.state.loadedActivityTypes = false;
  }

  componentDidMount() {
    // Override base class of componentDidMount
    this.getEventHistory();
    this.getPossibleActivities();
  }

  getPossibleActivities() {
    fetch("/api/v1/user_activities", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({ userActivityTypes: responseData.results });
        this.setState({ loadedActivityTypes: true });
      });
  }

  render() {
    return (
      <div>
        <AddUserActivityEvent
          addEventEntry={this.addEventEntry}
          renderReady={this.state.loadedActivityTypes}
          userActivityTypes={this.state.userActivityTypes}
        />
        <UserActivityEventLogTable
          eventHistory={this.state.eventHistory}
          currentPageNumber={this.state.currentPageNumber}
          lastPageNumber={this.state.lastPageNumber}
          renderReady={
            this.state.loadedHistory && this.state.loadedActivityTypes
          }
          userActivityTypes={this.state.userActivityTypes}
          getEventHistory={this.getEventHistory}
        />
      </div>
    );
  }
}
