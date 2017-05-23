import React, { PropTypes, Component } from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/util_constants";

export class AddSupplementView extends Component {
  constructor() {
    super();
    this.state = { ready: false };
    this.createSupplement = this.createSupplement.bind(this);
    this.createIngredientComposition = this.createIngredientComposition.bind(
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

  createIngredientComposition(
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

  createSupplement(e) {
    e.preventDefault();

    // First thing we have to do is create any ingredient compositions
    // if necessary. So let's check the 3 possible ingredients and see if
    // they're filled in. If so, create them
    if (this.ingredientName1.value && this.ingredientQuantity1.value) {
      const ingredientName = this.ingredientName1.value;
      const ingredientQuantity = this.ingredientQuantity1.value;
      const ingredientMeasurement = this.ingredientMeasurement1;

      // Create or get an ingredient named off of the name input
      const ingredient = this.createIngredient(ingredientName);
      // This comes back as a promise, so use a then to do what we want
      const ingredientComposition = ingredient.then(
        function(ingredientResult) {
          return this.createIngredientComposition(
            ingredientResult,
            ingredientQuantity,
            ingredientMeasurement
          );
        }.bind(this)
      );
      ingredientComposition.then(function(data) {
        console.log(data);
      });
    }

    // let ingredientMeasurement = this.state.measurements[this.ingredientMeasurement1.value]

    // this.createIngredientComposition(this.ingredientName1, this.ingredientQuantity1, ingredientMeasurement)
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
          <form onSubmit={e => this.createSupplement(e)}>
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
                <label><strong>Vendor</strong></label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Lipton"
                  ref={input => this.vendorName = input}
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
                onClick={e => this.createSupplement(e)}
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
