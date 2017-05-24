import React, { PropTypes, Component } from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/util_constants";

export class AddSupplementView extends Component {
  constructor() {
    super();
    this.state = { ready: false };
    this.addSupplementFormData = this.addSupplementFormData.bind(this);
    this.postIngredientComposition = this.postIngredientComposition.bind(this);

    this.createSupplement = this.createSupplement.bind(this);
    this.createIngredientComposition = this.createIngredientComposition.bind(
      this
    );

    this.createIngredientComposition1 = this.createIngredientComposition1.bind(
      this
    );
    this.createIngredientComposition2 = this.createIngredientComposition2.bind(
      this
    );
    this.createIngredientComposition3 = this.createIngredientComposition3.bind(
      this
    );
  }

  componentDidMount() {
    this.getPossibleSupplements();
  }

  createIngredient(ingredientName) {
    const params = {
      name: ingredientName
    };
    return fetch("/api/v1/ingredients", {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        return responseData;
      });
  }

  postIngredientComposition(
    ingredient,
    ingredientQuantity,
    ingredientMeasurement
  ) {
    const params = {
      ingredient_uuid: ingredient.uuid,
      measurement_uuid: ingredientMeasurement.uuid,
      quantity: ingredientQuantity
    };

    return fetch("/api/v1/ingredient_compositions", {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        return responseData;
      });
  }

  createSupplement(supplementName) {
    const params = {
      name: supplementName
    };
    return fetch("/api/v1/supplements", {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    })
      .then(response => {
        return response.json();
      })
      .then(function(responseData) {
        return responseData;
      });
  }

  createIngredientComposition(
    ingredientName,
    ingredientQuantity,
    ingredientMeasurement
  ) {
    // Create or get an ingredient named off of the name input
    const ingredient = this.createIngredient(ingredientName);

    // ingredient comes back as a promise, so use a then to do what we want
    const ingredientComposition = ingredient.then(
      function(ingredientResult) {
        return this.postIngredientComposition(
          ingredientResult,
          ingredientQuantity,
          ingredientMeasurement
        );
      }.bind(this)
    );

    console.log("Created" + ingredientName);

    return ingredientComposition;
  }

  createIngredientComposition1(supplementUUID) {
    // Embarrassing function, but create an ingredient if inputs are passed
    if (this.ingredientName1.value && this.ingredientQuantity1.value) {
      const ingredientName = this.ingredientName1.value;
      const ingredientQuantity = this.ingredientQuantity1.value;
      const ingredientMeasurement = this.ingredientMeasurement1;

      return this.createIngredientComposition(
        ingredientName,
        ingredientQuantity,
        ingredientMeasurement
      );
    }
  }

  createIngredientComposition2(supplementUUID) {
    // Embarrassing function, but create an ingredient if inputs are passed
    if (this.ingredientName2.value && this.ingredientQuantity2.value) {
      const ingredientName = this.ingredientName2.value;
      const ingredientQuantity = this.ingredientQuantity2.value;
      const ingredientMeasurement = this.ingredientMeasurement2;

      return this.createIngredientComposition(
        ingredientName,
        ingredientQuantity,
        ingredientMeasurement
      );
    }
  }

  createIngredientComposition3(supplementUUID) {
    // Embarrassing function, but create an ingredient if inputs are passed
  }

  addSupplementFormData(e) {
    e.preventDefault();
    const supplement = this.createSupplement(this.supplementName.value);
    supplement.then(
      function(supplementDetails) {
        const supplementUUID = supplementDetails.uuid;

        this.createIngredientComposition1(supplementUUID);
        this.createIngredientComposition2(supplementUUID);
        this.createIngredientComposition3(supplementUUID);
      }.bind(this)
    );
  }

  getPossibleSupplements() {
    fetch("/api/v1/measurements", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({ measurements: responseData });
        this.setState({ ready: true });
      });
  }

  renderMeasurements() {
    const measurementKeys = Object.keys(this.state.measurements);

    return (
      <div className="form-group col-sm-4">
        <label><strong>Measurement</strong></label>
        <select
          className="form-control"
          ref={input => this.ingredientMeasurement1 = input}
        >
          {measurementKeys.map(key => (
            <option value={key} key={key}>
              {this.state.measurements[key].name}
            </option>
          ))}
        </select>

        <select
          className="form-control"
          ref={input => this.ingredientMeasurement2 = input}
        >
          {measurementKeys.map(key => (
            <option value={key} key={key}>
              {this.state.measurements[key].name}
            </option>
          ))}
        </select>
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <strong>Create Supplement</strong> (Per Serving)
        </div>
        <div className="card-block">
          <form onSubmit={e => this.addSupplementFormData(e)}>
            <div className="row">
              <div className="form-group col-sm-4">
                <label><strong>Supplement Name</strong></label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Black Tea"
                  ref={input => this.supplementName = input}
                />
              </div>

            </div>

            <div className="row">
              <div className="form-group col-sm-4">
                <label><strong>Ingredients</strong><sup>1</sup></label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Caffeine"
                  ref={input => this.ingredientName1 = input}
                />
                <input
                  type="text"
                  className="form-control"
                  placeholder="Theanine"
                  ref={input => this.ingredientName2 = input}
                />
              </div>
              <div className="form-group col-sm-4">
                <label><strong>Quantity</strong><sup>2</sup></label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="50"
                  ref={input => this.ingredientQuantity1 = input}
                />

                <input
                  type="text"
                  className="form-control"
                  placeholder="75"
                  ref={input => this.ingredientQuantity2 = input}
                />
              </div>

              {this.state.ready ? this.renderMeasurements() : ""}

            </div>
            <div className="float-right">
              <button
                type="submit"
                id="supplement-dashboard-submit"
                className="btn btn-sm btn-success"
                onClick={e => this.addSupplementFormData(e)}
              >
                <i className="fa fa-dot-circle-o" /> Add Supplement
              </button>
            </div>
          </form>
          <div>
            <sup>1) Ingredients are optional inputs. </sup>
            <sup>2) Per unit of measurement.</sup>
          </div>
        </div>
      </div>
    );
  }
}
