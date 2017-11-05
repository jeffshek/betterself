import React from "react";

import { AddSupplementsStack } from "./add_supplements_stack";
import { SupplementStackTable } from "./supplements_stack_table";
import { BaseLogTable } from "../resources_table/resource_table";

export class SupplementsStackView extends BaseLogTable {
  constructor() {
    super();
    this.resourceName = "supplements_stacks";
  }

  render() {
    return (
      <div>
        <AddSupplementsStack addEventEntry={this.addEventEntry} />
        <SupplementStackTable />
      </div>
    );
  }
}
