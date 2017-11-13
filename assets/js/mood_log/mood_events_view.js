import React from "react";

import { AddSleepEvent } from "./add_mood_event";
import { SleepEntryLogTable } from "./mood_events_table";
import { BasePaginatedLogView } from "../resources_table/resource_view";

export class SleepEventsLogView extends BasePaginatedLogView {
  constructor() {
    super();
    this.resourceName = "sleep_activities";
  }

  render() {
    return (
      <div>
        <AddSleepEvent addEventEntry={this.addEventEntry} />
        <SleepEntryLogTable
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
