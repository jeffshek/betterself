import React from "react";
import { Link } from "react-router-dom";
import { BaseEventLogTable } from "../resources_table/resource_table";
import { getFetchJSONAPI } from "../utils/fetch_utils";
import {
  SupplementReminderRow,
  SupplementReminderTableHeader
} from "./constants";

export class SupplementReminderTable extends BaseEventLogTable {
  constructor() {
    super();
    this.state = {
      reminders: null
    };

    this.resourceURL = "/api/v1/supplement_reminders/";
  }

  componentDidMount() {
    this.getReminders();
  }

  confirmDelete = (uuid, name) => {
    const answer = confirm(
      `WARNING: This will delete the following supplement reminder \n\n${name} \n\nConfirm? `
    );

    if (answer) {
      this.deleteUUID(uuid);
    }
  };

  getReminders() {
    const url = "api/v1/supplement_reminders/";
    getFetchJSONAPI(url).then(responseData => {
      this.setState({ reminders: responseData });
    });
  }

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
