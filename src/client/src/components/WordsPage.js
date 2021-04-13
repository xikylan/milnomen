import React from "react";

import NavigationBar from "./NavigationBar";
import JumboHeader from "./wordspage/JumboHeader";
import WordTable from "./wordspage/WordTable";

export default function WordsPage({ srcLang, destLang }) {
  return (
    <>
      <NavigationBar />
      <JumboHeader srcLang={srcLang} destLang={destLang} />
      <WordTable srcLang={srcLang} destLang={destLang} />
    </>
  );
}
