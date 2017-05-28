import React, { Component } from "react";
import { EventLogView } from "../resources_table/resource_table_view";
import { AddUserEvent } from "./add_user_event";

class UserActivitiesEventLogView extends EventLogView {
  constructor() {
    super();
    this.resourceName = "user_activity_events";
  }

  render() {
    return (
      <div>
        <AddUserEvent addEventEntry={this.addEventEntry} />
        {/*<ProductivityLogTable*/}
        {/*eventHistory={this.state.eventHistory}*/}
        {/*currentPageNumber={this.state.currentPageNumber}*/}
        {/*lastPageNumber={this.state.lastPageNumber}*/}
        {/*renderReady={this.state.loadedHistory}*/}
        {/*getEventHistory={this.getEventHistory}*/}
        {/*/>*/}
      </div>
    );
  }
}

export default UserActivitiesEventLogView;
