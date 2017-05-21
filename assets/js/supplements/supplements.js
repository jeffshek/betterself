import React, { Component, PropTypes } from "react";
import { SupplementTable } from "./supplements_table";
import { AddSupplementView } from "./add_supplements";

export class SupplementView extends Component {
  render() {
    return (
      <div>
        <AddSupplementView />
        <SupplementTable />
      </div>
    );
  }
}
