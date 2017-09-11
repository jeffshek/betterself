import React from "react";
import moment from "moment";
import { Link } from "react-router-dom";
import { getSupplementOverviewURLFromUUID } from "../routing/routing_utils";

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

export const SupplementHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Name</th>
      <th className="center-source">Ingredients</th>
      <th className="center-source">Actions</th>
      <th>Date Added</th>
    </tr>
  </thead>
);

export const SupplementRow = props => {
  const data = props.object;

  const { uuid, name } = data;
  const dateCreated = data.created;
  const ingredientsFormatted = getIngredientsCompositionsLabels(
    data.ingredient_compositions
  );
  const timeFormatted = moment(dateCreated).format("l - h:mm:ss a");
  const supplementOverviewLink = getSupplementOverviewURLFromUUID(uuid);

  return (
    <tr>
      <td><Link to={supplementOverviewLink}>{name}</Link></td>
      <td>{ingredientsFormatted}</td>
      <td>
        <div className="center-icon">
          <div className="edit-icon" onClick={e => props.selectModalEdit(data)}>
            <i className="fa fa-edit fa-1x" />
          </div>
          &nbsp;
          <div
            className="remove-icon"
            onClick={e => props.confirmDelete(uuid, name)}
          >
            <i className="fa fa-remove fa-1x" />
          </div>
        </div>
      </td>
      <td>{timeFormatted}</td>
    </tr>
  );
};
