import React from "react";
import { BaseEventLogTable } from "../resources_table/resource_table";
import {
  SupplementReminderRow,
  SupplementReminderTableHeader
} from "./constants";

export class SupplementReminderTable extends BaseEventLogTable {
  constructor(props) {
    const { reminders } = props;
    super();
    this.state = {
      reminders: reminders
    };

    this.resourceURL = "/api/v1/supplement_reminders/";
  }

  confirmDelete = (uuid, name, reminder_time) => {
    const answer = confirm(
      `WARNING: This will delete the following supplement reminder \n\n${name} at ${reminder_time} \n\nConfirm? `
    );

    if (answer) {
      this.deleteUUID(uuid);
    }
  };

  renderTable() {
    if (!this.state.reminders) {
      return <div />;
    }

    const reminders = this.state.reminders;
    const remindersKeys = Object.keys(reminders);

    return (
      <div className="card-block">
        <table className="table table-bordered table-striped table-condensed">
          <SupplementReminderTableHeader />
          <tbody>
            {remindersKeys.map(key => (
              <SupplementReminderRow
                key={key}
                object={reminders[key]}
                confirmDelete={this.confirmDelete}
              />
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Supplements</strong>
        </div>
        {this.renderTable()}
      </div>
    );
  }
}
