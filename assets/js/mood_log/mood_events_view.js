import React from "react";

import { AddMoodEvent } from "./add_mood_event";
import { MoodEntryLogTable } from "./mood_events_table";
import { BasePaginatedLogView } from "../resources_table/resource_view";

export class MoodEventsLogView extends BasePaginatedLogView {
  constructor() {
    super();
    this.resourceName = "mood_logs";
  }

  render() {
    return (
      <div>
        <AddMoodEvent />
        <MoodEntryLogTable
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
