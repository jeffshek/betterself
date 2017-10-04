import React, { Component } from "react";
import { BasePaginatedLogView } from "../resources_table/resource_view";
import {
  SupplementEntryLogTable
} from "../supplement_events_log/supplement_events_table";
import {
  AddSupplementEvent
} from "../supplement_events_log/add_supplement_event";
import { getFetchJSONAPI } from "../utils/fetch_utils";
import { BaseEventLogTable } from "../resources_table/resource_table";
import { AddSupplementReminderView } from "./add_supplement_reminder";

export class SupplementRemindersView extends Component {
  constructor() {
    super();
  }

  render() {
    return (
      <div>
        <AddSupplementReminderView />
      </div>
    );
  }
}
