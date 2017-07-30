import React, { Component, PropTypes } from "react";
import { Nav, NavItem, NavLink } from "reactstrap";

export class MultiTabTableView extends Component {
  constructor(props) {
    super(props);

    // renderTableRow
    // tableColumns
    // tableData

    this.state = {
      selectedTabLocation: 0
    };

    this.renderNavTabs = this.renderNavTabs.bind(this);
  }

  renderNavTabs(props) {
    const navCount = this.props.tableColumns.indexOf(props);

    if (this.state.selectedTabLocation === navCount) {
      return (
        <NavItem className="selected-modal" key={props}>
          <NavLink>{props}</NavLink>
        </NavItem>
      );
    }
    return (
      <NavItem className="default-background" key={props}>
        <NavLink>{props}</NavLink>
      </NavItem>
    );
  }

  render() {
    return (
      <div className="float">
        <div className="card">
          <Nav tabs>
            {this.props.tableColumns.map(this.renderNavTabs)}
          </Nav>
        </div>
      </div>
    );
  }
}
