import React, { Component } from "react";

import { AddSupplementEvent } from "./add_supplement_event";
import { SupplementEntryLogTable } from "./supplement_events_table";
import { EventLogView } from "../resources_table/resource_view";

export class SupplementEventsLogView extends EventLogView {
  constructor() {
    super();
    this.resourceName = "supplement_events";
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
