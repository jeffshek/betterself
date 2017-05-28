import React, { Component } from "react";

import { AddSupplementEvent } from "./add_supplement_event";
import { SupplementEntryLogTable } from "./supplement_event_table";
import { EventLogView } from "../resources_table/resource_table_view";

class SupplementsLogView extends EventLogView {
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

export default SupplementsLogView;
