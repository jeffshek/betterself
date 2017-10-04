import React from "react";
import { EventLogView } from "../resources_table/resource_view";
import { UserActivityLogTable } from "./user_activities_table";
import { AddUserActivity } from "./add_user_activity";

export class UserActivitiesLogView extends EventLogView {
  constructor() {
    super();
    this.resourceName = "user_activities";
  }

  render() {
    return (
      <div>
        <AddUserActivity addEventEntry={this.addEventEntry} />
        <UserActivityLogTable
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
