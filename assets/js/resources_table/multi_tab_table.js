import React, { Component, PropTypes } from "react";
import { Nav, NavItem, NavLink } from "reactstrap";

const TableRow = props => {
  const { details } = props;
  return (
    <tr>
      <td>{details[0]}</td>
      <td>{details[1]}</td>
    </tr>
  );
};

export class MultiTabTableView extends Component {
  constructor(props) {
    super(props);

    // Inputs are ...
    // renderTableRow (maybe not yet)
    // tableColumns
    // tableData

    this.state = {
      selectedTabLocation: 0
    };

    this.renderNavTabs = this.renderNavTabs.bind(this);
    this.navLinkClickTab = this.navLinkClickTab.bind(this);
  }

  navLinkClickTab(event) {
    event.preventDefault();

    const target = event.target;
    const name = target.name;

    const navCount = this.props.tableColumns.indexOf(name);
    this.setState({ selectedTabLocation: navCount });
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
        <NavLink onClick={this.navLinkClickTab} name={props}>{props}</NavLink>
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
            {this.props.tableData[this.state.selectedTabLocation].map(key => (
              <TableRow key={key} details={key} />
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  render() {
    return (
      <div className="card-columns cols-2">
        <div className="float">
          <div className="card">
            <Nav tabs>
              {this.props.tableColumns.map(this.renderNavTabs)}
            </Nav>
            {this.renderTableData()}
          </div>
        </div>
        <div className="float">
          <div className="card">
            <Nav tabs>
              {this.props.tableColumns.map(this.renderNavTabs)}
            </Nav>
            {this.renderTableData()}
          </div>
        </div>
      </div>
    );
  }
}
