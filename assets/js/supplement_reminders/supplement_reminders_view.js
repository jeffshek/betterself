import React, { Component } from "react";

import { AddSupplementReminderView } from "./add_supplement_reminder";
import { SupplementReminderTable } from "./supplement_reminder_table";
import { getFetchJSONAPI } from "../utils/fetch_utils";

export class SupplementRemindersView extends Component {
  constructor() {
    super();

    this.state = {};
    this.getReminders();
  }

  getReminders() {
    const url = "api/v1/supplement_reminders/";
    getFetchJSONAPI(url).then(responseData => {
      this.setState({ supplementReminders: responseData });
    });
  }

  render() {
    if (!this.state.supplementReminders) {
      return <div />;
    }

    return (
      <div>
        <div className="card-header">
          <strong id="add-supplement-entry-text">
            Add Texting Reminders (Limit 5 A Day)
          </strong>
        </div>
        <AddSupplementReminderView reminders={this.state.supplementReminders} />
        <SupplementReminderTable reminders={this.state.supplementReminders} />
      </div>
    );
  }
}
