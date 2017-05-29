import React, { Component } from "react";
import { EventLogView } from "../resources_table/resource_view";
import { AddUserActivityEvent } from "./add_user_event";
import { UserActivityEventLogTable } from "./user_event_table";

class UserActivitiesEventLogView extends EventLogView {
  constructor() {
    super();
    this.resourceName = "user_activity_events";
  }

  render() {
    return (
      <div>
        <AddUserActivityEvent addEventEntry={this.addEventEntry} />
        <UserActivityEventLogTable
          eventHistory={this.state.eventHistory}
          currentPageNumber={this.state.currentPageNumber}
          lastPageNumber={this.state.lastPageNumber}
          renderReady={this.state.loadedHistory}
          getEventHistory={this.getEventHistory}
        />
      </div>
    );
  }
}

export default UserActivitiesEventLogView;
