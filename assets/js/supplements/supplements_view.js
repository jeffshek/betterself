import React, { Component } from "react";
import { SupplementTable } from "./supplements_table";
import { AddSupplementView } from "./add_supplement";

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
