import React from "react";

import { AddSupplementStack } from "./add_supplement_stack";
import { SupplementStackTable } from "./supplement_stack_table";
import { BaseLogTable } from "../resources_table/resource_table";

export class SupplementsStackView extends BaseLogTable {
  constructor() {
    super();
    this.resourceName = "supplements_stacks";
  }

  render() {
    return (
      <div>
        <AddSupplementStack addEventEntry={this.addEventEntry} />
        <SupplementStackTable />
      </div>
    );
  }
}
