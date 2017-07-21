import React, { Component, PropTypes } from "react";
import moment from "moment";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";

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

export const SupplementHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Name</th>
      <th>Ingredients</th>
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
