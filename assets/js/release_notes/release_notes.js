import React from "react";

export const ReleaseNotesView = () => {
  return (
    <div className="card">
      <div className="card-header analytics-text-box-label">
        <span className="font-2xl">
          Feature Updates
        </span>
      </div>
      <div className="card-block">
        <h3>
          <b>December 17th, 2017</b>
          {" "}
          - Still making lots of progress toward mobile (aim is a mobile app release of this or next week).
          {" "}
          <br />
          - Added Log Dropdown to show the Supplement Stack Compositions
        </h3>
        <h3>
          <b>December 11th, 2017</b>
          {" "}
          - Lots of progress toward mobile, this should be arriving soon!
        </h3>
        <h3>
          <b>November 28th, 2017</b>
          {" "}
          - Slight fix toward easier login and logout pages.
        </h3>
        <h3>
          <b>November 27th, 2017</b>
          {" "}
          - We're trying something new here, as it's been a little hard communicating with everyone about new
          features that they've requested. So for the time being, this page is going to be a place where we
          post new updates and features!!! Feel free to email me feedback at
          {" "}
          <b>jeffshek@gmail.com.</b>
          <br /><br />
          <a href="http://res.cloudinary.com/betterhealth/image/upload/v1511838475/create-supplement-modal_fw928m.png">
            - Added popup modal when creating new supplement (it was too easily accidently autocreated
            prior).
          </a>
        </h3>
      </div>
    </div>
  );
};
