import React, { Component, PropTypes } from "react";

export class BaseEventLogTable extends Component {
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
