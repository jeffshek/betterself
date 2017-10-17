import React, { Component } from "react";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/requests";

export class BaseLogTable extends Component {
  constructor() {
    super();
  }

  handleDatetimeChangeOnEditObject = moment => {
    let editObject = this.state.editObject;
    editObject.time = moment;

    this.setState({ editObject: editObject });
  };

  handleInputChange = event => {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  };

  toggle = () => {
    this.setState({
      modal: !this.state.modal
    });
  };

  selectModalEdit = object => {
    this.setState({ editObject: object });

    // Turn on modal to show for editing
    this.toggle();
  };

  putParamsUpdate(params) {
    fetch(this.resourceURL, {
      method: "PUT",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        // Once we get the data, refresh the page
        location.reload();
      });
  }

  deleteUUID(uuid) {
    const params = {
      uuid: uuid
    };

    fetch(this.resourceURL, {
      method: "DELETE",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    }).then(
      // After deleting, just refresh the entire page. In the future, remove
      // from the array and setState
      location.reload()
    );
  }

  getPageResults = page => {
    if (page === 0 || page > this.props.lastPageNumber) {
      return;
    }

    this.props.getEventHistory(page);
  };

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
