import React from "react";

import NavigationBar from "./homepage/NavigationBar";
import JumboHeader from "./homepage/JumboHeader";
import ChooseLanguage from "./homepage/ChooseLanguage";

export default function HomePage() {
  return (
    <>
      <NavigationBar />
      <JumboHeader />
      <ChooseLanguage />
    </>
  );
}
