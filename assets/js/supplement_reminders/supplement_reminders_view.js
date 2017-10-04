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
        <AddSupplementReminderView />
        <SupplementReminderTable />
      </div>
    );
  }
}
