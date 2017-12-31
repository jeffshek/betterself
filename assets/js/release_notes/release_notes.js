import React from "react";

// This CSS makes me want to die inside. I cannot wait to rewrite this.

export const ReleaseNotesView = () => {
  return (
    <div className="card">
      <div className="card-header analytics-text-box-label">
        <span className="font-2xl">
          Feature Updates
        </span>
      </div>
      <div className="card-block">
        <div className="release-notes">
          <b>December 30th, 2017</b>
          {" "}
          - Added ability to delete events from Daily Overview.
        </div>
        <div className="release-notes">
          <b>December 20th, 2017</b>
          {" "}
          - Added notes feature to supplement logs.
        </div>
        <div className="release-notes">
          <b>December 17th, 2017</b>
          {" "}
          <br />
          - Still making lots of progress toward mobile (aim is a mobile app release of this or next week).
          {" "}
          <br />
          - Added Log Dropdown to show the Supplement Stack Compositions
        </div>
        <div className="release-notes">
          <b>December 11th, 2017</b>
          {" "}
          - Lots of progress toward mobile, this should be arriving soon!
        </div>
        <div className="release-notes">
          <b>November 28th, 2017</b>
          {" "}
          - Slight fix toward easier login and logout pages.
        </div>
        <div className="release-notes">
          <b>November 27th, 2017</b>
          <br />
          {" "}
          - We're trying something new here, as it's been a little hard communicating with everyone about new
          features that they've requested. So for the time being, this page is going to be a place where we
          post new updates and features!!! Feel free to email me feedback at
          {" "}
          <b>jeffshek@gmail.com.</b>
          <br />
          <a href="http://res.cloudinary.com/betterhealth/image/upload/v1511838475/create-supplement-modal_fw928m.png">
            - Added popup modal when creating new supplement (it was too easily accidently autocreated
            prior).
          </a>
        </div>

      </div>
    </div>
  );
};
