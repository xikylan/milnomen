import React from "react";

import NavigationBar from "./homepage/NavigationBar";
import JumboHeader from "./homepage/JumboHeader";
import LanguageList from "./homepage/LanguageList";

export default function HomePage() {
  return (
    <>
      <NavigationBar />
      <JumboHeader />
      <LanguageList />
    </>
  );
}
