import { CreateSupplement } from "../supplements/constants";

export const SelectDetailsSerializer = detailsList => {
  // Formats a list of resources into a format that react-select uses

  const detailsKeys = Object.keys(detailsList);
  const selectDetails = detailsKeys.map(e => {
    return {
      value: e,
      label: detailsList[e].name
    };
  });

  return selectDetails;
};

export const CreateSupplementOnNewOptionClick = props => {
  const label = props.label;
  CreateSupplement(label);
};

export const CreateActivityOnNewOptionClick = props => {
  const label = props.label;
  CreateSupplement(label);
};
