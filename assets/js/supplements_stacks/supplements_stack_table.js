import React from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { BaseLogTable } from "../resources_table/resource_table";
import { SupplementStackRow, SupplementStackTableHeader } from "./constants";
import { getFetchJSONAPI } from "../utils/fetch_utils";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";
import Select from "react-select";

export class SupplementStackTable extends BaseLogTable {
  constructor() {
    super();

    this.state = {
      supplements: [],
      supplementsStacks: [],
      renderReady: false,
      addModal: false,
      selectedSupplementQuantity: 1
    };

    this.resourceURL = "/api/v1/supplements_stacks/";
  }

  componentDidMount() {
    this.getSupplementStacks();
    this.getSupplements();
  }

  getSupplementStacks() {
    const url = "api/v1/supplements_stacks";
    getFetchJSONAPI(url).then(responseData => {
      this.setState({
        supplementsStacks: responseData,
        renderReady: true
      });
    });
  }

  selectedStackChange = props => {
    this.setState({
      selectedStack: props,
      addModal: true
    });
  };

  getTableRender() {
    const historicalData = this.state.supplementsStacks;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <SupplementStackTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <SupplementStackRow
              key={key}
              object={historicalData[key]}
              selectedStackChange={this.selectedStackChange}
            />
          ))}
        </tbody>
      </table>
    );
  }

  renderReady() {
    if (!this.state.renderReady) {
      return <CubeLoadingStyle />;
    }
    return (
      <div className="card-block">
        {this.getTableRender()}
      </div>
    );
  }

  submitEdit() {
    const params = {
      uuid: this.state.selectedStack["uuid"]
      //name: this.state["supplementName"]
    };

    this.putParamsUpdate(params);
    this.toggle();
  }

  getSupplements() {
    const url = "/api/v1/supplements/";
    getFetchJSONAPI(url).then(responseData => {
      this.setState({
        supplements: responseData
      });
    });
  }

  handleSupplementChange = val => {
    let updatedLocation;
    if (val) {
      updatedLocation = val.value;
    } else {
      updatedLocation = null;
    }
    this.setState({
      selectedSupplementIndex: updatedLocation
    });
  };

  toggle = () => {
    this.setState({
      addModal: !this.state.addModal
    });
  };

  handleSettingsChange = event => {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    const intValue = parseInt(value);

    this.setState({
      [name]: intValue
    });
  };

  renderAddModal() {
    if (!this.state.addModal) {
      return <div />;
    }

    if (!this.state.supplements) {
      return <div />;
    }

    // React-Select needs it in this value: label format
    const supplementsKeys = Object.keys(this.state.supplements);
    const supplementDetails = supplementsKeys.map(e => {
      return {
        value: e,
        label: this.state.supplements[e].name
      };
    });

    return (
      <Modal isOpen={this.state.addModal} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>
          Add a supplement to {this.state.selectedStack.name}
        </ModalHeader>
        <ModalBody>
          <label className="form-control-label add-event-label">
            Supplement Name
          </label>
          <Select
            name="form-field-name"
            value={this.state.selectedSupplementIndex}
            options={supplementDetails}
            onChange={this.handleSupplementChange}
          />
          <br />
          <label className="form-control-label add-event-label">
            Supplement Quantity
          </label>
          <input
            name="selectedSupplementQuantity"
            type="number"
            className="form-control"
            defaultValue={this.state.selectedSupplementQuantity}
            onChange={this.handleSettingsChange}
          />
          <br />
        </ModalBody>
        <ModalFooter>
          <Button color="decline-modal" onClick={this.toggle}>Cancel</Button>
          <Button color="primary" onClick={this.submitEdit}>Update</Button>
        </ModalFooter>
      </Modal>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Supplement Stacks</strong>
        </div>
        {this.renderReady()}
        {this.renderAddModal()}
      </div>
    );
  }
}
