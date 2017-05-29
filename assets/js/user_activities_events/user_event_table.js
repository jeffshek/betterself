import React, { Component, PropTypes } from "react";
import moment from "moment";
import { CubeLoadingStyle } from "../animations/LoadingStyle";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";

const confirmDelete = (uuid, eventDate) => {
  const answer = confirm(
    `WARNING: This will delete the following Productivity Log \n\n${eventDate} \n\nConfirm? `
  );
  const params = {
    uuid: uuid
  };

  if (answer) {
    fetch("/api/v1/productivity_log/", {
      method: "DELETE",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    }).then(
      // After deleting, just refresh the entire page. In the future, remove
      // from the array and setState
      location.reload()
    );
  }
};

const UserActivityEventHistoryRow = props => {
  const data = props.object;

  const { source, time, duration_minutes, uuid } = data;
  const user_activity = data.user_activity;

  const name = user_activity.name;

  const timeFormatted = moment(time).format("dddd, MMMM Do YYYY, h:mm:ss a");

  return (
    <tr>
      <td>{timeFormatted}</td>
      <td>{name}</td>
      <td>{duration_minutes}</td>
      <td>Not Important</td>
      <td>Negative</td>
      <td>{source}</td>
      <td>
        <div onClick={e => confirmDelete(uuid, eventDate)}>
          <div className="remove-icon">
            <i className="fa fa-remove" />
          </div>
        </div>
      </td>
    </tr>
  );
};

const UserActivityEventHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Time</th>
      <th>Activity</th>
      <th>Duration Minutes</th>
      <th>Significant</th>
      <th>Negative</th>
      <th>Source</th>
      <th>Actions</th>
    </tr>
  </thead>
);

class BaseEventLogTable extends Component {
  constructor() {
    super();
    this.getPageResults = this.getPageResults.bind(this);
  }

  getPageResults(page) {
    if (page === 0 || page > this.props.lastPageNumber) {
      return;
    }

    this.props.getEventHistory(page);
  }

  getPaginationPageLinkRender(page, page_link_verbose_title) {
    // page_link_verbose_title might be "Last", "First" or just a number
    return (
      <li className="page-item">
        <a
          className="page-link"
          onClick={e => {
            this.getPageResults(page);
          }}
        >
          {page_link_verbose_title}
        </a>
      </li>
    );
  }

  getPaginationActivePageLinkRender() {
    const currentPageNumber = this.props.currentPageNumber;

    return (
      <li className="page-item active">
        <a className="page-link">{currentPageNumber}</a>
      </li>
    );
  }

  checkCurrentPageIsLastName() {
    const currentPageNumber = this.props.currentPageNumber;
    const lastPageNumber = this.props.lastPageNumber;

    if (currentPageNumber === lastPageNumber) {
      return true;
    }
  }

  getNavPaginationControlRender() {
    const currentPageNumber = this.props.currentPageNumber;
    const lastPageNumber = this.props.lastPageNumber;

    return (
      <nav>
        <ul className="pagination">
          {this.getPaginationPageLinkRender(1, "First")}
          {this.getPaginationPageLinkRender(currentPageNumber - 1, "Prev")}
          {this.getPaginationActivePageLinkRender()}
          {this.checkCurrentPageIsLastName()
            ? ""
            : this.getPaginationPageLinkRender(
                currentPageNumber + 1,
                currentPageNumber + 1
              )}
          <li className="page-item">
            <a className="page-link">...</a>
          </li>
          {this.getPaginationPageLinkRender(currentPageNumber + 1, "Next")}
          {this.getPaginationPageLinkRender(lastPageNumber, "Last")}
        </ul>
      </nav>
    );
  }
}

export class UserActivityEventLogTable extends BaseEventLogTable {
  getTableRender() {
    const historicalData = this.props.eventHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <UserActivityEventHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <UserActivityEventHistoryRow
              key={key}
              object={historicalData[key]}
            />
          ))}
        </tbody>
      </table>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Productivity History</strong>
        </div>
        {/*Conditional loading if ready to review or not yet*/}
        {!this.props.renderReady
          ? <CubeLoadingStyle />
          : <div className="card-block">
              <div className="float-right">
                {this.getNavPaginationControlRender()}
              </div>
              {this.getTableRender()}
              {this.getNavPaginationControlRender()}
            </div>}

      </div>
    );
  }
}
