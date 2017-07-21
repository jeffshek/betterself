import React, { PropTypes, Component } from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/util_constants";

// All the code in this file is embarassing

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
    return fetch("/api/v1/ingredients/", {
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

    return fetch("/api/v1/ingredient_compositions/", {
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

  createSupplement(supplementName, ingredientCompositions) {
    let params = {
      name: supplementName
    };
    if (ingredientCompositions) {
      params["ingredient_compositions"] = ingredientCompositions;
    }

    return fetch("/api/v1/supplements/", {
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

    return ingredientComposition;
  }

  createIngredientComposition1() {
    // Embarrassing function, but create an ingredient if inputs are passed
    if (this.ingredientName1.value && this.ingredientQuantity1.value) {
      const ingredientName = this.ingredientName1.value;
      const ingredientQuantity = this.ingredientQuantity1.value;
      const ingredientMeasurement = this.ingredientMeasurement1;

      return this.createIngredientComposition(
        ingredientName,
        ingredientQuantity,
        ingredientMeasurement
      ).then();
    }
  }

  createIngredientComposition2() {
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

  createIngredientComposition3() {
    // Embarrassing function, but create an ingredient if inputs are passed
    if (this.ingredientName3.value && this.ingredientQuantity3.value) {
      const ingredientName = this.ingredientName3.value;
      const ingredientQuantity = this.ingredientQuantity3.value;
      const ingredientMeasurement = this.ingredientMeasurement3;

      return this.createIngredientComposition(
        ingredientName,
        ingredientQuantity,
        ingredientMeasurement
      );
    }
  }

  addSupplementFormData(e) {
    e.preventDefault();
    const ingredientComposition1 = this.createIngredientComposition1();
    const ingredientComposition2 = this.createIngredientComposition2();
    const ingredientComposition3 = this.createIngredientComposition3();
    Promise.all([
      ingredientComposition1,
      ingredientComposition2,
      ingredientComposition3
    ]).then(result => {
      // Not all ingredients may have been entered
      const validCompositions = result.filter(function(element) {
        return element !== undefined;
      });
      const validCompositionsUUIDs = validCompositions.map(function(obj) {
        return { uuid: obj.uuid };
      });
      // In case there are duplicates, try not to mess up the data
      const uniqueCompositionUUIDs = [...new Set(validCompositionsUUIDs)];

      this.createSupplement(this.supplementName.value, uniqueCompositionUUIDs);
    });
  }

  getPossibleSupplements() {
    fetch("/api/v1/measurements/", {
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
        <select
          className="form-control"
          ref={input => this.ingredientMeasurement3 = input}
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
                <input
                  type="text"
                  className="form-control"
                  placeholder="Ginseng"
                  ref={input => this.ingredientName3 = input}
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
                <input
                  type="text"
                  className="form-control"
                  placeholder="10"
                  ref={input => this.ingredientQuantity3 = input}
                />
              </div>

              {this.state.ready ? this.renderMeasurements() : ""}

            </div>
            <div className="float-right">
              <button
                type="submit"
                id="create-new-supplement-button"
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
