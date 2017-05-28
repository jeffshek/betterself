import React, { Component, PropTypes } from "react";
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
//
// class SupplementView extends Component {
//   constructor() {
//     super();
//     this.state = {
//       loadedHistory: false
//     };
//     this.addEventEntry = this.addEventEntry.bind(this);
//     this.getEventHistory = this.getEventHistory.bind(this);
//   }
//
//   componentDidMount() {
//     this.getEventHistory();
//   }
//
// }
