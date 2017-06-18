import React, { Component } from "react";

import { AddSupplementEvent } from "./add_sleep_event";
import { SupplementEntryLogTable } from "./sleep_events_table";
import { EventLogView } from "../resources_table/resource_view";

class SleepEventsLogView extends EventLogView {
  constructor() {
    super();
    this.resourceName = "sleep_events";
  }

  render() {
    return (
      <div>
        <AddSupplementEvent addEventEntry={this.addEventEntry} />
        <SupplementEntryLogTable
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

export default SleepEventsLogView;
