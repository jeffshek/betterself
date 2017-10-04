import React from "react";
import { EventLogView } from "../resources_table/resource_view";
import {
  SupplementEntryLogTable
} from "../supplement_events_log/supplement_events_table";
import {
  AddSupplementEvent
} from "../supplement_events_log/add_supplement_event";
import { getFetchJSONAPI } from "../utils/fetch_utils";

export class SupplementRemindersView extends EventLogView {
  constructor() {
    super();
    // this.resourceName = "supplement_reminders";
    this.resourceName = "supplement_events";
    this.state.loadedSupplements = false;
  }

  componentDidMount() {
    // Override base class of componentDidMount
    this.getEventHistory();
    this.getPossibleSupplements();
  }

  getPossibleSupplements() {
    const url = "/api/v1/supplements";
    getFetchJSONAPI(url).then(responseData => {
      this.setState({ supplements: responseData });
      this.setState({ loadedSupplements: true });
    });
  }

  render() {
    return (
      <div>
        <AddSupplementEvent
          addEventEntry={this.addEventEntry}
          supplements={this.state.supplements}
        />
        <SupplementEntryLogTable
          eventHistory={this.state.eventHistory}
          supplements={this.state.supplements}
          loadedSupplements={this.state.loadedSupplements}
          currentPageNumber={this.state.currentPageNumber}
          lastPageNumber={this.state.lastPageNumber}
          renderReady={this.state.loadedHistory && this.state.loadedSupplements}
          getEventHistory={this.getEventHistory}
        />
      </div>
    );
  }
}
