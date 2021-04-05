import React from "react";

import NavigationBar from "./NavigationBar";
import JumboHeader from "./wordtablepage/JumboHeader";
import WordTable from "./wordtablepage/WordTable";

export default function SpanishWordsPage() {
  return (
    <>
      <NavigationBar />
      <JumboHeader srcLang="spanish" destLang="english" />
      <WordTable srcLang="spanish" destLang="english" />
    </>
  );
}
