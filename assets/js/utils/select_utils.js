import { CreateSupplementThenReload } from "../supplements/constants";

export const SelectDetailsSerializer = detailsList => {
  // Formats a list of resources into a format that react-select uses

  const detailsKeys = Object.keys(detailsList);
  const selectDetails = detailsKeys.map(e => {
    let label = detailsList[e].name;
    if (detailsList[e].description) {
      label = label + " - " + detailsList[e].description;
    }
    return {
      value: e,
      label: label
    };
  });

  return selectDetails;
};

export const CreateSupplementOnNewOptionClick = props => {
  const label = props.label;
  CreateSupplementThenReload(label);
};
