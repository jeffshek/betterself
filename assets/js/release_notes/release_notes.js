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
        <h3 text-align="left">
          <b>November 27th, 2017</b>
          {" "}
          - We're trying something new here, as it's been a little hard communicating with everyone about new features that they've requested. So for the time being, this page is going to be a place where we post new updates and features!!! Feel free to email me feedback at
          {" "}
          <b>jeffshek@gmail.com.</b>
          <br /><br />
          <a href="http://res.cloudinary.com/betterhealth/image/upload/v1511838475/create-supplement-modal_fw928m.png">
            - Added popup modal when creating new supplement (it was too easily accidently autocreated prior).
          </a>
        </h3>
      </div>
    </div>
  );
};
