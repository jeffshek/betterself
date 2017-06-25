import React, { PropTypes, Component } from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/util_constants";
import moment from "moment";
import { Link } from "react-router-dom";

const SupplementHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Name</th>
      <th>Ingredients</th>
      <th className="center-source">Actions</th>
      <th>Date Added</th>
    </tr>
  </thead>
);

const getIngredientsCompositionsLabels = ingredient_compositions => {
  let ingredientLabels = [];
  // You should probably switch to a map function here ...
  for (let i = 0; i < ingredient_compositions.length; i++) {
    let details = ingredient_compositions[i];
    let ingredient_name = details.ingredient.name;
    let measurement_size;

    try {
      measurement_size = details.measurement.short_name;
    } catch (err) {
      measurement_size = "";
    }

    let quantity = details.quantity || "1";

    // Describe it as 150 mg Caffeine
    let formatted_label = `${quantity}${measurement_size} ${ingredient_name}`;

    ingredientLabels.push(formatted_label);
  }

  return ingredientLabels.join(", ");
};

const confirmDelete = (uuid, name) => {
  const answer = confirm(
    `WARNING: This will delete ALL events related to ${name}!\n\nDelete supplement - ${name}? `
  );
  const params = {
    uuid: uuid
  };
  if (answer) {
    fetch("/api/v1/supplements/", {
      method: "DELETE",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    }).then(
      // After deleting, just refresh the entire page. In the future, remove
      // from the array and setState
      location.reload()
    );
  }
};

const SupplementRow = props => {
  const data = props.object;

  const { uuid, name } = data;
  const dateCreated = data.created;
  const ingredientsFormatted = getIngredientsCompositionsLabels(
    data.ingredient_compositions
  );
  const timeFormatted = moment(dateCreated).format("l - h:mm:ss a");

  return (
    <tr>
      <td>{name}</td>
      <td>{ingredientsFormatted}</td>
      <td>
        <div className="center-icon">
          <div onClick={e => confirmDelete(uuid, name)}>
            <div className="remove-icon">
              <i className="fa fa-remove" />
            </div>
          </div>
        </div>
      </td>
      <td>{timeFormatted}</td>
    </tr>
  );
};

export class SupplementTable extends Component {
  constructor() {
    super();
    this.state = {
      ready: false
    };
  }

  componentDidMount() {
    this.getSupplements();
  }

  getSupplements() {
    fetch(`api/v1/supplements/`, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({
          supplements: responseData
        });
        this.setState({ ready: true });
      });
  }

  renderTable() {
    const supplements = this.state.supplements;
    const supplementsKeys = Object.keys(supplements);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <SupplementHistoryTableHeader />
        <tbody>
          {supplementsKeys.map(key => (
            <SupplementRow key={key} object={supplements[key]} />
          ))}
        </tbody>
      </table>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Supplements</strong>

        </div>
        {this.state.ready ? this.renderTable() : ""}
      </div>
    );
  }
}
