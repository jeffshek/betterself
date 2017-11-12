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
