import React, { Component } from "react";
import { Nav, NavItem, NavLink } from "reactstrap";
import PropTypes from "prop-types";

export class MultiTabTableView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedTabLocation: 0
    };
  }

  navLinkClickTab = event => {
    event.preventDefault();

    const target = event.target;
    const name = target.name;
    const navCount = this.props.tableNavTabs.indexOf(name);

    this.setState({ selectedTabLocation: navCount });
  };

  renderNavTabs = props => {
    const navCount = this.props.tableNavTabs.indexOf(props);

    if (this.state.selectedTabLocation === navCount) {
      return (
        <NavItem className="selected-modal" key={props}>
          <NavLink>{props}</NavLink>
        </NavItem>
      );
    }
    return (
      <NavItem className="default-background" key={props}>
        <NavLink onClick={this.navLinkClickTab} name={props}>{props}</NavLink>
      </NavItem>
    );
  };

  renderTableData() {
    // There may be a more elegant way of doing this (declaring a variable), just to use <TableRow> syntax
    // but I don't know it.
    const TableRow = this.props.tableRowRenderer;
    const tableData = this.props.tableData[this.state.selectedTabLocation];

    return (
      <div className="card-block">
        <table className="table">
          <thead>
            <tr>
              {this.props.tableColumnHeaders.map(key => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableData.length > 0 &&
              tableData.map(key => (
                <TableRow key={key.uniqueKey} details={key} />
              ))}
          </tbody>
        </table>
      </div>
    );
  }

  render() {
    return (
      <div className="float">
        <div className="card">
          <Nav tabs>
            <NavItem className="default-background">
              <NavLink className="add-event-label">
                {this.props.tableName}
              </NavLink>
            </NavItem>
            {this.props.tableNavTabs.map(this.renderNavTabs)}
          </Nav>
          {this.renderTableData()}
        </div>
      </div>
    );
  }
}

MultiTabTableView.propTypes = {
  tableData: PropTypes.array.isRequired,
  tableNavTabs: PropTypes.array.isRequired,
  tableRowRenderer: PropTypes.func.isRequired,
  tableColumnHeaders: PropTypes.array.isRequired,
  tableName: PropTypes.string.isRequired
};
