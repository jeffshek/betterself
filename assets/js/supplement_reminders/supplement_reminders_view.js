import React, { Component } from "react";
import { AddSupplementReminderView } from "./add_supplement_reminder";
import { SupplementReminderTable } from "./supplement_reminder_table";

export class SupplementRemindersView extends Component {
  constructor() {
    super();
  }

  render() {
    return (
      <div>
        <div className="card-header">
          <strong id="add-supplement-entry-text">
            Add Texting Reminders (Limit 5 A Day)
          </strong>
        </div>
        <AddSupplementReminderView />
        <SupplementReminderTable />
      </div>
    );
  }
}
