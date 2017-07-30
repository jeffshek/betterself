import React, { Component, PropTypes } from "react";
import { Nav, NavItem, NavLink } from "reactstrap";

const TableRow = props => {
  const data = props.details;
  return (
    <tr>
      <td>{data[0]}</td>
      <td>{data[1]}</td>
    </tr>
  );
};

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

  renderTableData() {
    return (
      <div className="card-block">
        <table className="table">
          <thead>
            <tr>
              <th>Activity</th>
              <th>Correlation</th>
            </tr>
          </thead>
          <tbody>
            {this.props.tableData.map(key => (
              <TableRow key={key} details={key} />
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
            {this.props.tableColumns.map(this.renderNavTabs)}
          </Nav>
          {this.renderTableData()}
        </div>
      </div>
    );
  }
}
