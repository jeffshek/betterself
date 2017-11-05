import React from "react";

import { AddSupplementsStack } from "./add_supplements_stack";
import { SupplementsStackTable } from "./supplements_stack_table";
import { BaseLogTable } from "../resources_table/resource_table";

export class SupplementsStackView extends BaseLogTable {
  constructor() {
    super();
    this.resourceName = "supplements_stacks";
  }

  //componentDidMount() {
  //  this.getEventHistory();
  //}

  render() {
    return (
      <div>
        <AddSupplementsStack addEventEntry={this.addEventEntry} />
        <SupplementsStackTable />
      </div>
    );
  }
}
